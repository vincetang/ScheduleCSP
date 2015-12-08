#Group Members:
#Vincent Tang 		998192450 	g2tangvi
#Justin Djordjevic	997412152	g1djordj
#Sandy Tran		996419148	g3transa

from cspbase import *
from propagators import *
import itertools
import copy

'''

Classes:
    Appointment objects are intiialized with start_time, end_time, [resources], [position]
        Example:
        apt1 = Appointment(2, 4, ['needle', 'stethoscope'], ['doctor', 'nurse'])

    Resources are initialized with name, qty_total, reusable
        Example:
        r1 = Resource('needle', 3, False)

    Staff are initialized with [name, position, minh, maxh]
        Example:
        s1 = ['Clark', 'doctor', 5, 10]


Constraints:
    1. All appointments are fulfilled by staff with correct position
    2. No staff member is attending more than one appointment that is overlapping
    3. Every staff member is working at most their max number of appointments
    4. Every staff member is working at least their min number of appointments
    5. Overlapping appointments do not use more of one type of reusable resource than what is available
    6. All appointments do not use more than the available number of each non reusable resource


Scheduling CSP:
    Input:
         - A list of Appointment objects
         - A list of Resource objects
         - A list of Staff objects
         Note: all Appointment objects must correspond with Resource and Staff objects; ie an appointment cannot require
         a syringe while no syringe is listed in the list of Resource objects
         
    Oputput:
         If a solution exists:
         - Each appointment is printed along with the staff member required and that staff member's position
         
         If a solution does NOT exist:
         - a notification is printed informing the user that there are insufficient resources or staff to accomodate
           all the appointments
           
    A list of resources is not printed if a solution exists because since the required resources are specified as
    input for each appointment, a solution implies that those required resources are available, otherwise there 
    would be no solution.

'''

class Appointment:

    ''' An Appointment has the following attributes:
            start_time: the hour this appointment starts
            end_time: the hour this appointment ends
            resources: a list of resources required for this appointment
            positions: a list of acceptable staff member positions to fulfill this appointment
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
            reusables = get_reusable_resources(resource_list)
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
    
    nonreusables = get_nonreusable_resources(resource_list)
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
    result = ""
    result += "--- Final Schedule ---\n"
    for i in l:
        result += ('Appointment' + str(l.index(i)) + ' at ' + str(i.start_time) + '-' + str(i.end_time) + ':\n')
        result += ('\tStaff: '+ str(i.position.get_assigned_value().name) + ', ' + str(i.position.get_assigned_value().pos) + '\n')
    print(result)
        
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
    try:
        csp, app_vars = schedule_model(a,r,s)
        solver = BT(csp)
        print("=======================================================")
        print("using GAC")
        solver.bt_search(prop_GAC)
        print_soln(app_vars)  
        return True
    except AttributeError:
        print('No Solution; insufficient resources and/or unviable staff hours')    
        return False