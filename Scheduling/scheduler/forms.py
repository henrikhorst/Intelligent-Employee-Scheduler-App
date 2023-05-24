from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Employee, WeeklyShiftPlan, Preferences


class NewEmployeeForm(forms.Form):
    name = forms.CharField(max_length=60, label="Vor- und Nachname")
    shifts_per_week = forms.IntegerField(min_value=1, max_value=21, label="Schichten pro Woche")

class PickEmployeeForm(forms.Form):
    name = forms.CharField(max_length=60, label="Name", required=True)
    single_object = forms.ModelChoiceField(
        queryset=WeeklyShiftPlan.objects.all(),
        empty_label="Option auswählen",
        label = "Dienstplanstruktur auswählen:",
        error_messages={
            'required': 'Dieses Feld muss ausgewählt werden',
        },
    )
    objects = forms.ModelMultipleChoiceField(
        queryset=Employee.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label = "Mitarbeiter auswählen",
        error_messages={
            'required': 'Dieses Feld muss ausgewählt werden',
        }
    )

class NewWeeklyShiftPlanForm(forms.Form):
    monday_1 = forms.IntegerField(label="Montag Frühdienst")
    monday_2 = forms.IntegerField(label="Montag Spätdienst")
    monday_3 = forms.IntegerField(label="Montag Nachtdienst")
    tuesday_1 = forms.IntegerField(label="Dienstag Frühdienst")
    tuesday_2 = forms.IntegerField(label="Dienstag Spätdienst")
    tuesday_3 = forms.IntegerField(label="Dienstag Nachtdienst")
    wednesday_1 = forms.IntegerField(label="Mittwoch Frühdienst")
    wednesday_2 = forms.IntegerField(label="Mittwoch Spätdienst")
    wednesday_3 = forms.IntegerField(label="Mittwoch Nachtdienst")
    thursday_1 = forms.IntegerField(label="Donnerstag Frühdienst")
    thursday_2 = forms.IntegerField(label="Donnerstag Spätdienst")
    thursday_3 = forms.IntegerField(label="Donnerstag Nachtdienst")
    friday_1 = forms.IntegerField(label="Freitag Frühdienst")
    friday_2 = forms.IntegerField(label="Freitag Spätdienst")
    friday_3 = forms.IntegerField(label="Freitag Nachtdienst")
    saturday_1 = forms.IntegerField(label="Samstag Frühdienst")
    saturday_2 = forms.IntegerField(label="Samstag Spätdienst")
    saturday_3 = forms.IntegerField(label="Samstag Nachtdienst")
    sunday_1 = forms.IntegerField(label="Sonntag Frühdienst")
    sunday_2 = forms.IntegerField(label="Sonntag Spätdienst")
    sunday_3 = forms.IntegerField(label="Sonntag Nachtdienst")


class ChangePrefernecesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        exclude = ['employee']



class SignUpForm(UserCreationForm):
    username = forms.CharField(label="Benutzername", help_text="Nur Buchstaben, Zeichen und @/./+/-/_ erlaubt.")
    email = forms.EmailField(label="Email:")
    first_name = forms.CharField(max_length=50, label="Vorname:")
    last_name = forms.CharField(max_length=50, label = 'Nachname:')
    password1 = forms.CharField(
        label="Password",
        help_text="<be><ul><li>Ihr Passwort darf Ihren anderen persönlichen Daten nicht zu ähnlich sein.</li>"
                  "<li>Ihr Passwort muss mindestens 8 Zeichen enthalten.</li>"
                  "<li>Ihr Passwort darf kein häufig verwendetes Passwort sein.</li>"
                  "<li>Ihr Passwort darf nicht ausschließlich aus Zahlen bestehen.</li></ul>",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Password confirmation",
        help_text="<br> Geben Sie zur Überprüfung das gleiche Passwort wie zuvor ein.",
        widget=forms.PasswordInput
    )
    

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')