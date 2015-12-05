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
        self.positions = positions
        
class Resource:
    '''A resource has the following attributes:
            resource_name: the name of the resource (a string)
            qty_total: the total number of this resource available
            qty_used: the number of this resource being used

        If qty_used == qty_total then the resource is not available
    '''
    def __init__(self, resource_name, qty_total):
        self.resource_name = resource_name
        self.qty_total = qty_total
        #self.qty_used = 0 # none used when initialized

    def is_available(self):
        if (self.qty_used < self.qty_total):
            return True
        return False

    def set_qty_total(self,qty):
        self.qty_total = qty

    def use(self):
        '''Uses a resource. Returns True and increments qty_used if available. Returns False if
            resource is unavailable (qty_used == qty_total)
        '''
        if self.qty_used < self.qty_total:
            self.qty_used += 1
            return True
        else:
            return False

    def free(self):
        '''Free a resource once you are done using'''
        self.qty_used -= 1

        if self.qty_used < 0:
            qty_used = 0

class Staff:
    def __init__(self, name, position, minh, maxh):
        self.name = name
        self.pos = position
        self.minh = minh
        self.maxh = maxh

def csp_setup(name, app, res, staff):
    csp = CSP(name)
    app_vars = copy.deepcopy(app) # this will be used for printing final solution
    res_vars = []   # easier to also keep separate copy of these vars for making constraints
    staff_vars = []
    res_count = 1   # this and staff_count are just for naming the variables
    staff_count = 1
    
    for a in range(len(app)):
        
        r_list = []
        for r in app[a].resources:
            v = Variable('resource'+str(res_count))
            v.add_domain_values(res)
            csp.add_var(v)
            res_vars.append(v)
            res_count+=1
        app_vars[a].resources = r_list
        
        s_list = []
        for s in app[a].positions:
            v = Variable('staff'+str(staff_count))
            v.add_domain_values(staff)
            csp.add_var(v)
            staff_vars.append(v)
            staff_count+=1            
        app_vars[a].positions = s_list
        
    return csp, app_vars, res_vars, staff_vars


def schedule_model(a,r,s):
    csp, app_vars, res_vars, staff_vars = csp_setup('schedule',a,r,s)
    overlaps = get_overlapping_appointments(app_vars)
    add_overlapping_staff_constraints(csp, overlaps, s)
    add_correct_staff_constraints(csp, a, app_vars, s)
    #overlap_constraints(csp, task_vars)
    return csp, app_vars

def add_overlapping_staff_constraints(csp, overlaps, staff_list):
    '''Staff members should not be working on more than one appointment at a time. '''
    for i in overlaps:
        if len(i) > 1:  # overlaps found
            c = Constraint('overlap_staff', i)
            sat = list(itertools.permutations(staff_list, len(i)))
            c.add_satisfying_tuples(sat)
            
def add_correct_staff_constraints(csp, app_list, app_vars, staff_list):
    '''Only staff members with the correct position can cover each appointment. '''
    for i in range(len(app_list)):
        p = app_list[i].positions
        v = app_vars[i]
        s = []
        for j in staff_list:
            if j.pos in p:
                s.append(j)
        c = Constraint('correct_staff_position', v)
        c.add_satisfying_tuples(s)        

def add_resource_constraints(csp,resources):
    # generate satisfying tuples which are
    # if appointments at the same time, do not use more qty than we have
    sat_tuples = []

    overlapping_appointments = []

    #for each apponitment in a set of overlapping appointments
        # get a count of resources
        # check of qty is less than max for each resource

def get_overlapping_appointments(app_vars):
    day = [[] for i in range(0,24)] # create a list of 24 empty lists, each representing an hour of the day

    for av in app_vars:
        for x in range(av.start_time, av.end_time):
            day[x].append(av)

    overlaps = [s for s in day if len(s)>1]

    return overlaps

def print_soln(l):
    result = []
    for i in l:
        result.append(i.get_assigned_value())
    print(str(result))

def solve_schedule(a,r,s):
    csp, app_vars = schedule_model(a,r,s)
    solver = BT(csp)
    print("=======================================================")
    print("GAC")
    solver.bt_search(prop_GAC)
    print("Solution")
    #print_soln(app_vars)  
    
    
#appointments
a1 = Appointment(1, 3, ['needle', 'stethoscope', 'swab'], ['nurse', 'doctor'])
a2 = Appointment(3, 4, ['needle', 'thermometer'], ['nurse'])
a3 = Appointment(5, 7, ['needle', 'otoscope', 'bp_device', 'bandage'], ['doctor'])
a4 = Appointment(2, 5, ['thermometer'], [])
a5 = Appointment (6, 8, ['otoscope', 'stethoscope', 'swab'], ['nurse'])
a = [a1,a2,a3]
a2 = [a1,a2,a3,a4,a5]
x = get_overlapping_appointments(a2)

for t in x:

    print("Appointment conflicts:")
    for y in t:
        print("start:" + str(y.start_time) + " end:" + str(y.end_time) + " resources:" + str(y.resources))

##procedures
#p1 = Procedure('injection', [('swab', 1), ('inject', 2)], ['nurse'], ['needle', 'fluid'])
#p2 = Procedure('blood pressure', [('inflate', 3), ('measure', 1)], ['nurse'], ['bp_device'])
#p3 = Procedure('heartbeat', [('listen', 2)], ['doctor'], ['stethoscope'])
#p = [p1,p2,p3]

#resources

r1 = Resource('needle', 2)
r2 = Resource('bp_device', 1)
r3 = Resource('stethoscope', 1)
r4 = Resource('thermometer', 1)
r5 = Resource('tongue depressor', 1)
r6 = Resource('otoscope', 1)
r7 = Resource('swab', 1)
r8 = Resource('bandage', 1)
r9 = Resource('gauze', 1)
r = [r1,r2,r3,r4,r5,r6,r7,r8,r9]

#staff
s1 = Staff('N1', 'nurse', 2, 4)
s2 = Staff('D1', 'doctor', 1, 5)
s = [s1,s2]

#solve_schedule(a,r,s)