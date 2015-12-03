from cspbase import *
from propagators import *
import itertools

'''
Input: 

schedule = A list of all tasks that need to be completed. Each element contains a time duration
for the task and the position required for someone to complete the task

employees = a list of Employee objects that specify details like when the employee is
available, their position and min/max hours needed

Variables:

Constraints:

'''
class Appointment:

    def __init__(self, starttime, endtime, procedure):
        self.starttime = starttime
        self.endtime = endtime
        self.procedure = procedure # a list of procedures

class Procedure:

    def __init(self, procedure_name, actions ):
        self.name = procedure_name
        self.actions = actions


class Resource:


class Employee:
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
        



def csp_setup(name, tasks, employees):
    csp = CSP(name)
    task_vars = []
    for t in tasks:
        domain = [1, 0]     # 1 = keep the task, 0 = don't keep the task
        #for e in employees:
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


def schedule_model(tasks, employees):
    csp, task_vars = csp_setup('schedule', tasks, employees)
    overlap_constraints(csp, task_vars)
    return csp, task_vars

def add_position_contraints(csp, employees):
    ''' Add contraints that force employees to work together if they are
        under a certain level of power (i.e. trainees need experienced workers
    '''

def add_role_count_contraints(csp, employees):
    '''Add contraints for the number of employees at each level of experience
        i.e. cannot have all janitors scheduled with no doctors/nurses
    '''

def add_hour_contraints(csp, employees):
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