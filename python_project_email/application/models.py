from django.db import models

# Create your models here.
EVENT_CHOICES = (
    (1, "Birthday"),
    (2, "WorkAnniversary")
)


class Common(models.Model):
    """
    Abstract Model to add created_at and updated_at in models
     """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Employee(Common):
    """ Model for the Employee """
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    birth_date = models.DateField()
    joining_date = models.DateField()

    def _str_(self):
        return "{}".format(self.name)


class Event(Common):
    """ Model for the Event """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    event_type = models.IntegerField(choices=EVENT_CHOICES)
    event_date = models.DateField()

    def _str_(self):
        return "{} , {}".format(self.employee.name, self.event_type)


class Template(Common):
    """ Model for the Template """
    event_type = models.IntegerField(choices=EVENT_CHOICES)
    template = models.TextField()

    def _str_(self):
        return "{} : {}".format(self.event_type, self.template)


class EmailLog(models.Model):
    """ Model for the Email Log """

    EMAIL_STATUS_CHOICES = (
        (1, "Pass"),
        (2, "Fail"),
        (3, "No Events for the day")

    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    email_sent_at = models.DateTimeField()
    status = models.IntegerField(choices=EMAIL_STATUS_CHOICES, )
    error_info = models.CharField(max_length=255)

    def _str_(self):
        return "{}".format(self.employee.name)