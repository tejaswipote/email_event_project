from django.contrib import admin

# Register your models here.
from application.models import Employee, Template, Event, EmailLog

admin.site.register(Employee)
admin.site.register(Template)
admin.site.register(EmailLog)
admin.site.register(Event)