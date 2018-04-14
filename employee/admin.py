from django.contrib import admin

# Register your models here.

from employee.models import Department, Result, Parameter, Employee, Answer


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)


class EmployeeAdmin(admin.ModelAdmin):
    raw_id_fields = ('department',)
    list_display = ('email', 'department', 'supervisor')
    fields = ('first_name', 'last_name', 'email', 'username', 'password', 'nik', 'supervisor')


class ParameterAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'question',
        'department'
    )


class ResultInline(admin.StackedInline):
    model = Result.answers.through
    extra = 0


class ResultAdmin(admin.ModelAdmin):
    exclude = ('answers',)
    inlines = (ResultInline,)
    list_display = ('name', 'employee', 'created')


admin.site.register(Department, DepartmentAdmin)

admin.site.register(Employee, EmployeeAdmin)

admin.site.register(Parameter, ParameterAdmin)

admin.site.register(Answer)
admin.site.register(Result, ResultAdmin)
