from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', ]

        help_texts = {
            'username': 'Students should use their Roll number',
            'email': 'Students must provide a valid Email',

        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enrolment Number'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})



