from celery import shared_task
from time import sleep
from django.core.mail import send_mail

@shared_task
def sleepy(duration):
    sleep(duration)
    return None


@shared_task
def send_appointment_mail(subject,body,reciever):
    send_mail(subject,body,'neuron9889@gmail.com',[reciever],fail_silently=False)