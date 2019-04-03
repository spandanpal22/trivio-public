from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser,Question

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email','college','name',)

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        #fields = ('username', 'email','college','score','name',)
        fields = UserChangeForm.Meta.fields


class ReplyForm(forms.ModelForm):
	class Meta:
		model=Question
		fields=('answer',)