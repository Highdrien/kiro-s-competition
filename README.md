# Kiro Competition 2022-2023

This repository is the code used for the [Kiros competition](https://kiro.enpc.org/index.php) organized by the Pont Paris school (year: 2022-2023). You can find the subject on their website.

## Table of Contents

- [Kiro Competition 2022-2023](#kiro-competition-2022-2023)
  - [Table of Contents](#table-of-contents)
  - [Structure](#structure)
  - [Execution](#execution)
  - [How the code works](#how-the-code-works)

## Structure

    .
    ├── concours_kiro_2022_2023
    │   ├── solution                # solutions forlder             
    │   │    ├── huge-sol.json      
    │   │    ├── large-sol.json
    │   │    ├── medium-sol.json    
    │   │    └── tiny-sol.json  
    │   ├── sujet                   # subjects forlder
    │   │    ├── huge.json           
    │   │    ├── large.json
    │   │    ├── medium.json     
    │   │    └── tiny.json                                      
    │   ├── data.py                 # collects data
    │   ├── job.py                  # class job
    │   ├── main.py                 # main
    │   ├── solver.py               # class solver
    │   └── task.py                 # class task

## Execution

To open and create json files you need to have the json package. In a terminal type the following command:
```bash
pip install json
```

Then, in the `data.py` folder, change the size parameter (line 3) to your liking (tiny, medium, large or huge).

Then run the program `main.py`. The file `<size>-sol.json` will be created in the `solution` folder. If it already exists, it will be modified.

## How the code works

To solve the problem, the `data.py` program will retrieve the data stored in a json file and transform it into a python dictionary. The programs `job.py` and `task.py` create python classes to use job and task.

The program `solver.py` will find an estimation of the best solution. To do this, we chose to approximate the cost of the tasks we can do at each time (we calculate how much it will cost us not to do this task, depending on the rest of the tasks to complete the job). We also get the list of machines sorted by their utilities. That is to say that we will assign to the machines according to their demand in the available tasks. The goal is to be able to assign in priority the machines that are less useful. We do the same for the operators. Then we will find triplets (task, machine, operator) which minimizes the cost of the tasks, and the utility of the machines and the operators. We took the choice to minimize in priority the tasks, then the machines then the operators. We find a maximum of triplet then we assign the machines and the operators chosen to their respective task. We increment the time, and we start again.

