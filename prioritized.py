import time as timer
from single_agent_planner import compute_heuristics, a_star, get_sum_of_cost


class PrioritizedPlanningSolver(object):
    """A planner that plans for each robot sequentially."""

    def __init__(self, my_map, starts, goals):
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """

        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)

        self.CPU_time = 0

        # compute heuristics for the low-level search
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

    def find_solution(self):
        """ Finds paths for all agents from their start locations to their goal locations."""
        start_time = timer.time()
        result = []
        constraints = [
            # {'agent':1,
            #  'loc':[(1,4)],
            #  'timestep':3}
            # # 1.2
            # {'agent':0,
            #  'loc':[(1,5)],
            #  'timestep':4}
            
            # #1.3
            # {'agent':1,
            #  'loc':[(1,2),(1,3)],
            #  'timestep':1}
            
            # #1.4
            #  {'agent': 0, 
            #   'loc': [(1, 5)], 
            #   'timestep': 10
            #   }
            
            # 1.5
            # {'agent':1,
            #  'loc':[(1,2)],
            #  'timestep':1
            # },
            # {'agent':1,
            #  'loc':[(1,3)],
            #  'timestep':2
            # },
            # {'agent':1,
            #  'loc':[(1,3),(1,2)],
            #  'timestep':2
            # },
            # {'agent':1,
            #  'loc':[(1,3),(1,4)],
            #  'timestep':2
            # },
            
            #2.4
            # {'agent':1,
            #  'loc':[(1,1)],
            #  'timestep':1
            # },
            # {'agent':1,
            #  'loc':[(1,2)],
            #  'timestep':2
            # },
            # {'agent':1,
            #  'loc':[(1,3)],
            #  'timestep':3
            # },
            # {'agent':1,
            #  'loc':[(1,2),(1,1)],
            #  'timestep':2
            # },
            # {'agent':1,
            #  'loc':[(1,3),(1,2)],
            #  'timestep':3
            # },
            # {'agent':1,
            #  'loc':[(1,3),(1,4)],
            #  'timestep':3
            # },
            # {'agent':1,
            #  'loc':[(1,3),(2,3)],
            #  'timestep':3
            # },
            
            
            # {'agent':0,
            #  'loc':[(1,2)],
            #  'timestep':1
            # },
            # {'agent':0,
            #  'loc':[(1,3)],
            #  'timestep':2
            # },
            # {'agent':0,
            #  'loc':[(1,2),(1,1)],
            #  'timestep':1
            # },
            # {'agent':0,
            #  'loc':[(1,3),(1,2)],
            #  'timestep':2
            # },
            # {'agent':0,
            #  'loc':[(1,3),(1,4)],
            #  'timestep':2
            # },
            # {'agent':0,
            #  'loc':[(1,3),(2,3)],
            #  'timestep':2
            # },
            
          
        ]
        for i in range(self.num_of_agents):  # Find path for each agent
            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i],
                          i, constraints)
            if path is None:
                raise BaseException('No solutions')
            result.append(path)
                             
            ##############################
            # Task 2: Add constraints here
            #         Useful variables:
            #            * path contains the solution path of the current (i'th) agent, e.g., [(1,1),(1,2),(1,3)]
            #            * self.num_of_agents has the number of total agents
            #            * constraints: array of constraints to consider for future A* searches
            # upperbound = len(result[0])
            #2.1
            for j in range(i+1,self.num_of_agents):
                for l in range(len(path)):
                    constraints.append({'agent':j,
                                        'loc':[path[l]],
                                        'timestep':l})
            # 2.2                 
                    constraints.append({'agent':i+1,
                                        'loc':[path[l],path[l-1]],
                                        'timestep':l})
            # 2.3   
                #2.4
                upperbound = 3
                while True:
                    next_path =a_star(self.my_map, self.starts[j], self.goals[j], self.heuristics[j], 
                                      j, constraints)
                    if path[-1] in next_path:
                        #2.4
                        if len(next_path) < upperbound:
                            constraints.append({'agent':j,
                                                'loc':[path[-2]],
                                                'timestep':next_path.index(path[-1])})  
                            constraints.append({'agent':j,
                                                'loc':[path[-1]],
                                                'timestep':next_path.index(path[-1])})
                        else:
                            raise BaseException('No solutions')
                        
                    else:
                        break
                    
            

        self.CPU_time = timer.time() - start_time

        print("\n Found a solution! \n")
        print("CPU time (s):    {:.2f}".format(self.CPU_time))
        print("Sum of costs:    {}".format(get_sum_of_cost(result)))
        print(result)
        return result
