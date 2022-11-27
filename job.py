from dataclasses import dataclass

from data import DATA
from task import Task

UNIT_PENALTY = DATA['parameters']['costs']['unit_penalty']
TARDINESS = DATA['parameters']['costs']['tardiness']

@dataclass
class Job:
  job: int              # number of job
  sequence: list[Task]  # list of task indices
  release_date: int     # release_date
  due_date: int         # due date
  weight: int           # weight of the job
  current: int = 0      # index of the current task
  
  @staticmethod
  def from_json(i):
    job = DATA['jobs'][i-1]

    return Job(
      job = job['job'],
      sequence = list(map(Task.from_json, job['sequence'])),
      release_date = job['release_date'],
      due_date = job['due_date'],
      weight = job['weight']
    )

  def is_done(self):
    '''return if the job is done or not'''
    return self.current == len(self.sequence)

  def is_available(self, t):
    '''return if the job is in progress or not (on the time t)'''
    return self.release_date <= t and not self.is_done()

  def standby_cost(self, t):
    '''returns if the job is in progress or not'''
    C_min = t + sum([task.processing_time for task in self.sequence[self.current:]])

    dt = 1
    cost = dt

    if C_min > self.due_date:
      cost += dt*TARDINESS
    elif C_min + dt > self.due_date:
      cost += UNIT_PENALTY + dt*TARDINESS

    return self.weight * cost

  def current_task(self):
    '''return the index of the task that must be done or that is running'''
    return self.sequence[self.current]