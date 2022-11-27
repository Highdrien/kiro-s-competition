import json

from data import DATA, size
from job import Job
from solver import Solver

solver = Solver(
  jobs = list(map(Job.from_json, range(DATA['parameters']['size']['nb_jobs'])))
)

for _ in range(100):
  solver.step()

with open(f"solution/{size}-sol.json", 'w') as file:
  tasks = []
  for job in solver.jobs:
    for task in job.sequence:
      tasks.append(task.to_json())

  json.dump(sorted(tasks, key=lambda task: task['task']), file, indent='\t')
