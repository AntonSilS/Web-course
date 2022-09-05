from django.urls import path

from . import views

urlpatterns = [
    path('countfin/', views.index, name='index'),
    path('countfin/edit-categories/', views.edit, name='edit'),
    path('countfin/report/', views.report, name='report'),
    path('countfin/messages/', views.messages, name='messages')
]