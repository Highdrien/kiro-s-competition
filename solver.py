from dataclasses import dataclass

from data import DATA
from job import Job


@dataclass
class Solver:
  jobs: list[Job] # list of jobs
  t: int = 0      # time

  def update_jobs(self):
    '''update all jobs'''
    for job in self.jobs:
      if job.is_done():
        continue
      if job.current_task().is_done(self.t):
        job.current += 1

  def get_jobs_by_priority(self):
    '''return the list of available jobs sorted by their estimated cost'''
    available_jobs = filter(lambda job: job.is_available(self.t), self.jobs)
    return sorted(available_jobs, key=lambda job: job.standby_cost(self.t))

  def get_running_tasks(self, jobs):
    '''return all the running tasks'''
    tasks = []

    for job in self.jobs:
      if job.is_done():
        continue
      task = job.current_task()
      if task.is_active(self.t):
        tasks.append(task)
    return tasks
  
  def get_scheduled_tasks(self, jobs):
    '''return the list of tasks that can be started'''
    tasks = list(map(lambda job: job.current_task(), jobs))
    return list(filter(lambda task: not task.is_active(self.t), tasks))

  def get_available_machines(self, running_tasks, scheduled_tasks):
    '''return the list of machines that are currently available 
    sorted by whether they are in high demand to do the tasks. 
    The least requested machines will be at the top of the list'''
    def score(machine):
      '''returns the number of times the machine should be used by tasks'''
      count = 0
      for task in scheduled_tasks:
        if machine in task.machines:
          count += 1
      return count

    machines = list(range(1, DATA['parameters']['size']['nb_machines']+1))
    for task in running_tasks:
      machines.remove(task.machine)
    
    return sorted(machines, key=score)

  def get_available_operators(self, running_tasks, scheduled_tasks):
    '''return the list of operators that are currently available 
    sorted by whether they are in high demand to do the tasks. 
    The least requested operators will be at the top of the list'''
    def score(operator):
      '''returns the number of times the operator should be used by tasks'''
      count = 0
      for task in scheduled_tasks:
        for operators in task.machines.values():
          if operator in operators:
            count += 1
      return count

    operators = list(range(1, DATA['parameters']['size']['nb_operators']+1))
    for task in running_tasks:
      operators.remove(task.operator)
    
    return sorted(operators, key=score)

  def step(self):
    '''makes all the necessary changes to increment the time by one unit'''
    self.update_jobs()
    jobs = self.get_jobs_by_priority()

    running_tasks = self.get_running_tasks(jobs)
    scheduled_tasks = self.get_scheduled_tasks(jobs)
    machines = self.get_available_machines(running_tasks, scheduled_tasks)
    operators = self.get_available_operators(running_tasks, scheduled_tasks)

    for task in scheduled_tasks:
      machine = task.compatible_machine(machines)
      if machine is None:
        continue
      operator = task.compatible_operator(machine, operators)
      if operator is None:
        continue
      
      task.assign(self.t, machine, operator)
      machines.remove(machine)
      operators.remove(operator)

    self.t += 1