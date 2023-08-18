import datetime

from application.models import Event, Template, Employee, EmailLog
from application.serializers import TemplateSerializer, EventSerializer, EmailLogSerializer, EmployeeSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


def send_emails(request):
    # Find events of todays date
    events = Event.objects.filter(event_date__lt=datetime.date.today(), event_date__day=datetime.date.today().day,
                                  event_date__month=datetime.date.today().month, )
    if events:
        for event in events:
            # find template based on event type
            template = Template.objects.get(event_type=event.event_type).template
            # find employee id
            emp = Employee.objects.get(id=event.employee_id)
            try:
                # format template
                template = template.format(emp.name)

                send_email(template, emp)
                EmailLog.objects.create(**{"employee": emp, "email_sent_at": datetime.datetime.now(), "status": 1})

            except Exception as e:
                try:
                    send_email(template, emp)
                    EmailLog.objects.create(**{"employee": emp, "email_sent_at": datetime.datetime.now(), "status": 1})
                except Exception as e:
                    EmailLog.objects.create(
                        **{"employee": emp, "email_sent_at": datetime.datetime.now(), "status": 2, "error_info": e})
        return HttpResponse("Sent Event for today")

    else:

        return HttpResponse("No Events for today")


def send_email(template, receiver):
    import smtplib, ssl

    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        sender_email = "tejaspote20@gmail.com"
        password = ""
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver.email, template)


# get event by id
def employee(request, pk):
    try:
        employees = Employee.objects.get(id=pk)
        serializer = EmployeeSerializer(employees)

    except Exception:
        return HttpResponse("No Employee found for given pk")
    return JsonResponse({"status": "success", "data": {"employees": serializer.data}})


# create or get all employee
@csrf_exempt
@api_view(['GET', 'POST'])
def employees(request):
    if request.method == "POST":
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        event_serializer = EventSerializer(
            data={"employee": serializer.data["id"], "event_type": 1, "event_date": serializer.data["birth_date"]})
        if event_serializer.is_valid():
            event_serializer.save()
        event_serializer = EventSerializer(
            data={"employee": serializer.data["id"], "event_type": 2, "event_date": serializer.data["joining_date"]})
        if event_serializer.is_valid():
            event_serializer.save()
    else:
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)

    return JsonResponse({"status": "success", "data": {"employees": serializer.data}})


# get all events
def events(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)

    return JsonResponse({"status": "success", "data": {"events": serializer.data}})


# get all templates
def templates(request):
    templates = Template.objects.all()
    serializer = TemplateSerializer(templates, many=True)

    return JsonResponse({"status": "success", "data": {"templates": serializer.data}})


# get all email logs
def email_logs(request):
    email_logs = EmailLog.objects.all()
    serializer = EmailLogSerializer(email_logs, many=True)

    return JsonResponse({"status": "success", "data": {"email_logs": serializer.data}})

