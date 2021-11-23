from django import forms
from .models import Message, Task, Group
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded-md',
                'placeholder': 'Enter your username...'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'w-full p-2 rounded-md',
                'placeholder': 'Enter your password...'
            }),
        }
        help_texts = {
            'username': ''
        }


class SignUpForm(UserCreationForm):

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-2 rounded-md',
            'placeholder': 'Enter password...'
        }),
        help_text="""
        Your password can’t be too similar to your other personal information.<br>
        Your password must contain at least 8 characters.<br>
        Your password can’t be a commonly used password.<br>
        Your password can’t be entirely numeric.
        """
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-2 rounded-md',
            'placeholder': 'Repeat password...'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded-md',
                'placeholder': 'Enter username...'
            })
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded-md',
                'placeholder': 'Enter your name here...'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-2 rounded-md',
                'placeholder': 'Enter your email here...'
            })
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded-md',
                'placeholder': 'Task name...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 rounded-md resize-none h-24',
                'placeholder': 'Task description...'
            }),
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded-md',
                'placeholder': 'Group name...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 rounded-md resize-none h-24',
                'placeholder': 'Group description...'
            })
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'w-full text-black p-2 rounded-md resize-none h-24',
                'placeholder': 'Enter your message here...'
            })
        }