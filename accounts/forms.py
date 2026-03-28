from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


INPUT_CLASS = (
    'w-full px-4 py-2 border border-gray-300 rounded-lg '
    'focus:outline-none focus:ring-2 focus:ring-blue-500'
)


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': INPUT_CLASS,
                'placeholder': 'you@example.com',
                'autocomplete': 'email',
            }
        ),
    )
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Enter your password',
                'autocomplete': 'current-password',
            }
        ),
    )


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {
                'class': INPUT_CLASS,
                'placeholder': 'you@example.com',
                'autocomplete': 'email',
            }
        )
        self.fields['first_name'].widget.attrs.update(
            {
                'class': INPUT_CLASS,
                'placeholder': 'First name',
                'autocomplete': 'given-name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'class': INPUT_CLASS,
                'placeholder': 'Last name',
                'autocomplete': 'family-name',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'class': INPUT_CLASS,
                'placeholder': 'Create password',
                'autocomplete': 'new-password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'class': INPUT_CLASS,
                'placeholder': 'Confirm password',
                'autocomplete': 'new-password',
            }
        )