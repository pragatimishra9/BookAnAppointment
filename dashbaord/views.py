from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.views import View
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta, date
from .task import send_appointment_mail


class HomePageDoctor(View):
    def get(self, request):
        if request.user.is_authenticated:
            doctor = Doctor.objects.get(user=User.objects.get(username=request.user))
            appointments = Appointment.objects.all().filter(
                doctor=doctor, appointment_date=date.today()
            )
            total_appointments = Appointment.objects.all().filter(doctor=doctor).count
            remaining_appointments = (
                Appointment.objects.all()
                .filter(doctor=doctor, appointment_status="Open")
                .count
            )
            closed_appointments = (
                Appointment.objects.all()
                .filter(doctor=doctor, appointment_status="Closed")
                .count
            )
            canceled_appointments = (
                Appointment.objects.all()
                .filter(doctor=doctor, appointment_status="Cancelled")
                .count
            )

            time_slots = ["15 Min", "30 Min", "45 Min", "60 Min"]

            data = {
                "time_slots": time_slots,
                "doctor": doctor,
                "appointments": appointments,
                "total": total_appointments,
                "remaining": remaining_appointments,
                "closed": closed_appointments,
                "canceled": canceled_appointments,
            }
            return render(request, "doctor/dashboard.html", data)
        return redirect("/signin")

    def post(self, request):
        pass


@csrf_exempt
def update_timeslot(request):
    if request.method == "POST":
        data = json.load(request)
        start_time = data["start_time"]
        end_time = data["end_time"]
        time_slot = data["time_slot"]
        user = User.objects.get(username=request.user)
        doctor = Doctor.objects.get(user=user)
        doctor.appointment_slot_time = time_slot
        doctor.day_start_time = start_time
        doctor.day_end_time = end_time

        start_time = datetime.strptime(start_time, "%H:%M")
        end_time = datetime.strptime(end_time, "%H:%M")
        time_slot = int(time_slot.split(" ")[0])

        check_time = start_time + timedelta(minutes=time_slot)

        if check_time <= end_time:
            doctor.save()
            return JsonResponse({"status": 200})
        else:
            response = JsonResponse({"status": 403})
            response.status_code = 403
            return response

    else:
        return JsonResponse({"status": 500})


@csrf_exempt
def book_an_appointment(request):
    if request.method == "POST":
        data = json.load(request)
        doctor_id = data["doctor_id"]
        date = data["date"]
        time_slot = data["time_slot"]
        patient_name = data["patient_name"]
        patient_email = (data["patient_email"],)
        patient_contact = data["patient_contact"]

        patient_email = patient_email[0]
        doctor = Doctor.objects.get(pk=doctor_id)

        appointment = Appointment(
            doctor=doctor,
            patient_name=patient_name,
            patient_email=patient_email,
            patient_contact=patient_contact,
            appointment_date=date,
            appointment_time=time_slot,
            appointment_status="Open",
        )
        appointment.save()

        subject = "Appointment Booked For - " + str(date) + " - " + str(time_slot)
        body = (
            "Hi "
            + str(patient_name)
            + "\n\n"
            + "your appointent has been booked successfully...."
        )
        send_appointment_mail.delay(subject, body, patient_email)

        subject = "Appointment Booked For - " + str(date) + " - " + str(time_slot)
        body = (
            "Hi Dr."
            + str(doctor.name)
            + "\n\n"
            + "A Patient have booked an appointment for you, patient details are below \n"
            + "Patient Name: "
            + str(patient_name)
            + "\n"
            + "Patient Contact: "
            + str(patient_contact)
            + "\n"
            + "Date and time: "
            + str(date)
            + " "
            + str(time_slot)
            + "\n\n"
            + "Thank You, \n BookAnAppointment"
        )

        send_appointment_mail.delay(subject, body, doctor.email)
        return JsonResponse({"status": 200})

    else:
        return JsonResponse({"status": 500})


@csrf_exempt
def update_an_appointment(request):
    if request.method == "POST":
        data = json.load(request)
        id = data["id"]
        status = data["status"]

        appointment = Appointment.objects.get(pk=id)
        appointment.appointment_status = status
        appointment.save()
        return JsonResponse({"status": 200})

    else:
        return JsonResponse({"status": 500})


class Reports(View):
    def get(self, request):
        user = User.objects.get(username=request.user)
        doctor = Doctor.objects.all().filter(user=user)[0]
        summary_date = request.GET.get("summary_report_date")
        detailed_date = request.GET.get("detailed_report_date")
        if summary_date != None:
            year, month = summary_date.split("-")
            filter_appoint = (
                Appointment.objects.all()
                .order_by("-id")
                .filter(
                    appointment_date__year=int(year),
                    appointment_date__month=int(month),
                    doctor=doctor,
                )
            )

            summary_report_ls = []
            check = []
            for fa in filter_appoint:
                if fa.appointment_date not in check:
                    check.append(fa.appointment_date)
                    ins = SummaryReport()
                    ins.date = fa.appointment_date
                    ins.no_appointments = len(
                        filter_appoint.filter(appointment_date=fa.appointment_date)
                    )
                    ins.closed_appointments = len(
                        filter_appoint.filter(
                            appointment_date=fa.appointment_date,
                            appointment_status="Closed",
                        )
                    )
                    ins.cancelled_appointments = len(
                        filter_appoint.filter(
                            appointment_date=fa.appointment_date,
                            appointment_status="Cancelled",
                        )
                    )

                    summary_report_ls.append(ins)
        else:
            summary_report_ls = []

        if detailed_date != None:
            year, month = detailed_date.split("-")
            filter_appoint = (
                Appointment.objects.all()
                .order_by("-id")
                .filter(
                    appointment_date__year=int(year),
                    appointment_date__month=int(month),
                    doctor=doctor,
                )
            )
            check = []
            detailed_report_ls = []
            for fa in filter_appoint:
                if fa.appointment_date not in check:
                    check.append(fa.appointment_date)
                    for ains in filter_appoint.filter(
                        appointment_date=fa.appointment_date
                    ):
                        ins = DetailedReport()
                        ins.date = fa.appointment_date
                        ins.patient_name = ains.patient_name
                        ins.status = ains.appointment_status
                        detailed_report_ls.append(ins)
        else:
            detailed_report_ls = []

        data = {
            "summary_report": summary_report_ls,
            "detailed_report": detailed_report_ls,
        }
        appointments = Appointment.objects.all()
        return render(request, "doctor/reports.html", data)
