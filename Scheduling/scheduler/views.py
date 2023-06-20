from ortools.sat.python import cp_model
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import NewEmployeeForm, NewWeeklyShiftPlanForm, SignUpForm, PickEmployeeForm, ChangePrefernecesForm
from .models import Employee, WeeklyShiftPlan, Schedule, CalenderWeek
from django.db.models import BooleanField
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import utils

# Create your views here.

def index(request):
    if request.method == "POST":
        username= request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username= username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "Einloggen erfolgreich")
            return HttpResponseRedirect("./")
        else:
            messages.success(request, "Falscher Nutzername oder Passwort")
            return HttpResponseRedirect("./")
    return render(request, "scheduler/index.html")

def about(request):
    return render(request, "scheduler/about.html")

def schedule_structure(request):
    if request.user.is_authenticated:
        # The user is logged in. Render a user-specific page.
        context = {
            'username': request.user.username,
            'email': request.user.email,
        }
        return render(request, "scheduler/schedule_structure.html", {
            "weekly_shift_plans" : [],
        })
    else:
        # The user is not logged in. Render a standard page.
        weekly_shifts_plans = WeeklyShiftPlan.objects.all()
        return render(request,"scheduler/schedule_structure.html", {
            "weekly_shift_plans" : weekly_shifts_plans,
        })
    
def schedule_structure_add(request):
    if request.method == 'POST':
        form = NewWeeklyShiftPlanForm(request.POST)

        if form.is_valid():
            weekly_shift_plan = WeeklyShiftPlan(
                monday_1=form.cleaned_data['monday_1'],
                monday_2=form.cleaned_data['monday_2'],
                monday_3=form.cleaned_data['monday_3'],
                tuesday_1=form.cleaned_data['tuesday_1'],
                tuesday_2=form.cleaned_data['tuesday_2'],
                tuesday_3=form.cleaned_data['tuesday_3'],
                wednesday_1=form.cleaned_data['wednesday_1'],
                wednesday_2=form.cleaned_data['wednesday_2'],
                wednesday_3=form.cleaned_data['wednesday_3'],
                thursday_1=form.cleaned_data['thursday_1'],
                thursday_2=form.cleaned_data['thursday_2'],
                thursday_3=form.cleaned_data['thursday_3'],
                friday_1=form.cleaned_data['friday_1'],
                friday_2=form.cleaned_data['friday_2'],
                friday_3=form.cleaned_data['friday_3'],
                saturday_1=form.cleaned_data['saturday_1'],
                saturday_2=form.cleaned_data['saturday_2'],
                saturday_3=form.cleaned_data['saturday_3'],
                sunday_1=form.cleaned_data['sunday_1'],
                sunday_2=form.cleaned_data['sunday_2'],
                sunday_3=form.cleaned_data['sunday_3'],
                
                
                )
            weekly_shift_plan.save()
            return HttpResponseRedirect("./")
    else:
        form = NewWeeklyShiftPlanForm()
    return render(request, "scheduler/schedule_structure_add.html", {
        "form": form
    })


def employees(request):
    if request.user.is_authenticated:
        # The user is logged in. Render a user-specific page.
        context = {
            'username': request.user.username,
            'email': request.user.email,
        }
        employees = Employee.objects.filter(user=request.user)
        return render(request,"scheduler/employees.html", {
            "employees" : employees,
        })
    else:
        # The user is not logged in. Render a standard page.
        employees = Employee.objects.filter(user=None)
        return render(request,"scheduler/employees.html", {
            "employees" : employees,
        })

def employee(request, id):
    employee = get_object_or_404(Employee, pk=id)
    path = employee.name.lower().replace(" ", "_")
    return render(request, "scheduler/employee.html", {
        "employee" : employee,
        "path" : f"{path}.jpg",
    })

def add_employee(request):
    if request.method == 'POST':
        form = NewEmployeeForm(request.POST)

        if form.is_valid():
            employee = Employee(user= request.user, name=form.cleaned_data['name'],shifts_per_week=form.cleaned_data['shifts_per_week'])
            employee.save()
            return HttpResponseRedirect("./")
    else:
        form = NewEmployeeForm()
    return render(request, "scheduler/add_employee.html", {
        "form": form
    })

def change_preferences(request):
    form = ChangePrefernecesForm()
    return render(request, 'scheduler/change_preferences.html', {'form': form})


