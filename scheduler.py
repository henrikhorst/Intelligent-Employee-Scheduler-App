from ortools.sat.python import cp_model
import pandas as pd
import numpy as np

class Scheduler:
    def __init__(self, num_nurses = 4, num_shifts = 3, num_days = 3) -> None:
        self.all_nurses = range(num_nurses)
        self.all_shifts = range(num_shifts)
        self.all_days = range(num_days)

        model = cp_model.CpModel()
        # Creates a boolean value for all possible combinations
        shifts = {}
        for n in self.all_nurses:
            for d in self.all_days:
                for s in self.all_shifts:
                    shifts[(n, d, s)] = model.NewBoolVar(f'shift_n{n}d{d}s{s}')

        #Each shift is assigned to a single nurse per day
        for d in self.all_days:
            for s in self.all_shifts:
                model.AddExactlyOne(shifts[(n, d, s)] for n in self.all_nurses)
        #Each nurse works at most one shift per day.
        for n in self.all_nurses:
            for d in self.all_days:
                model.AddAtMostOne(shifts[(n, d, s)] for s in self.all_shifts)

        # Try to distribute the shifts evenly, so that each nurse works
        # min_shifts_per_nurse shifts. If this is not possible, because the total
        # number of shifts is not divisible by the number of nurses, some nurses will
        # be assigned one more shift.
        min_shifts_per_nurse = (num_shifts * num_days) // num_nurses
        if num_shifts * num_days % num_nurses == 0:
            max_shifts_per_nurse = min_shifts_per_nurse
        else:
            max_shifts_per_nurse = min_shifts_per_nurse + 1
        for n in self.all_nurses:
            shifts_worked = []
            for d in self.all_days:
                for s in self.all_shifts:
                    shifts_worked.append(shifts[(n, d, s)])
            model.Add(min_shifts_per_nurse <= sum(shifts_worked))
            model.Add(sum(shifts_worked) <= max_shifts_per_nurse)

        solver = cp_model.CpSolver()
        solver.parameters.linearization_level = 0
        # Enumerate all solutions.
        solver.parameters.enumerate_all_solutions = True

        # Display the first five solutions.
        solution_limit = 1
        solution_printer = NursesPartialSolutionPrinter(shifts, num_nurses,
                                                        num_days, num_shifts,
                                                        solution_limit)
        solver.Solve(model, solution_printer)

        
class NursesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, shifts, num_nurses, num_days, num_shifts, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._num_nurses = num_nurses
        self._num_days = num_days
        self._num_shifts = num_shifts
        self._solution_count = 0
        self._solution_limit = limit
        

    def on_solution_callback(self):
        self.solutions = pd.DataFrame(np.zeros((self._num_nurses, self._num_days * self._num_shifts), dtype = int))
        self._solution_count += 1
        print(f'Solution {self._solution_count}')
        for d in range(self._num_days):
            print(f'Day {d}')
            for n in range(self._num_nurses):
                is_working = False
                for s in range(self._num_shifts):
                    if self.Value(self._shifts[(n, d, s)]):
                        is_working = True
                        self.solutions.iloc[n, d*self._num_shifts + s] = 1
                        print(f'  Nurse {n} works shift {s}')
                if not is_working:
                    print(f'  Nurse {n} does not work')
        self.solutions.to_csv(f"solution{self._solution_count}")
        
        if self._solution_count >= self._solution_limit:
            print(f'Stop search after {self._solution_limit} solutions' )
            self.StopSearch()

    def solution_count(self):
        return self._solution_count

       
        
            