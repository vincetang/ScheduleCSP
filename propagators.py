##Look for #IMPLEMENT tags in this file. These tags indicate what has
##to be implemented to complete the warehouse domain.  

#'''This file will contain different constraint propagators to be used within 
   #bt_search.

   #propagator == a function with the following template
      #propagator(csp, newly_instantiated_variable=None)
           #==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      #csp is a CSP object---the propagator can use this to get access
      #to the variables and constraints of the problem. The assigned variables
      #can be accessed via methods, the values assigned can also be accessed.

      #newly_instaniated_variable is an optional argument.
      #if newly_instantiated_variable is not None:
          #then newly_instantiated_variable is the most
           #recently assigned variable of the search.
      #else:
          #progator is called before any assignments are made
          #in which case it must decide what processing to do
           #prior to any variables being assigned. SEE BELOW

       #The propagator returns True/False and a list of (Variable, Value) pairs.
       #Return is False if a deadend has been detected by the propagator.
       #in this case bt_search will backtrack
       #return is true if we can continue.

      #The list of variable values pairs are all of the values
      #the propagator pruned (using the variable's prune_value method). 
      #bt_search NEEDS to know this in order to correctly restore these 
      #values when it undoes a variable assignment.

      #NOTE propagator SHOULD NOT prune a value that has already been 
      #pruned! Nor should it prune a value twice

      #PROPAGATOR called with newly_instantiated_variable = None
      #PROCESSING REQUIRED:
        #for plain backtracking (where we only check fully instantiated constraints)
        #we do nothing...return true, []

        #for forward checking (where we only check constraints with one remaining variable)
        #we look for unary constraints of the csp (constraints whose scope contains
        #only one variable) and we forward_check these constraints.

        #for gac we establish initial GAC by initializing the GAC queue
        #with all constaints of the csp


      #PROPAGATOR called with newly_instantiated_variable = a variable V
      #PROCESSING REQUIRED:
         #for plain backtracking we check all constraints with V (see csp method
         #get_cons_with_var) that are fully assigned.

         #for forward checking we forward check all constraints with V
         #that have one unassigned variable left

         #for gac we initialize the GAC queue with all constraints containing V.
         
   #'''

#def prop_BT(csp, newVar=None):
    #'''Do plain backtracking propagation. That is, do no 
    #propagation at all. Just check fully instantiated constraints'''
    
    #if not newVar:
        #return True, []
    #for c in csp.get_cons_with_var(newVar):
        #if c.get_n_unasgn() == 0:
            #vals = []
            #vars = c.get_scope()
            #for var in vars:
                #vals.append(var.get_assigned_value())
            #if not c.check(vals):
                #return False, []
    #return True, []

#def FCCheck(C, x):
    ## C is a constraint with all its variables already assigned,
    ## except for variable x
    ## returns True/False, [(var, val), ...]: True if DWO, False if passed
    ## list of var-val pairs of pruned variables

    #prunings = []
    #for d in x.cur_domain():
        #vars = C.get_scope()
        #x_index = vars.index(x)
        #vals = []

        ## build list of values for variables in the constraint
        #for var in vars:
            #vals.append(var.get_assigned_value())

        ## insert d for the value of x
        #vals[x_index] = d

        ## Check constraint satisfaction
        #if not C.check(vals):
            ## prune d from x's domain
            #x.prune_value(d)
            #prunings.append((x,d))
    #if (x.cur_domain_size() == 0):
        ## Entire domain of x pruned, return DWO
        #return True, prunings
    #else:
        ## There is a solution (not DWO)
        #return False, prunings

#def prop_FC(csp, newVar=None):
    #'''Do forward checking. That is check constraints with 
       #only one uninstantiated variable. Remember to keep 
       #track of all pruned variable,value pairs and return '''

    ## we look for unary constraints of the csp (constraints whose scope contains
    ## only one variable) and we forward_check these constraints.
    #DWOOcurred = False
    #prunings = []
    #if newVar == None:
        ## Look for all unary constraints of the csp
        #for c in csp.get_all_cons():
            ##c_scope = c.get_scope()
            #if (c.get_n_unasgn() == 1):
                ## forward check the constraint
                #var = c.get_unasgn_vars()[0]
                #DWOOcurred, pruned = FCCheck(c, var)
                #prunings.extend(pruned)
                #if DWOOcurred:
                    #break
    #else:
        ##  forward check all constraints with newVar
        ##  that have one unassigned variable left
        ## for d in newVar.cur_domain():
        ##     newVar.assign(d)
        #constraints = csp.get_cons_with_var(newVar)
        #for c in constraints:
            #if c.get_n_unasgn() == 1:
                #var = c.get_unasgn_vars()[0]
                #DWOOcurred, pruned = FCCheck(c, var)
                #prunings.extend(pruned)
                #if DWOOcurred:
                    #break
    #if (not DWOOcurred): # all constraints were ok
        #return True, prunings
    #var.restore_curdom()
    #return False, prunings

