from django.urls import path
from . import views

urlpatterns= [
    path("", views.index, name="index"),
    path("login/", views.login_user, name = "login"),
    path("logout/", views.logout_user, name = "logout"),
    path("register/", views.register_user, name = "register"),
    path("about", views.about, name = "about"),
    path("employees", views.employees, name = "employees"),
    path("add", views.add_employee, name="add_employee"),
    path("schedule-structure", views.schedule_structure, name = "schedule-structure"),
    path("schedule-structure-add", views.schedule_structure_add, name = "schedule-structure-add"),
    path("schedule", views.schedule, name = "schedule"),
    path("schedule-add", views.schedule_add, name = "schedule-add"),
    path("change-preferences", views.change_preferences, name = "change-preferences"),
    path("employee/<int:id>", views.employee, name="employee"),
    path("schedule/<int:id>", views.single_schedule, name="single_schedule"),

    
    
]