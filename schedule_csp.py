from cspbase import *
import itertools

'''
Input: 

schedule = A list of 7 lists to represent each day in a week. Each nested list will
contain 24 lists as elements to represent each hour of a day. Each of these 24 list
elements will have 1 of 2 values:

1 - empty = there is no task that needs to be scheduled for this time
2 - string = the string representation of the type of position needed for this hour

employees = a list of Employee objects that specify details like when the employee is
available, their position and min/max hours needed

Variables:
Each task element that needs to be scheduled will be a variable and each variable's domain
will have all workers who are able to do the task and are listed as available during that time

Constraints:

'''
class Employee:
    
    def __init__(self, name, position, times, minh, maxh):
        self.name = name
        self.pos = position
        self.times = times
        self.minh = minh
        self.maxh = maxh
        
        
def csp_setup(name, schedule, employees):
    csp = CSP(name)
    v_sched = []
    for day in schedule:
        v_day = []
        for hour in day:
            if len(hour) > 0:  # not a blank spot
                task = hour[0] # position required for task
                time = hour[1] # time of task
                v = Variable(task)
                for e in employees:
                    if time in e.times:
                        v.add_domain_values(e)
                csp.add_var(v) 
                v_day.append(v)
            else:
                v_day.append([])
        v_sched.append(v_day)
    return csp, v_sched

def min_constraints(csp):
    employees = csp.get_all_vars()
    #for i in 

def schedule_model(schedule, employees):
    csp, v_sched = csp_setup('schedule', schedule, employees)