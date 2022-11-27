from dataclasses import dataclass
from typing import Optional

from data import DATA

@dataclass
class Task:
  task: int                       # task number
  machines: list[list[int]]       # list of machines and operators that can do the task
  processing_time: int            # time of execution of the task
  start: Optional[int] = None     # start date of the task
  machine: Optional[int] = None   # number of the machine that has been assigned to the task
  operator: Optional[int] = None  # number of the operator that has been assigned to the task

  @staticmethod
  def from_json(i):
    '''retrieves the data from the task'''
    task = DATA['tasks'][i-1]

    return Task(
      task = i,
      machines = {data['machine']: data['operators'] for data in task['machines']},
      processing_time = task['processing_time']
    )

  def to_json(self):
    '''writes the task data in json format'''
    return {
      'task': self.task,
      'start': self.start,
      'machine': self.machine,
      'operator': self.operator
    }
  
  def assign(self, start, machine, operator):
    '''assigns a start of the task, a machine and an operator to the task'''
    self.start = start
    self.machine = machine
    self.operator = operator

  def compatible_machine(self, machines):
    '''return the first machine available in a list of machines'''
    for machine in machines:
      if machine in self.machines:
        return machine
    return None

  def compatible_operator(self, machine, operators):
    '''return the first operatior who is available and who can work on an available machine'''
    for operator in operators:
      if operator in self.machines[machine]:
        return operator
    return None

  def is_active(self, t):
    '''return if this task is working on or not (on the time t)'''
    return self.start is not None and self.start + self.processing_time > t

  def is_done(self, t):
    ''' return if this task is finish or not (on the time t)'''
    return self.start is not None and self.start + self.processing_time <= t
