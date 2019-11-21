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

"""
This module defines a loop to evaluate a scheduler in a different thread
"""

__license__= "Cecill-C"
__revision__=" $Id: loop.py 2450 2010-05-12 17:50:05Z chopard $ "

from time import sleep
from threading import Thread

class Loop (object) :
	"""Create a thread to evaluate a scheduler.
	"""
	def __init__ (self, scheduler, post_step_func = None, init_func = None) :
		"""Constructor
		
		.. warning:: for this object to works fine, especially with `reinit
		             method, tasks must be registered in the scheduler prior
		             to construct this object
		
		:Parameters:
		 - `scheduler` (Scheduler) - a scheduler to manage each step
		 - `post_step_func` (function) - a function that take no arguments and
		                                 will be called after each step
		 - `init_func` (function) - a function that take no arguments and will
		       be called at each reinitialisation (including this constructor)
		"""
		self._scheduler = scheduler
		self._post_step_func = [] if post_step_func is None \
		                          else [post_step_func]
		self._init_func = [] if init_func is None else [init_func]
		self._end_func = None
		self._running = False
		self._step_in_progress = False
		self._thread = None
		
		#register initial state of the scheduler
		if self._scheduler:
			self._initial_state = tuple(self._scheduler._tasks) #TODO hack pabo
		else:
			self._initial_state = tuple() #TODO hack pabo
		
		#initialise iterator
		self.reinit()
	
	###############################################
	#
	#    accessors
	#
	###############################################
	def running (self) :
		"""Tell wether the loop is currently running.
		"""
		return self._running
	
	def current_step (self) :
		"""Current step reached by the scheduler.
		"""
		return self._scheduler.current_cycle()
	
	def add_init_processing (self, func) :
		if self._init_func is None :
			self._init_func = [func]
		else :
			self._init_func.append(func)
	
	def reinit (self) :
		"""Restart scheduler from 0
		"""
		if self.running() :
			self.pause()
		
		sch = self._scheduler
		if sch is not None :
			sch._tasks = list(self._initial_state) #TODO hack pabo
			sch._current_cycle = 0 #TODO hack pabo
			self._gen = sch.run()
		
		for init_func in self._init_func :
			init_func()
	
	def _step (self) :
		"""Internal function that actually perform one step of the scheduler
		"""
		next_cycle = self._gen.next()
		self._post_step_processing()
		return next_cycle
	
	def add_post_step_processing(self,func):
		if self._post_step_func is None :
			self._post_step_func = [func]
		else : self._post_step_func.append(func)
	
	def _post_step_processing(self):
		if self._post_step_func is not None :
			for post_func in self._post_step_func:
				post_func()
	
	def step (self) :
		"""Perform one step of the scheduler in the current thread
		"""
		#test for multiple call to this function (multithreading)
		if self._step_in_progress :
			return
		
		#test for call to this function while play is already activated
		if self.running() :
			self.pause()
		
		#perform step
		self._step_in_progress = True
		ret = self._step()
		self._step_in_progress = False
		return ret
	
	def _loop (self) :
		"""Internal function that advance step by step
		as long as running is True.
		"""
		while True :
			if not self._running :
				return
			self._step()
			sleep(0.01)
	
	def play (self) :
		"""Create a thread and evaluate the scheduler infinitely
		"""
		self._running = True
		self._thread = Thread(None,self._loop)
		self._thread.start()
	
	def pause (self) :
		"""Pause the current thread
		
		Wait for the current step to be finished before exiting the thread.
		"""
		#stop thread
		self._running = False
		
		#kill thread properly
		if self._thread is not None :
			while self._thread.isAlive() :
				sleep(0.01)
			self._thread = None






