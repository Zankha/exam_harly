# -*- coding: utf-8 -*-
import datetime
import time
import threading
import random


class Pump():
	name = None
	priority = 0
	period = 0
	execTime = 0
	last_execTime = 0
	last_deadline = 0
	reset = 0
	def __init__(self, name, period, execTime, output, last_exec, target):
		self.name = name;
		self.period = period;
		self.execTime = execTime;
		self.output = output;
		self.last_execTime = last_exec;
		self.target = target;
		self.reset = execTime;
		
	def run(self):
		self.last_execTime = datetime.datetime.now()
		print(self.name + " : Starting to pump (" + self.last_execTime.strftime("%H:%M:%S") + ") : execution time = " + str(self.execTime))

		while(self.execTime != 0):
	
			self.execTime -= 1
	
			time.sleep(1)
			
			if (self.execTime <= 0):
				self.execTime = self.reset
				if(self.target.storage < self.target.capacity):
					self.target.storage += self.output;
					if(self.target.storage < self.target.capacity):
						self.target.storage = self.target.capacity;
					print(self.name + " : Outputting to tank normally (" + datetime.datetime.now().strftime("%H:%M:%S") + ")")
					return
				if(self.target.storage >= self.target.capacity):
					print(self.name + " : Tank is full, wasting oil (" + datetime.datetime.now().strftime("%H:%M:%S") + ")")
					return
		
class Tank():
	
	storage = 0
	
	def __init__(self, capacity):
		self.capacity = capacity;
		
class Machine():
	name = None
	priority = 0
	period = 0
	execTime = 0
	last_execTime = 0
	reset = 0
	last_deadline = 0
	machineType = None
	def __init__(self, name, period, execTime, output, inpt, last_exec, tank, mType, target):
		self.name = name;
		self.period = period;
		self.execTime = execTime;
		self.output = output;
		self.inpt = inpt;
		self.last_execTime = last_exec;
		self.target = target;
		self.machineType = mType;
		self.tank = tank;
		self.reset = execTime;
		
	def run(self):
		self.last_execTime = datetime.datetime.now()
		
		if(self.tank.storage < self.inpt):
			return
		else:
			print(self.name + " : Starting to process (" + self.last_execTime.strftime("%H:%M:%S") + ") : execution time = " + str(self.execTime))
			self.tank.storage -= self.inpt;
			while(self.execTime != 0):
				self.execTime -= 1
		
				time.sleep(1)
		
				if (self.execTime <= 0):
					self.execTime = self.reset
					self.target.storage += self.output;
					print(self.name + " : Outputting to pile normally (" + datetime.datetime.now().strftime("%H:%M:%S") + ")")
					return
		
		
if __name__ == '__main__':
	
	#initialise
	stop = False
	testTime = datetime.timedelta(minutes=2)
	startTime = datetime.datetime.now()
	print("TIME")
	print(testTime+startTime)
	tank = Tank(capacity = 50)
	tank.storage = 0
	wheelStock = Tank(capacity = 999)
	motorStock = Tank(capacity = 999)
	pump1Prio = -1
	pump2Prio = -1
	motorPrio = -1
	wheelPrio = -1
	last_exec = datetime.datetime.now()
	print('Test')
	pump1 = Pump(name= "Pump 1", period = 5, execTime = 2, output = 10, last_exec=0, target=tank);
	pump2 = Pump(name= "Pump 2", period=15, execTime=3, output=20, last_exec=0, target=tank);
	wheelMachine = Machine(name="Wheel Machine", period=5,execTime=3,output=1,inpt=5,last_exec=0,tank=tank,mType='Wheel',target=wheelStock)
	motorMachine = Machine(name="Motor Machine", period=5,execTime=5,output=1,inpt=25,last_exec=0,tank=tank,mType='Motor',target=motorStock)
	taskList = [pump1, pump2, wheelMachine, motorMachine]
	
	
	while(stop == False):
		print("Tank: " + str(tank.storage) + "/" + str(tank.capacity))
		if(datetime.datetime.now() >= (startTime + testTime)):
			stop = True
		if(tank.storage == 50):
			print("IF test")
			pump1Prio = -1
			pump2Prio = -1
			if(motorStock.storage < wheelStock.storage/4):
				motorPrio = 3
				wheelPrio = 2
			else:
				wheelPrio = 3
				motorPrio = -1
		if(tank.storage == 0):
			pump2Prio = 3
			pump1Prio = -1
			motorPrio = -1
			wheelPrio = 1
		if(0 < tank.storage and tank.storage < 25):
			pump2Prio = 3
			pump1Prio = 2
			wheelPrio = -1
			motorPrio = -1
		if(25 < tank.storage and tank.storage < 50):
			if(motorStock.storage < wheelStock.storage/4):
				pump1Prio = 3
				motorPrio = 2
				wheelPrio = 1
			if(motorStock.storage >= wheelStock.storage/4):
				pump1Prio = 1
				wheelPrio = 3
				motorPrio = -1
				
		pump1.priority = pump1Prio
		pump2.priority = pump2Prio
		wheelMachine.priority = wheelPrio
		motorMachine.priority = motorPrio
		
		execList = []
		for task in taskList:
			if(task.priority == 3):
				execList.append(task)
		for task in taskList:
			if(task.priority == 2):
				execList.append(task)	
		for task in taskList:
			if(task.priority == 1):
				execList.append(task)		
		for task in taskList:
			if(task.priority == 0):
				execList.append(task)		
		for toRun in execList:
			toRun.run()
		
	print("Wheel Stock: " + str(wheelStock.storage) + ". Motor Stock: " + str(motorStock.storage))