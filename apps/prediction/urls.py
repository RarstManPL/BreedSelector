from django.urls import path

from . import views

app_name = 'prediction'
urlpatterns = [
    path('form', views.form, name='form'),
    path('result', views.result, name='result'),
]
