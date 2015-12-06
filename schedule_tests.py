from schedule_csp import *

def case1():
    # --- General case; has solution ----
    #resources
    
    #appointments
    a1 = Appointment(1, 3, ['needle', 'stethoscope', 'swab'], ['nurse'])
    a2 = Appointment(3, 4, ['needle', 'thermometer'], ['nurse', 'doctor'])
    a3 = Appointment(5, 7, ['needle', 'otoscope', 'bp_device'], ['nurse'])
    a4 = Appointment(2, 5, ['thermometer'], ['doctor'])
    a5 = Appointment (6, 8, ['otoscope', 'stethoscope', 'swab'], ['nurse', 'doctor'])
    a = [a1,a2,a3,a4,a5]
    
    #resources
    
    r1 = Resource('needle', 3, False)
    r2 = Resource('bp_device', 1, True)
    r3 = Resource('stethoscope', 1, True)
    r4 = Resource('thermometer', 3, True)
    r5 = Resource('otoscope', 2, True)
    r6 = Resource('swab', 2, False)
    r7 = Resource('bandage', 1, False)
    r = [r1,r2,r3,r4,r5,r6,r7]
    
    #staff
    s1 = Staff('Jean', 'nurse', 2, 4)
    s2 = Staff('Diana', 'doctor', 1, 3)
    s3 = Staff('Alex', 'nurse', 1, 3)
    s4 = Staff('Mark', 'doctor', 1, 2)
    s = [s1,s2,s3,s4]
    
    return solve_schedule(a,r,s)


def case2():
    # --- General case; no solution; staff min time ----
    
    #appointments
    a1 = Appointment(1, 3, ['needle', 'stethoscope', 'swab'], ['nurse'])
    a2 = Appointment(3, 4, ['needle', 'thermometer'], ['nurse', 'doctor'])
    a3 = Appointment(5, 7, ['needle', 'otoscope', 'bp_device'], ['nurse'])
    a4 = Appointment(2, 5, ['thermometer'], ['doctor'])
    a5 = Appointment (6, 8, ['otoscope', 'stethoscope', 'swab'], ['nurse', 'doctor'])
    a = [a1,a2,a3,a4,a5]
    
    #resources
    r1 = Resource('needle', 3, False)
    r2 = Resource('bp_device', 1, True)
    r3 = Resource('stethoscope', 1, True)
    r4 = Resource('thermometer', 3, True)
    r5 = Resource('otoscope', 2, True)
    r6 = Resource('swab', 2, False)
    r7 = Resource('bandage', 1, False)
    r = [r1,r2,r3,r4,r5,r6,r7]
    
    #staff
    s1 = Staff('Jean', 'nurse', 2, 5)
    s2 = Staff('Diana', 'doctor', 3, 4)
    s3 = Staff('Alex', 'nurse', 2, 5)
    s4 = Staff('Mark', 'doctor', 1, 2)
    s = [s1,s2,s3,s4]
    
    return solve_schedule(a,r,s)
    

def case3a():
    # --- no solution; insufficient nonreusable resources ----
    #appointments
    a1 = Appointment(1, 3, ['needle', 'stethoscope', 'swab'], ['nurse'])
    a2 = Appointment(3, 4, ['needle', 'stethoscope'], ['nurse', 'doctor'])
    a = [a1,a2]
    
    #resources
    r1 = Resource('needle', 1, False)
    r2 = Resource('bp_device', 1, True)
    r3 = Resource('stethoscope', 2, True)
    r4 = Resource('swab', 3, False)
    r = [r1,r2,r3,r4]
    
    #staff
    s1 = Staff('Jean', 'nurse', 1, 5)
    s2 = Staff('Diana', 'doctor', 1, 4)
    s = [s1,s2]
    
    return solve_schedule(a,r,s)
    
def case3b():
    # --- solution; sufficient nonreusable resources ----
    #appointments
    a1 = Appointment(1, 3, ['needle', 'stethoscope', 'swab'], ['nurse'])
    a2 = Appointment(3, 4, ['needle', 'stethoscope'], ['nurse', 'doctor'])
    a = [a1,a2]
    
    #resources
    r1 = Resource('needle', 2, False)
    r2 = Resource('bp_device', 1, True)
    r3 = Resource('stethoscope', 2, True)
    r4 = Resource('swab', 3, False)
    r = [r1,r2,r3,r4]
    
    #staff
    s1 = Staff('Jean', 'nurse', 1, 5)
    s2 = Staff('Diana', 'doctor', 1, 4)
    s = [s1,s2]
    
    return solve_schedule(a,r,s)
    
