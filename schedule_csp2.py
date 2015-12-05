from cspbase import *
from propagators import *
import itertools
import copy

'''
Classes

Input:
    List of appointments
        Appointments = [apt1, apt2, apt3, apt4]

Classes:
    Appointment objects are intiialized with [start_time, end_time, procedures]
        Examples:
        apt1 = [2, 4, [p1]]
        apt2 = [2, 6, [p2, p3]]
        apt3 = [1, 6, [p2]]
        apt4 = [5, 6, [p3]]

    Procedures are initialized with [procedure_name, duration, staff_reqs, resources]
        Examples:
        p1 = ['flu shot', 1, ['doctor'], [r1, r2]]
        p2 = ['measure bp', 1, [], [r3, r4]]
        p3 = ['diagnose', 2, ['doctor'], []]

    Resources are initialized with [name, qty_total]
        Examples:
        r1 = ['needle', 3]
        r2 = ['bandaid', 5]
        r3 = ['bp monitor', 1]
        r4 = ['stethascope', 2]

    Staff are initialized with [name, position, times, minh, maxh]
        Examples:
        s1 = ['Deborah, 'receptionist', [1], 3, 5]
        s2 = ['Clark', 'doctor', [1,2,3,4,5], 5, 10]
        s3 = ['Lisa', 'nurse', [2,3,4], 4, 6]

Constraints: **INCOMPLETE**
    1. Appointments must start somewhere between start_time and end_time-1
    2. The time of an appointment plus its duration cannot surpass end_time
    3. At least one staff member must be assigned to an appointment
    4. All positional requirements must be filled by staff for any given appointment

    The following constraints must be used if we allow multiple appointments at one time
    5. All resources needed in an appointment must be available for the time the apopintment is booked


Scheduling CSP:
    - A schedule is a 5x5 matrix. Each column represents a day, each row represents an hour
    - An appointment can be scheduled on any day but must be scheduled within the hours of start_time and end_time
      and must satisfy all constraints listed above
    - row[i] represents the hour of i to i+1. For example, the first row corresponds to times starting at 1 and
      ending at 2
      Examples:
      [0,0] represents the first day from the first hour to the second hour. An appointment with start_time
      1 and end_time 2 would fit into [0,0], [0,1], [0,2], [0,3], [0,4] (i.e., any slot in the first row)

      An appointment with start_time 2 and end_time 4 and total_ duration 1 could fit into any column and take
      any slot in the 2nd or 3rd row

      An appointment wit start_time 2 and end_time 4 and total_duration 2 would take up 2 slots. It could fit in
      any column but would take up BOTH rows 2 and 3.

      Suppose we have the following appointments:
      Note appointments are defined with [start_time, end_time, procedures]. Suppose all procedures in this example
      have a duration of 1 hour.
      apt1 = [1, 2, [p1]]
      apt2 = [3, 4, [p3]]
      apt3 = [1, 5, [p1,p2,p3,p4]]
      apt4 = [1, 5, [p2]]

      One possible schedule would look like this
      [ [apt1],[],[],[apt3],[    ],
        [    ],[],[],[apt3],[    ],
        [apt2],[],[],[apt3],[apt4],
        [    ],[],[],[apt3],[    ],
        [    ],[],[],[apt3],[    ]]

      Another valid schedule for the same appointments would be
      [ [apt4],[apt3],[],[],[apt1],
        [    ],[apt3],[],[],[    ],
        [apt2],[apt3],[],[],[    ],
        [    ],[apt3],[],[],[    ],
        [    ],[apt3],[],[],[    ]]

'''

class Appointment:

    ''' An Appointment has the following attributes:
            starttime: earliest the appointment can be started
            endtime: latest the appointment can end (if the appointment
                    can't be finished by this time, do not start it)
            duration: length of the appointment (starttime + duration >= endtime)
            resources: a list of resources required for this appointment
    '''
    def __init__(self, start_time, end_time, resources, positions):
        self.start_time = start_time
        self.end_time = end_time
        self.resources = resources # a list of procedures
        self.position = positions
        
class Resource:
    '''A resource has the following attributes:
            resource_name: the name of the resource (a string)
            qty_total: the total number of this resource available
    '''
    def __init__(self, resource_name, qty_total, reusable):
        self.resource_name = resource_name
        self.qty_total = qty_total
        self.reusable = reusable


class Staff:
    '''A resource has the following attributes:
            name: the name of the staff member
            pos: the position this staff member holds
            minh: the minimum number of appointments this staff member can work
            maxh: the maximum number of appointments this staff member can work
    '''    
    def __init__(self, name, position, minh, maxh):
        self.name = name
        self.pos = position
        self.minh = minh
        self.maxh = maxh
        
def assign_resource(r, r_list):
    '''Helper for csp_setup. '''
    for i in r_list:
        if i.resource_name == r:
            return [i]

