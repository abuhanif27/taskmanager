from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


INPUT_CLASS = (
    'w-full rounded-xl border border-slate-300 bg-white/90 px-4 py-2.5 text-slate-900 shadow-sm '
    'transition placeholder:text-slate-400 focus:border-brand-500 focus:outline-none focus:ring-2 '
    'focus:ring-brand-400/40 dark:border-slate-700 dark:bg-slate-900/70 dark:text-slate-100 '
    'dark:placeholder:text-slate-500'
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