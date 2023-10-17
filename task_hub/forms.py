from django.contrib.auth import get_user_model
from django.contrib.auth.forms import forms, AuthenticationForm, UserChangeForm, UserCreationForm

from task_hub.models import Task, Position


class WorkerLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs = {
                "class": "form-control form-control-lg",
                "placeholder": field.label
            }
            field.label = ""


class WorkerChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "position", )


class WorkerCreationForm(UserCreationForm):
    position = forms.ModelChoiceField(
        empty_label="Select position",
        queryset=Position.objects.all(),
        widget=forms.Select(attrs={"class": "form-select form-select-lg"}),
    )

    def __init__(self, *args, **kwargs):
        super(WorkerCreationForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name != "position":
                field.widget.attrs = {
                    "placeholder": field.label,
                    "class": "form-control form-control-lg",
                }

            if field_name != "password2":
                field.help_text = ""

            field.label = ""

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name", "position", )

    def save(self, commit=True):
        user = super(WorkerCreationForm, self).save(commit=False)
        user.position = self.cleaned_data['position']
        if commit:
            user.save()
        return user


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control blur",
                "placeholder": "🔍︎ Search by username"
            }
        )
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