def csp_setup(name, app, res, staff):
    '''Create CSP object and all Variable objects needed along with their domains. '''
    
    csp = CSP(name)
    app_vars = copy.deepcopy(app) # this will be used for printing final solution
    res_vars = []   # easier to also keep separate copy of these vars for making constraints
    staff_vars = []
    res_count = 1   # this and staff_count are just for naming the variables
    staff_count = 1
    
    for a in range(len(app)):
        
        # resources
        r_list = []
        for r in app[a].resources:
            v = Variable('resource'+str(res_count)) 
            v.add_domain_values(assign_resource(r, res)) # we know exactly what resources needed so can limit domain 
            csp.add_var(v)
            res_vars.append(v)
            r_list.append(v)
            res_count+=1
        app_vars[a].resources = r_list
        
        # staff
        s_list = []
        v = Variable('staff'+str(staff_count))
        csp.add_var(v)
        v.add_domain_values(staff)
        staff_vars.append(v)
        app_vars[a].position = v
        
    return csp, app_vars, res_vars, staff_vars

def add_overlapping_staff_constraints(csp, overlaps, staff_list):
    '''Staff members should not be working on more than one appointment at a time. '''
    for i in overlaps:
        if len(i) > 1:  # overlaps found
            c_vars = [j.position for j in i]
            c = Constraint('overlap_staff', c_vars)
            sat = list(itertools.permutations(staff_list, len(i)))
            c.add_satisfying_tuples(sat)
            csp.add_constraint(c)
            
def add_correct_staff_constraints(csp, app_list, app_vars, staff_list):
    '''Only staff members with the acceptable position can cover each appointment. '''
    for i in range(len(app_list)):
        p = app_list[i].position
        v = app_vars[i].position
        s = []
        for j in staff_list:
            if j.pos in p:
                s.append((j,))
        c = Constraint('correct_staff_position', [v])
        c.add_satisfying_tuples(s)  
        csp.add_constraint(c)
        
        
def add_maxh_staff_constraints(csp, app_list, staff_vars, staff_list):
    '''Each staff member should work at least their established maximum
    number of appointments. '''
    
    args = [staff_list for m in range(len(app_list))]
    tuples = list(itertools.product(*args))
    
    for i in staff_list:
        for j in range(len(tuples)):
            if tuples[j] != None and tuples[j].count(i) > i.maxh:
                tuples[j] = None
                
    while None in tuples:
        tuples.remove(None)   
        
    c = Constraint('maxh', staff_vars)
    c.add_satisfying_tuples(tuples)  
    csp.add_constraint(c)
    
def add_minh_staff_constraints(csp, app_list, staff_vars, staff_list):
    '''Each staff member should work at least their established minimum
    number of appointments. '''
    
    args = [staff_list for m in range(len(app_list))]
    tuples = list(itertools.product(*args))
    
    for i in staff_list:
        for j in range(len(tuples)):
            if tuples[j] != None and tuples[j].count(i) < i.minh:
                tuples[j] = None
                
    while None in tuples:
        tuples.remove(None)   
        
    c = Constraint('minh', staff_vars)
    c.add_satisfying_tuples(tuples)  
    csp.add_constraint(c)
        
        
def get_reusable_resources(r):
    '''Helper for add_reusable_resource_constraints. '''
    result = []
    for i in r:
        if i.reusable:
            result.append(i)
    return result

def add_reusable_resource_constraints(csp, overlap_vars, resource_list):
    '''Overlapping appointments do not use more of one type of reusable resource 
    than what is available'''
    
    for i in overlap_vars:
        if len(i) > 1:
            reusables = get_reusable_resources(r)
            resources = [r for l in i for r in l.resources]
            args = [resource_list for m in range(len(resources))]
            tuples = list(itertools.product(*args))

            for j in reusables:
                for k in range(len(tuples)):
                    if tuples[k] != None and tuples[k].count(j) > j.qty_total:
                        tuples[k] = None
            while None in tuples:
                tuples.remove(None)

            c = Constraint('reusable_resources', resources)
            c.add_satisfying_tuples(tuples)  
            csp.add_constraint(c)
      
def get_nonreusable_resources(r):
    '''Helper for add_nonreusable_resource_constraints. '''
    result = []
    for i in r:
        if not i.reusable:
            result.append(i)
    return result

def is_nonreuseable(name, nonreusables):
    '''Helper for add_nonreusable_resource_constraints. '''
    for i in nonreusables:
        if name == i.resource_name:
                return True
    return False

