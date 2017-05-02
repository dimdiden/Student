from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
)

# This method will return the currently active user model
# the custom user model if one is specified, or User otherwise.
User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs = {
            'class': 'form-control',
        }

        self.fields['password'].widget.attrs = {
            'class': 'form-control',
        }

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        # user_qs = User.objects.filter(username=username)
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("The user is no longer active")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs = {
            'class': 'form-control',
        }

        self.fields['password'].widget.attrs = {
            'class': 'form-control',
        }

        self.fields['email'].widget.attrs = {
            'class': 'form-control',
        }
        self.fields['email2'].widget.attrs = {
            'class': 'form-control',
        }

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
 
        if email != email2:
            raise forms.ValidationError("Emails must match")

        email_qs = User.objects.filter(email=email)
        if email_qs:
            raise forms.ValidationError("This email has already been registered")

        return super(UserRegisterForm, self).clean(*args, **kwargs)
