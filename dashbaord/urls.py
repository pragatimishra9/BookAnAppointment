from django.urls import path
from . import views

urlpatterns = [
    path('home',views.HomePageDoctor.as_view(),name="homepagedoctor"),
    path('update_timeslot',views.update_timeslot,name="update_timeslot"),
    path('book_an_appointment',views.book_an_appointment,name="book_an_appointment"),
    path('update_an_appointment',views.update_an_appointment,name="update_an_appointment"),
    path('reports',views.Reports.as_view(),name="reports")
]