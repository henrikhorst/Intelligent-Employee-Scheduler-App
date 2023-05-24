from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=50)
    working_hours_per_week = models.PositiveIntegerField(default=0)
    worked_hours = models.PositiveIntegerField(default=0)
    shifts_per_week = models.PositiveIntegerField()
    slug = models.SlugField(default="", null=False)

    def __str__(self) -> str:
        return f"{self.name}"
    
    def get_absolute_url(self):
        return reverse("employee", args=[self.id])
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Preferences(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    
    OPTION_ONE = 'OPTION_ONE'
    OPTION_TWO = 'OPTION_TWO'
    OPTION_THREE = 'OPTION_THREE'

    MY_CHOICES = [
        (OPTION_ONE, 'Gut'),
        (OPTION_TWO, 'Würde gehen, aber nicht gut'),
        (OPTION_THREE, 'Gar nicht'),
    ]

    monday_1 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)
    monday_2 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)
    monday_3 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)
    tuesday_1 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)
    tuesday_2 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)
    tuesday_3 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)
    wednesday_1 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)
    wednesday_2 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)
    wednesday_3 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)
    thursday_1 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)
    thursday_2 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)
    thursday_3 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)
    friday_1 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)
    friday_2 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)
    friday_3 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)
    saturday_1 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)
    saturday_2 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)
    saturday_3 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)
    sunday_1 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)
    sunday_2 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)
    sunday_3 = models.CharField(max_length=20,choices=MY_CHOICES,default=OPTION_ONE,)

    def __str__(self) -> str:
        return f"{self.employee.name}"


## CalenderWeek is a parent class for single Schedules
class CalenderWeek(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("single_schedule", args=[self.id])

    
class Schedule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null = True)
    calender_week = models.ForeignKey(CalenderWeek,on_delete=models.CASCADE,blank=True, null=True)
    monday_1 = models.BooleanField(default=False)
    monday_2 = models.BooleanField(default=False)
    monday_3 = models.BooleanField(default=False)
    tuesday_1 = models.BooleanField(default=False)
    tuesday_2 = models.BooleanField(default=False)
    tuesday_3 = models.BooleanField(default=False)
    wednesday_1 = models.BooleanField(default=False)
    wednesday_2 = models.BooleanField(default=False)
    wednesday_3 = models.BooleanField(default=False)
    thursday_1 = models.BooleanField(default=False)
    thursday_2 = models.BooleanField(default=False)
    thursday_3 = models.BooleanField(default=False)
    friday_1 = models.BooleanField(default=False)
    friday_2 = models.BooleanField(default=False)
    friday_3 = models.BooleanField(default=False)
    saturday_1 = models.BooleanField(default=False)
    saturday_2 = models.BooleanField(default=False)
    saturday_3 = models.BooleanField(default=False)
    sunday_1 = models.BooleanField(default=False)
    sunday_2 = models.BooleanField(default=False)
    sunday_3 = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.calender_week}: {self.employee}"

class WeeklyShiftPlan(models.Model):
    name = models.CharField(max_length=50)
    monday_1 = models.IntegerField()
    monday_2 = models.IntegerField()
    monday_3 = models.IntegerField()
    tuesday_1 = models.IntegerField()
    tuesday_2 = models.IntegerField()
    tuesday_3 = models.IntegerField()
    wednesday_1 = models.IntegerField()
    wednesday_2 = models.IntegerField()
    wednesday_3 = models.IntegerField()
    thursday_1 = models.IntegerField()
    thursday_2 = models.IntegerField()
    thursday_3 = models.IntegerField()
    friday_1 = models.IntegerField()
    friday_2 = models.IntegerField()
    friday_3 = models.IntegerField()
    saturday_1 = models.IntegerField()
    saturday_2 = models.IntegerField()
    saturday_3 = models.IntegerField()
    sunday_1 = models.IntegerField()
    sunday_2 = models.IntegerField()
    sunday_3 = models.IntegerField()

    def __str__(self) -> str:
            return f"{self.name}"






