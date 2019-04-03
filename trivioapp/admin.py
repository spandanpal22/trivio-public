from django.contrib import admin
# from .models import Question
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import SignUpForm, CustomUserChangeForm
from .models import CustomUser,Question,Event




class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['name','email', 'username', 'score','college','status','flag','email_confirmed']
    
    fieldsets = (
        (None, {'fields': ('name','email', 'username','score','college','password','status','flag','email_confirmed')}), )

admin.site.register(CustomUser, CustomUserAdmin)
# Register your models here.
admin.site.register(Question)
admin.site.register(Event)