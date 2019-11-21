# -*- python -*-
#
#       scheduler: simple scheduling of tasks
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#                       Christophe Pradal <christophe.pradal@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""This module defines the base class Scheduler to list and evaluate tasks."""

__license__= "Cecill-C"
__revision__=" $Id: scheduler.py 2450 2010-05-12 17:50:05Z chopard $ "

from heapq import heappush,heappop

class Scheduler (object) :
    """Call a set of tasks at regular time interval.
    """
    def __init__ (self) :
        """Initialise the Scheduler.
        """
        #current step of evaluation
        self._current_cycle = 0
        
        #heapqueue of tasks
        self._tasks = []
    
    ###############################################
    #
    #    accessors
    #
    ###############################################
    def tasks (self) :
        """Iterate on all scheduled tasks.
        """
        return (task for cycle,task in self._tasks)
    
    def current_cycle (self) :
        """Retrieve the value of the current cycle
        
        .. warning:: the current cycle has already been evaluated. The next
                     next cycle to be executed is returned by `run`.
        """
        return self._current_cycle
    
    ###############################################
    #
    #    edit
    #
    ###############################################
    def register (self, task, start_time = None) :
        """Register a new task in the scheduler.
        
        task: a Task object
        start_time: ellapsed cycle number before
                    evaluating the task. If None,
                    uses task delay.
        """
        if start_time is None :
            start_time = self._current_cycle + task.delay()
        else :
            assert start_time >= self._current_cycle
        
        heappush(self._tasks, (start_time,task) )
    
    ###############################################
    #
    #    evaluate
    #
    ###############################################
    def run (self) :
        """Evaluate one cycle of the scheduler.
        
        yield the next cycle
        """
        tasks = self._tasks
        while len(tasks) > 0 :
            #retrieve tasks to evaluate at this cycle
            self._current_cycle,task = heappop(tasks)
            task_list = [(task.priority(),task)]
            while len(tasks) > 0 and tasks[0][0] == self._current_cycle :
                cc,task = heappop(tasks)
                task_list.append( (task.priority(),task) )
            
            #sort task by priority
            task_list.sort(reverse = True)
            
            #evaluate
            for priority,task in task_list :
                #evaluate the task
                delay = task.evaluate()
                #reinsert the task in the heapqueue
                if delay is not None :
                    heappush(tasks, (self._current_cycle + delay,task) )
            
            #return
            if len(tasks) > 0 :
                yield tasks[0][0]