#def GAC_Enforce(csp, queue):
    #''' GAC_queue contains all constraints one of whose variables
        #had its domain reduced.
        #Returns True/False, [(var, val)...], where True if DWO
        #(False if OK) and list of pruned var-val pairs '''
    #prunings = []
    #while queue:
        #c = queue.pop(0)
        #c_scope = c.get_scope()
        #for v in c_scope:
            #csat_found = False
            #v_index = c_scope.index(v) # index of variable in constraint
            #for d in v.cur_domain():

                ## check for a support for v=d in constraint C
                #if not c.has_support(v, d):
                    ## No assignments of A for all other variables such that c(A U v=d) = True
                    #v.prune_value(d)
                    #prunings.append((v,d))
                    #if (v.cur_domain_size() == 0):
                        #queue = [] # empty queue
                        #return True, prunings # DWO, return immediately
                    #else:
                        ## push all constraints not in GACQueue with V on to the GACQueue
                        #for cons in csp.get_cons_with_var(v):
                            #if cons not in queue:
                                #queue.append(cons)
    #return False, prunings

#def prop_GAC(csp, newVar=None):
    #'''Do GAC propagation. If newVar is None we do initial GAC enforce 
       #processing all constraints. Otherwise we do GAC enforce with
       #constraints containing newVar on GAC Queue'''
    #prunings = []
    ##if new var = None:
    ## for gac we establish initial GAC by initializing the GAC queue
    ## with all constaints of the csp
    #if (newVar == None):
        ## Initialize GAC queue with all constraints since newVar is none
        #gac_queue = csp.get_all_cons()
    #else:
        ## Prune all values of newVar's cur_domain != d
        ##cur_dom = newVar.cur_domain()
        #for d in newVar.cur_domain():
            #if d != newVar.get_assigned_value():
                #newVar.prune_value(d)
                #prunings.append((newVar, d))
        ## put all constraints whose scope contains V in gac_queue
        #gac_queue = csp.get_cons_with_var(newVar)

    #DWO, pruned = GAC_Enforce(csp, gac_queue)
    #prunings.extend(pruned)
    #if not DWO:
        #return True, prunings
    #newVar.restore_curdom()
    #return False, prunings
    
    
# Name:        Justin Djordjevic
# Student#:    997412152

#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one remaining variable)
        we look for unary constraints of the csp (constraints whose scope contains
        only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
         
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
    #IMPLEMENT
    pruned = []
    if not newVar:
        for c in csp.get_all_cons():
            if len(c.get_scope()) == 1:
                v = c.get_scope()[0]
                r, l = fccheck(c, v)
                pruned += l
                if not r:
                    return False, pruned
                
        for c in csp.get_all_cons():
            if c.get_n_unasgn() == 1:
                v = c.get_unasgn_vars()[0]
                r, l = fccheck(c, v)
                pruned += l
                if not r:
                    return False, pruned    
    else:
        for c in csp.get_all_cons():
            if c.get_n_unasgn() == 1 and newVar in c.get_scope():
                v = c.get_unasgn_vars()[0]
                r, l = fccheck(c, v)
                pruned += l
                if not r:
                    return False, pruned
                
    return True, pruned

def fccheck(c, v):
    '''Perform a forward check with Constraint c and Variable v. '''
    pruned = []
    for val in v.cur_domain():
        v.assign(val)
        test = get_vals(c)
        if not c.check(test):
            v.prune_value(val)
            pruned.append((v, val))
        v.unassign()
    if len(v.cur_domain()) == 0:
        return False, pruned
    else:
        return True, pruned
    
def get_vals(c):
    '''Return list of all values for assigned variables in constraint c. 
    (helper method for fccheck). '''
    vals = []
    for v in c.get_scope():
        vals.append(v.get_assigned_value())
    return vals
                

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    #IMPLEMENT
    if not newVar:
        q = csp.get_all_cons().copy()
        r, l = enforce_GAC(q, csp)
    else:
        q = csp.get_all_cons().copy()
        for c in csp.get_all_cons():
            if newVar not in c.get_scope():
                q.remove(c)
        r, l = enforce_GAC(q, csp)
        
    if not r:
        return False, l
    else:
        return True, l
        
def enforce_GAC(q, csp):
    '''Enforce GAC with the variables in csp and using the constraints in list
    q. '''
    pruned = []
    while len(q) > 0:
        c = q.pop()
        for v in c.get_scope():
            for val in v.cur_domain():
                if not c.has_support(v, val):
                    v.prune_value(val)
                    pruned.append((v, val))
                    if len(v.cur_domain()) == 0:
                        return False, pruned
                    else:
                        q += csp.get_cons_with_var(v)
                    
    return True, pruned