def schedule(request):
    if request.user.is_authenticated:
        # The user is logged in. Render a user-specific page.
        context = {
            'username': request.user.username,
            'email': request.user.email,
        }
        return render(request, "scheduler/schedule.html", {
                "calender_weeks": []
            })
    else:
        # The user is not logged in. Render a standard page.
        
        if request.method == 'GET':
            calender_weeks = CalenderWeek.objects.all()
            return render(request, "scheduler/schedule.html", {
                "calender_weeks": calender_weeks
            })
        else:
            return render(request, "scheduler/schedule.html")
    
def single_schedule(request, id):
    single_schedule = get_object_or_404(CalenderWeek, pk=id)
    # Get list of boolean field names in MyModel
    bool_fields = [field.name for field in Schedule._meta.fields if isinstance(field, BooleanField)]
    # For each object, sum over the values of the boolean fields
    sum_boolean = 0
    # For each object, sum over the values of the boolean fields
    sum_boolean_list = []
    for obj in single_schedule.schedule_set.all():
        sum_boolean = 0
        for field in bool_fields:
            
            if getattr(obj, field): # this gets the value of the field from the object
                
                sum_boolean += 1
        sum_boolean_list.append(sum_boolean)
    combined = zip(single_schedule.schedule_set.all(), sum_boolean_list)
    return render(request, "scheduler/calender_week.html", {
        "combined" : combined
        
    })

