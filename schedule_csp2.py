from cspbase import *
from propagators import *
import itertools

'''
Input: 

schedule = A list of all tasks that need to be completed. Each element contains a time duration
for the task and the position required for someone to complete the task

staff = a list of Employee objects that specify details like when the employee is
available, their position and min/max hours needed

Variables:

Constraints:

------------------
Example:

# list of appointments
Appointments = [apt1, apt2, apt3, apt4]

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

Constraints
    #TODO

Scheduling:
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
            procedure: a list of procedures involved in this apointment

        An appointment can be started and completed at any time between
        starttime and endtime. However, if the appointment cannot be completed
        by endtime, we must rebook the appointment.
    '''
    def __init__(self, start_time, end_time, procedures):
        self.start_time = start_time
        self.end_time = end_time
        self.procedures = procedures # a list of procedures

    def get_total_duration(self):
        '''return this apopintments duration'''
        total_duration = 0
        for proc in self.procedures:
            total_duration += proc.duration

        return total_duration


    def can_be_completed(self, time):
        '''Returns true if appointment can be completed at time'''
        if (time >= self.start_time) and (self.get_total_duration() + time <= self.end_time):
            return True
        return False

class Procedure:
    '''A procedure has the following attributes
            name: string - the name of the procedure
            actions: a list of tuples ('name','duration'). The first element
                    specifies the name of the action, the second is its duration
            pos_reqs: if empty, any staff member can perform this procedure, otherwise
                    only the staff members with positions listed can perform this procedure
            resources: the required resources to complete this procedure
            inprogress: true if procedure is being performed (resources in use), false otherwise
    '''
    def __init(self, procedure_name, duration, staff_reqs, resources ):
        self.name = procedure_name
        self.duration = duration
        self.staff_reqs = staff_reqs
        self.resources = resources
        self.inprogress = False

    def end_procedure(self):
        '''This method must be run at the end of a procedure to free resources'''
        self.inprogress = False
        for resource in self.resources:
            resource.free()



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
        self.qty_used = 0 # none used when initialized

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
    def __init__(self, name, position, times, minh, maxh):
        self.name = name
        self.pos = position
        self.times = times  # list of nums representing hours
        self.minh = minh
        self.maxh = maxh
        
    def get_maxh(self):
        return self.maxh
    
    def get_minh(self):
        return self.minh    

    def get_name(self):
        return self.name

    def get_position(self):
        return self.pos

#class Task:
    #def __init__(self, position, time):
        #self.pos = position
        #self.time = time    # list/tuple of 2 elements = start and and time
        
    #def get_time(self):
        #return self.time
    
    #def get_pos(self):
        #return self.pos
        



def csp_setup(name, tasks, staff):
    csp = CSP(name)
    task_vars = []
    for t in tasks:
        domain = [1, 0]     # 1 = keep the task, 0 = don't keep the task
        #for e in staff:
            #if t.pos == e.pos and t.time in e.times:
                #domain.append(e)
        v = Variable(str(t), t)
        v.add_domain_values(domain)
        csp.add_var(v)
        task_vars.append(v)
        
    return csp, task_vars

def times_intersect(t1, t2):
    times = t1.time + t2.time
    times.sort()
    if times[:2] != t1.time and times[:2] != t2.time:
        return True
    return False

def overlap_constraints(csp, tasks):
    ''' '''
    for i in tasks:
        for j in tasks:
            if i != j and times_intersect(i, j):
                name = str(i) + ', ' + str(j)
                vals = [(0,0),(1,0),(0,1)]         # can't have both tasks scheduled
                c = Constraint(name, [i,j])
                c.add_satisfying_tuples(vals)    
                csp.add_constraint(c)                  


def schedule_model(tasks, staff):
    csp, task_vars = csp_setup('schedule', tasks, staff)
    overlap_constraints(csp, task_vars)
    return csp, task_vars



""" Constraints
    1. Appointments cannot overlap
    2. If appointment requires staff
"""
def add_position_contraints(csp, staff):
    ''' Add contraints that force staff to work together if they are
        under a certain level of power (i.e. trainees need experienced workers
    '''

def add_role_count_contraints(csp, staff):
    '''Add contraints for the number of staff at each level of experience
        i.e. cannot have all janitors scheduled with no doctors/nurses
    '''

def add_hour_contraints(csp, staff):
    '''Add contraints for minimum and maximum number of hours that
        an employee can work
    '''


def print_soln(l):
    result = []
    for i in l:
        result.append(i.get_assigned_value())
    print(str(result))

def solve_schedule(t,e):
    csp, var_array = schedule_model(t,e)
    solver = BT(csp)
    print("=======================================================")
    print("GAC")
    solver.bt_search(prop_GAC)
    print("Solution")
    print_soln(var_array)  
    
    
t = [[1,3],[2,4],[4,5],[5,6]]
t = [[1,6],[2,4],[3,5],[4,6]]
e = []
solve_schedule(t,e)