def case4a():
    # --- no solution; insufficient reusable resources ----
    #appointments
    a1 = Appointment(1, 3, ['needle', 'stethoscope', 'swab'], ['nurse'])
    a2 = Appointment(2, 4, ['needle', 'stethoscope'], ['nurse', 'doctor'])
    a = [a1,a2]
    
    #resources
    r1 = Resource('needle', 3, False)
    r2 = Resource('bp_device', 1, True)
    r3 = Resource('stethoscope', 1, True)
    r4 = Resource('swab', 3, False)
    r = [r1,r2,r3,r4]
    
    #staff
    s1 = Staff('Jean', 'nurse', 1, 5)
    s2 = Staff('Diana', 'doctor', 1, 4)
    s = [s1,s2]
    
    return solve_schedule(a,r,s)
    
def case4b():
    # --- solution; sufficient reusable resources ----
    #appointments
    a1 = Appointment(1, 3, ['needle', 'stethoscope', 'swab'], ['nurse'])
    a2 = Appointment(2, 4, ['needle', 'stethoscope'], ['nurse', 'doctor'])
    a = [a1,a2]
    
    #resources
    r1 = Resource('needle', 3, False)
    r2 = Resource('bp_device', 1, True)
    r3 = Resource('stethoscope', 3, True)
    r4 = Resource('swab', 3, False)
    r = [r1,r2,r3,r4]
    
    #staff
    s1 = Staff('Jean', 'nurse', 1, 5)
    s2 = Staff('Diana', 'doctor', 1, 4)
    s = [s1,s2]
    
    return solve_schedule(a,r,s)
    
def case5a():
    # --- no solution; staff min appointments ----
    #appointments
    a1 = Appointment(1, 3, ['needle', 'stethoscope', 'swab'], ['nurse'])
    a2 = Appointment(2, 4, ['needle', 'stethoscope'], ['nurse', 'doctor'])
    a = [a1,a2]
    
    #resources
    r1 = Resource('needle', 3, False)
    r2 = Resource('bp_device', 3, True)
    r3 = Resource('stethoscope', 3, True)
    r4 = Resource('swab', 3, False)
    r = [r1,r2,r3,r4]
    
    #staff
    s1 = Staff('Jean', 'nurse', 2, 5)
    s2 = Staff('Diana', 'doctor', 1, 4)
    s = [s1,s2]
    
    return solve_schedule(a,r,s)
    
def case5b():
    # --- solution; staff min appointments ----
    #appointments
    a1 = Appointment(1, 3, ['needle', 'stethoscope', 'swab'], ['nurse'])
    a2 = Appointment(2, 4, ['needle', 'stethoscope'], ['nurse', 'doctor'])
    a = [a1,a2]
    
    #resources
    r1 = Resource('needle', 3, False)
    r2 = Resource('bp_device', 3, True)
    r3 = Resource('stethoscope', 3, True)
    r4 = Resource('swab', 3, False)
    r = [r1,r2,r3,r4]
    
    #staff
    s1 = Staff('Jean', 'nurse', 1, 5)
    s2 = Staff('Diana', 'doctor', 1, 4)
    s = [s1,s2]
    
    return solve_schedule(a,r,s)
    
    
def case6a():
    # --- no solution; staff max appointments ----
    #appointments
    a1 = Appointment(1, 2, ['needle', 'stethoscope', 'swab'], ['nurse'])
    a2 = Appointment(2, 3, ['needle', 'bp_device'], ['nurse', 'doctor'])
    a3 = Appointment(3, 4, ['needle', 'stethoscope', 'bp_device'], ['nurse'])
    a4 = Appointment(4, 5, ['swab'], ['doctor'])
    a5 = Appointment(5, 6, ['stethoscope'], ['nurse', 'doctor'])
    a = [a1,a2,a3,a4,a5]
    
    #resources
    r1 = Resource('needle', 5, False)
    r2 = Resource('bp_device', 5, True)
    r3 = Resource('stethoscope', 5, True)
    r4 = Resource('swab', 5, False)
    r = [r1,r2,r3,r4]
    
    #staff
    s1 = Staff('Jean', 'nurse', 1, 2)
    s2 = Staff('Diana', 'doctor', 1, 2)
    s = [s1,s2]
    
    return solve_schedule(a,r,s)
    
def case6b():
    # --- solution; staff max appointments ----
    #appointments
    a1 = Appointment(1, 2, ['needle', 'stethoscope', 'swab'], ['nurse'])
    a2 = Appointment(2, 3, ['needle', 'bp_device'], ['nurse', 'doctor'])
    a3 = Appointment(3, 4, ['needle', 'stethoscope', 'bp_device'], ['nurse'])
    a4 = Appointment(4, 5, ['swab'], ['doctor'])
    a5 = Appointment(5, 6, ['stethoscope'], ['nurse', 'doctor'])
    a = [a1,a2,a3,a4,a5]
    
    #resources
    r1 = Resource('needle', 5, False)
    r2 = Resource('bp_device', 5, True)
    r3 = Resource('stethoscope', 5, True)
    r4 = Resource('swab', 5, False)
    r = [r1,r2,r3,r4]
    
    #staff
    s1 = Staff('Jean', 'nurse', 1, 3)
    s2 = Staff('Diana', 'doctor', 1, 2)
    s = [s1,s2]
    
    return solve_schedule(a,r,s)
    
