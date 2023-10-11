from django.contrib.auth import get_user_model
from django.contrib.auth.forms import forms, UsernameField, AuthenticationForm

from task_hub.models import Task


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Username"}
        )
    )

    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Password"
            }
        ),
    )


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    deadline = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control datepicker",
                "placeholder": "Please select date",
            }
        )
    )

    class Meta:
        model = Task
        fields = "__all__"


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control blur",
                "placeholder": "🔍︎ Search by task name"
            }
        )
    )