def add_nonreusable_resource_constraints(csp, app_list, app_vars, resource_list):
    '''Resources that are nonreusable should not be used more times than the available
    quantity of that resource. '''
    
    nonreusables = get_nonreusable_resources(r)
    resources = []
    for i in range(len(app_list)):
        for j in range(len(app_list[i].resources)):
            if is_nonreuseable(app_list[i].resources[j], nonreusables):
                resources.append(app_vars[i].resources[j])
                
    args = [resource_list for m in range(len(resources))]
    tuples = list(itertools.product(*args)) 
    
    for j in nonreusables:
        for k in range(len(tuples)):
            if tuples[k] != None and tuples[k].count(j) > j.qty_total:
                tuples[k] = None
    while None in tuples:
        tuples.remove(None)    
    
    c = Constraint('nonreusable_resources', resources)
    c.add_satisfying_tuples(tuples)  
    csp.add_constraint(c)    

def get_overlapping_appointments(app_vars):
    '''Return a nested list of overlapping appointments. '''
    
    day = [[] for i in range(0,24)] # create a list of 24 empty lists, each representing an hour of the day

    for av in app_vars:
        for x in range(av.start_time, av.end_time):
            day[x].append(av)

    overlaps = [s for s in day if len(s)>1]

    return overlaps

def print_soln(l):
    '''Print the final arrangement of staff to appointments. Note that resources are not listed
    because as long as the CSP is solvable, all resource constraints are met. '''
    
    print("--- Final Schedule ---")
    for i in l:
        print('Appointment' + str(l.index(i)) + ' at ' + str(i.start_time) + '-' + str(i.end_time) + ':')
        print('\tStaff: '+ str(i.position.get_assigned_value().name) + ', ' + str(i.position.get_assigned_value().pos) + '\n')
        
def schedule_model(a,r,s):
    '''Create the CSP, all the Variable objects and all the Constraints. Return the final CSP
    and all the appointments to print the final output if the problem has a solution. '''
    # setup 
    csp, app_vars, res_vars, staff_vars = csp_setup('schedule',a,r,s)
    
    # overlapping appointments
    var_overlaps = get_overlapping_appointments(app_vars)
    
    # constraints
    add_overlapping_staff_constraints(csp, var_overlaps, s)
    add_correct_staff_constraints(csp, a, app_vars, s)
    add_maxh_staff_constraints(csp, a, staff_vars, s)
    add_minh_staff_constraints(csp, a, staff_vars, s)
    add_reusable_resource_constraints(csp, var_overlaps, r)
    add_nonreusable_resource_constraints(csp, a, app_vars, r)
    
    return csp, app_vars
        
def solve_schedule(a,r,s):
    '''Solve the CSP for this problem. '''
    csp, app_vars = schedule_model(a,r,s)
    solver = BT(csp)
    print("=======================================================")
    print("using GAC")
    solver.bt_search(prop_GAC)
    print_soln(app_vars)  
    
    
#appointments
a1 = Appointment(1, 3, ['needle', 'stethoscope', 'swab'], ['nurse', 'doctor'])
a2 = Appointment(3, 4, ['needle', 'thermometer'], ['nurse', 'doctor'])
a3 = Appointment(5, 7, ['needle', 'otoscope', 'bp_device'], ['nurse', 'doctor'])
a4 = Appointment(2, 5, ['thermometer'], ['nurse', 'doctor'])
a5 = Appointment (6, 8, ['otoscope', 'stethoscope', 'swab'], ['nurse', 'doctor'])
#a = [a1,a2,a3]
a = [a1,a2,a3,a4,a5]
x = get_overlapping_appointments(a)

#for t in x:

    #print("Appointment conflicts:")
    #for y in t:
        #print("start:" + str(y.start_time) + " end:" + str(y.end_time) + " resources:" + str(y.resources))

##procedures
#p1 = Procedure('injection', [('swab', 1), ('inject', 2)], ['nurse'], ['needle', 'fluid'])
#p2 = Procedure('blood pressure', [('inflate', 3), ('measure', 1)], ['nurse'], ['bp_device'])
#p3 = Procedure('heartbeat', [('listen', 2)], ['doctor'], ['stethoscope'])
#p = [p1,p2,p3]

#resources

r1 = Resource('needle', 3, False)
r2 = Resource('bp_device', 1, True)
r3 = Resource('stethoscope', 1, True)
r4 = Resource('thermometer', 3, True)
r5 = Resource('tongue depressor', 1, False)
r6 = Resource('otoscope', 2, True)
r7 = Resource('swab', 2, False)
r8 = Resource('bandage', 1, False)
r9 = Resource('gauze', 1, False)
r = [r2,r1,r3,r4,r6,r7,r8]

#staff
s1 = Staff('N1', 'nurse', 2, 10)
s2 = Staff('D1', 'doctor', 0, 0)
s3 = Staff('N2', 'nurse', 1, 10)
s4 = Staff('D2', 'doctor', 0, 0)
s = [s1,s2,s3,s4]

solve_schedule(a,r,s)