def case7a():
    # --- no solution; no staff available for overlapping appointments ----
    #appointments
    a1 = Appointment(1, 3, ['needle', 'stethoscope', 'swab'], ['nurse'])
    a2 = Appointment(2, 4, ['needle', 'stethoscope'], ['nurse'])
    a3 = Appointment(4, 5, ['needle', 'stethoscope', 'bp_device'], ['doctor'])
    a = [a1,a2,a3]
    
    #resources
    r1 = Resource('needle', 3, False)
    r2 = Resource('bp_device', 3, True)
    r3 = Resource('stethoscope', 3, True)
    r4 = Resource('swab', 3, False)
    r = [r1,r2,r3,r4]
    
    #staff
    s1 = Staff('Jean', 'nurse', 2, 5)
    s2 = Staff('Diana', 'doctor', 1, 4)
    s = [s1,s2]
    
    return solve_schedule(a,r,s)
    
def case7b():
    # --- no solution; no staff available for overlapping appointments ----
    #appointments
    a1 = Appointment(1, 3, ['needle', 'stethoscope', 'swab'], ['nurse'])
    a2 = Appointment(2, 4, ['needle', 'stethoscope'], ['nurse', 'doctor'])
    a3 = Appointment(4, 5, ['needle', 'stethoscope', 'bp_device'], ['doctor'])
    a = [a1,a2,a3]
    
    #resources
    r1 = Resource('needle', 3, False)
    r2 = Resource('bp_device', 3, True)
    r3 = Resource('stethoscope', 3, True)
    r4 = Resource('swab', 3, False)
    r = [r1,r2,r3,r4]
    
    #staff
    s1 = Staff('Jean', 'nurse', 1, 5)
    s2 = Staff('Diana', 'doctor', 1, 4)
    s = [s1,s2]
    
    return solve_schedule(a,r,s)
    
def case8a():
    # --- no solution; no staff available for required position ----
    #appointments
    a1 = Appointment(1, 3, ['needle', 'stethoscope', 'swab'], ['nurse'])
    a2 = Appointment(2, 4, ['needle', 'stethoscope'], ['nurse'])
    a3 = Appointment(4, 5, ['needle', 'stethoscope', 'bp_device'], ['doctor'])
    a = [a1,a2,a3]
    
    #resources
    r1 = Resource('needle', 3, False)
    r2 = Resource('bp_device', 3, True)
    r3 = Resource('stethoscope', 3, True)
    r4 = Resource('swab', 3, False)
    r = [r1,r2,r3,r4]
    
    #staff
    s1 = Staff('Jean', 'nurse', 2, 5)
    s2 = Staff('Diana', 'nurse', 1, 4)
    s = [s1,s2]
    
    return solve_schedule(a,r,s)

def case8b():
    # --- solution; staff available for required position ----
    #appointments
    a1 = Appointment(1, 3, ['needle', 'stethoscope', 'swab'], ['nurse'])
    a2 = Appointment(2, 4, ['needle', 'stethoscope'], ['nurse'])
    a3 = Appointment(4, 5, ['needle', 'stethoscope', 'bp_device'], ['doctor'])
    a = [a1,a2,a3]
    
    #resources
    r1 = Resource('needle', 3, False)
    r2 = Resource('bp_device', 3, True)
    r3 = Resource('stethoscope', 3, True)
    r4 = Resource('swab', 3, False)
    r = [r1,r2,r3,r4]
    
    #staff
    s1 = Staff('Jean', 'nurse', 1, 5)
    s2 = Staff('Diana', 'nurse', 1, 4)
    s3 = Staff('David', 'doctor', 1, 4)
    s = [s1,s2,s3]
    
    return solve_schedule(a,r,s)
    

if __name__ == "__main__":
    
    # ---- test cases with more variables but takes longer time to complete (~2 mins each) ---
    tests_long = []
    #tests_long = [case1(), not case2()]     # *** comment out this line to skip the long tests
    
    # shorter test cases for each set of constraints
    tests_short = [not case3a(), case3b(), not case4a(), case4b(), not case5a(), case5b(), not case6a(), case6b(), not case7a(), case7b(), not case8a(), case8b()] + tests_long
    
    passall = 0
    for i in tests_short:
        if i == False:
            passall += 1
        
    if passall == 0:
        print('All tests pass!')
    else:
        print('failed ' + str(passall) + ' tests')