from django.contrib.auth.forms import forms, UsernameField, AuthenticationForm


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