def schedule_add(request):
    if request.method == 'POST':
        form = PickEmployeeForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            employees = form.cleaned_data['objects']
            weekly_shift_plan = form.cleaned_data['single_object']
            # Do something with selected_objects here
            calender_week = CalenderWeek.objects.create(name = name)
            # get the number of employees
            num_employees = employees.count()
            print(num_employees)
            data = ((employee.name, employee.shifts_per_week) for employee in employees)
            num_shifts = 3
            num_days = 7
            num_weeks = 1

            ## Fixed assignment: (employee, shift, day).
            # This fixes the first 2 days of the schedule.
            fixed_assignments = []
            # Prohibited assignment: (employee, shift, day).
            prohibited_assignments = []
            # Request: (employee, shift, day, weight)
            # A negative weight indicates that the employee desire this assignment.
            requests = []
            # Employee 3 does not want to work on the first Saturday (negative weight
            # for the Off shift).
            #(3, 0, 5, -2),
            # Employee 5 wants a night shift on the second Thursday (negative weight).
            #(5, 3, 10, -2),
            # Employee 2 does not want a night shift on the first Friday (positive
            # weight).
            #(2, 3, 4, 4)
            for counter, employee in enumerate(employees):
                #Monday (counter, 0-2, 0)
                if employee.preferences.monday_1 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,0,0))
                elif employee.preferences.monday_1 == 'OPTION_ONE':
                    requests.append((counter,0,0,-1))
                elif employee.preferences.monday_1 == 'OPTION_TWO':
                    requests.append((counter,0,0,2))
                if employee.preferences.monday_2 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,1,0))
                elif employee.preferences.monday_2 == 'OPTION_ONE':
                    requests.append((counter,1,0,-1))
                elif employee.preferences.monday_2 == 'OPTION_TWO':
                    requests.append((counter,1,0,2))
                if employee.preferences.monday_3 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,2,0))
                elif employee.preferences.monday_3 == 'OPTION_ONE':
                    requests.append((counter,2,0,-1))
                elif employee.preferences.monday_3 == 'OPTION_TWO':
                    requests.append((counter,2,0,2))
                #Tuesday (counter, 0-2, 1)
                if employee.preferences.tuesday_1 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,0,1))
                elif employee.preferences.monday_3 == 'OPTION_ONE':
                    requests.append((counter,0,1,-1))
                elif employee.preferences.monday_3 == 'OPTION_TWO':
                    requests.append((counter,0,1,2))
                
                if employee.preferences.tuesday_2 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,1,1))
                elif employee.preferences.monday_3 == 'OPTION_ONE':
                    requests.append((counter,1,1,-1))
                elif employee.preferences.monday_3 == 'OPTION_TWO':
                    requests.append((counter,1,1,2))
                
                if employee.preferences.tuesday_3 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,2,1))
                elif employee.preferences.monday_3 == 'OPTION_ONE':
                    requests.append((counter,2,1,-1))
                elif employee.preferences.monday_3 == 'OPTION_TWO':
                    requests.append((counter,2,1,2))

                #Wednesday (counter, 0-2, 2)
                if employee.preferences.wednesday_1 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,0,2))
                elif employee.preferences.monday_3 == 'OPTION_ONE':
                    requests.append((counter,0,2,-1))
                elif employee.preferences.monday_3 == 'OPTION_TWO':
                    requests.append((counter,0,2,2))

                if employee.preferences.wednesday_2 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,1,2))
                elif employee.preferences.monday_3 == 'OPTION_ONE':
                    requests.append((counter,1,2,-1))
                elif employee.preferences.monday_3 == 'OPTION_TWO':
                    requests.append((counter,1,2,2))

                if employee.preferences.wednesday_3 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,2,2))
                elif employee.preferences.monday_3 == 'OPTION_ONE':
                    requests.append((counter,2,2,-1))
                elif employee.preferences.monday_3 == 'OPTION_TWO':
                    requests.append((counter,2,2,2))

                #Thursday (counter, 0-2, 3)
                if employee.preferences.thursday_1 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,0,3))
                elif employee.preferences.monday_3 == 'OPTION_ONE':
                    requests.append((counter,0,3,-1))
                elif employee.preferences.monday_3 == 'OPTION_TWO':
                    requests.append((counter,0,3,2))

                if employee.preferences.thursday_2 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,1,3))
                elif employee.preferences.monday_3 == 'OPTION_ONE':
                    requests.append((counter,1,3,-1))
                elif employee.preferences.monday_3 == 'OPTION_TWO':
                    requests.append((counter,1,3,2))

                if employee.preferences.thursday_3 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,2,3))
                elif employee.preferences.monday_3 == 'OPTION_ONE':
                    requests.append((counter,2,3,-1))
                elif employee.preferences.monday_3 == 'OPTION_TWO':
                    requests.append((counter,2,3,2))
                #Friday (counter, 0-2, 4)
                if employee.preferences.friday_1 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,0,4))
                elif employee.preferences.monday_3 == 'OPTION_ONE':
                    requests.append((counter,0,4,-1))
                elif employee.preferences.monday_3 == 'OPTION_TWO':
                    requests.append((counter,0,4,2))

                if employee.preferences.friday_2 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,1,4))
                elif employee.preferences.monday_3 == 'OPTION_ONE':
                    requests.append((counter,1,4,-1))
                elif employee.preferences.monday_3 == 'OPTION_TWO':
                    requests.append((counter,1,4,2))

                if employee.preferences.friday_3 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,2,4))
                elif employee.preferences.monday_3 == 'OPTION_ONE':
                    requests.append((counter,2,4,-1))
                elif employee.preferences.monday_3 == 'OPTION_TWO':
                    requests.append((counter,2,4,2))

                #Saturday (counter, 0-2, 5)
                if employee.preferences.saturday_1 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,0,5))
                elif employee.preferences.monday_3 == 'OPTION_ONE':
                    requests.append((counter,0,5,-1))
                elif employee.preferences.monday_3 == 'OPTION_TWO':
                    requests.append((counter,0,5,2))

                if employee.preferences.saturday_2 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,1,5))
                elif employee.preferences.monday_3 == 'OPTION_ONE':
                    requests.append((counter,1,5,-1))
                elif employee.preferences.monday_3 == 'OPTION_TWO':
                    requests.append((counter,1,5,2))
                
                if employee.preferences.saturday_3 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,2,5))
                elif employee.preferences.monday_3 == 'OPTION_ONE':
                    requests.append((counter,2,5,-1))
                elif employee.preferences.monday_3 == 'OPTION_TWO':
                    requests.append((counter,2,5,2))

                #Sunday (counter, 0-2, 6)
                if employee.preferences.sunday_1 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,0,6))
                elif employee.preferences.monday_3 == 'OPTION_ONE':
                    requests.append((counter,0,6,-1))
                elif employee.preferences.monday_3 == 'OPTION_TWO':
                    requests.append((counter,0,6,2))

                if employee.preferences.sunday_2 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,1,6))
                elif employee.preferences.monday_3 == 'OPTION_ONE':
                    requests.append((counter,1,6,-1))
                elif employee.preferences.monday_3 == 'OPTION_TWO':
                    requests.append((counter,1,6,2))

                if employee.preferences.sunday_3 == 'OPTION_THREE':
                    prohibited_assignments.append((counter,2,6))
                elif employee.preferences.monday_3 == 'OPTION_ONE':
                    requests.append((counter,2,6,-1))
                elif employee.preferences.monday_3 == 'OPTION_TWO':
                    requests.append((counter,2,6,2))

            ### Shift constraints on continuous sequence :
            #     (shift, hard_min, soft_min, min_penalty,
            #             soft_max, hard_max, max_penalty)
            shift_constraints = [
                # One or two consecutive days of rest, this is a hard constraint.
                (-1, 1, 1, 0, 2, 2, 0),
                # between 2 and 3 consecutive days of night shifts, 1 and 4 are
                # possible but penalized.
                (2, 1, 2, 20, 3, 4, 5),
            ]

            ### Weekly sum constraints on shifts days:
            #     (shift, hard_min, soft_min, min_penalty,
            #             soft_max, hard_max, max_penalty)
            weekly_sum_constraints = [
                # Constraints on rests per week.
                #(0, 1, 2, 7, 2, 3, 4),
                # At least 1 night shift per week (penalized). At most 4 (hard).
                #(3, 0, 1, 3, 4, 4, 0),
            ]

            # Penalized transitions:
            #     (previous_shift, next_shift, penalty (0 means forbidden))
            penalized_transitions = [
                # Afternoon to night has a penalty of 4.
                (1, 2, 4),
                # Night to morning is forbidden.
                (2, 0, 0),
                # Afternoon to morning is forbidden.
                (1, 0, 1),
            ]
            
            
            all_employees = range(num_employees)
            all_shifts = range(num_shifts)
            all_days = range(num_days)
            model = cp_model.CpModel()
            # Creates a boolean value for all possible combinations
            shifts = {}
            for n in all_employees:
                for d in all_days:
                    for s in all_shifts:
                        shifts[(n, d, s)] = model.NewBoolVar(f'shift_n{n}d{d}s{s}')
            ### Everthing contrain dependend begins now
            # Linear terms of the objective in a minimization context.
            obj_int_vars = []
            obj_int_coeffs = []
            obj_bool_vars = []
            obj_bool_coeffs = []

            # Each employee works at most one shift per day.
            for n in all_employees:
                for d in all_days:
                    model.AddAtMostOne(shifts[(n, d, s)] for s in all_shifts)

            # Fixed assignments.
            for n, s, d in fixed_assignments:
                model.Add(shifts[n, d, s] == 1)

            # Prohibited assignments.
            for n, s, d in prohibited_assignments:
                model.Add(shifts[n, d, s] == 0)

            # Employee requests
            for n, s, d, w in requests:
                obj_bool_vars.append(shifts[n, d, s])
                obj_bool_coeffs.append(w)

        
            # Assign the number of shifts per day
            
            weekly_cover_demands = (weekly_shift_plan.monday_1, weekly_shift_plan.monday_2, weekly_shift_plan.monday_3, weekly_shift_plan.tuesday_1, weekly_shift_plan.tuesday_2, weekly_shift_plan.tuesday_3, weekly_shift_plan.wednesday_1, weekly_shift_plan.wednesday_2, weekly_shift_plan.wednesday_3, weekly_shift_plan.thursday_1, weekly_shift_plan.thursday_2, weekly_shift_plan.thursday_3, weekly_shift_plan.friday_1, weekly_shift_plan.friday_2, weekly_shift_plan.friday_3, weekly_shift_plan.saturday_1, weekly_shift_plan.saturday_2, weekly_shift_plan.saturday_3, weekly_shift_plan.sunday_1, weekly_shift_plan.sunday_2, weekly_shift_plan.sunday_3)
            ##print(shift_tuple)
            counter_d = 0
            for d in all_days:
                for s in all_shifts:
                    if s==0:
                        model.Add(sum(shifts[(n, d, s)] for n in all_employees) == weekly_cover_demands[counter_d])
                    elif s==1:
                        model.Add(sum(shifts[(n, d, s)] for n in all_employees) == weekly_cover_demands[counter_d+1])
                    elif s==2:
                        model.Add(sum(shifts[(n, d, s)] for n in all_employees) == weekly_cover_demands[counter_d+2])
                    ##print(shift_tuple[counter_d], shift_tuple[counter_d+1], shift_tuple[counter_d+2])
                counter_d += 3
            

            # Assign the max shift number and most equal distribution
            # Try to distribute the shifts evenly, so that each nurse works
            # min_shifts_per_nurse shifts. If this is not possible, because the total
            # number of shifts is not divisible by the number of nurses, some nurses will
            # be assigned one more shift.

            for n in all_employees:
                max_shifts_per_nurse = employees[n].shifts_per_week
                shifts_worked = []
                for d in all_days:
                    for s in all_shifts:
                        shifts_worked.append(shifts[(n, d, s)])
                #model.Add(min_shifts_per_nurse <= sum(shifts_worked))
                model.Add(sum(shifts_worked) <= max_shifts_per_nurse)
            
            # Penalized transitions
            for previous_shift, next_shift, cost in penalized_transitions:
                for n in range(num_employees):
                    for d in range(num_days - 1):
                        transition = [
                            shifts[n,d, previous_shift].Not(), shifts[n, d + 1, next_shift].Not()
                        ]
                        if cost == 0:
                            model.AddBoolOr(transition)
                        else:
                            trans_var = model.NewBoolVar(
                                f'transition (employee={n}, day={d})')
                            transition.append(trans_var)
                            model.AddBoolOr(transition)
                            obj_bool_vars.append(trans_var)
                            obj_bool_coeffs.append(cost)
            
            # Shift constraints
            for ct in shift_constraints:
                shift, hard_min, soft_min, min_cost, soft_max, hard_max, max_cost = ct
                for e in range(num_employees):
                    if shift == -1:
                        works =  []
                        for d in range(num_days):
                            # Define a new boolean variable that is true if any of the previous variables are true.
                            combined_bool_or = model.NewBoolVar(f'combined_bool_or_e_{e}_day_{d}')
                            shiftss = []
                            for s in range(num_shifts):
                                shiftss.append(shifts[e, d, s])

                            model.AddBoolOr(shiftss).OnlyEnforceIf(combined_bool_or)
                            works.append(combined_bool_or)
                    else:
                        works = [shifts[e, d, shift] for d in range(num_days)]

                    variables, coeffs = utils.add_soft_sequence_constraint(
                        model, works, hard_min, soft_min, min_cost, soft_max, hard_max,
                        max_cost,
                        f'shift_constraint(employee {e}, shift {shift})' )
                    obj_bool_vars.extend(variables)
                    obj_bool_coeffs.extend(coeffs)

            
             # Objective
            model.Minimize(
                sum(obj_bool_vars[i] * obj_bool_coeffs[i]
                    for i in range(len(obj_bool_vars))) +
                sum(obj_int_vars[i] * obj_int_coeffs[i]
                    for i in range(len(obj_int_vars))))
            solver = cp_model.CpSolver()
            solution_printer = cp_model.ObjectiveSolutionPrinter()
            status = solver.Solve(model, solution_printer)
            
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
                    self._solution_count += 1
                
                    print(f'Solution {self._solution_count}')
                    for d in range(self._num_days):
                        print(f'Day {d}')
                        for n in range(self._num_nurses):
                            is_working = False
                            for s in range(self._num_shifts):
                                if self.Value(self._shifts[(n, d, s)]):
                                    is_working = True
                                    print(f'  Nurse {n} works shift {s}')
                            if not is_working:
                                print(f'  Nurse {n} does not work')
                    
                    # Save to db
                    nurses = employees
                    mapping = ["monday_1", "monday_2", "monday_3", "tuesday_1", "tuesday_2", "tuesday_3", "wednesday_1", "wednesday_2", "wednesday_3", "thursday_1", "thursday_2", "thursday_3", "friday_1", "friday_2", "friday_3", "saturday_1", "saturday_2", "saturday_3", "sunday_1", "sunday_2", "sunday_3"]
                    for n in range(len(nurses)):
                        work = {}
                        for d in range(self._num_days):
                            for s in range(self._num_shifts):
                                if self.Value(self._shifts[(n, d, s)]):
                                    work[mapping[self._num_shifts*d+s]] = True


                        Schedule.objects.create(calender_week=calender_week, employee= nurses[n], **work)


                    if self._solution_count >= self._solution_limit:
                        print(f'Stop search after {self._solution_limit} solutions' )
                        self.StopSearch()

                def solution_count(self):
                    return self._solution_count

            # Display the first five solutions.
            solution_limit = 1
            solution_printer = NursesPartialSolutionPrinter(shifts, num_employees,
                                                            num_days, num_shifts,
                                                            solution_limit)
            
            solver.Solve(model, solution_printer)
            
            return redirect('schedule')
    else:
        form = PickEmployeeForm()
    return render(request, "scheduler/schedule_add.html", {
        "form": form
    })




def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, "Ausloggen erfolgreich")
    return HttpResponseRedirect("./")

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            form.save()
            # Authenticate and Login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username= username, password= password)
            login(request, user)
            messages.success(request, "Registrieren erfolgreich")
            return redirect("index")
        else:
            form = SignUpForm()
            
            return render(request, "scheduler/register.html", {"form": form})


    else:
        form = SignUpForm()
        print(form)
        return render(request, "scheduler/register.html", {"form": form})
    
    
    