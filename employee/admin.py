from django import forms
from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from employee.models import Department, Result, Parameter, Employee, Answer, Territory


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)


class EmployeeCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(EmployeeCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EmployeeChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=("Password",),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\'../password/\'>this form</a>."))

    class Meta:
        model = Employee
        fields = ('email',)

    def clean_password(self):
        return self.initial["password"]


class EmployeeAdmin(UserAdmin):
    form = EmployeeChangeForm
    add_form = EmployeeCreationForm
    list_display = ('email', 'first_name', 'nik', 'department', 'supervisor')
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Company info', {'fields': ('nik', 'department', 'supervisor', 'territory')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    filter_horizontal = ()


class ParameterAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'question',
        'department'
    )


admin.site.register(Department, DepartmentAdmin)

admin.site.register(Employee, EmployeeAdmin)

admin.site.register(Parameter, ParameterAdmin)

admin.site.register(Territory)

admin.site.unregister(Group)
