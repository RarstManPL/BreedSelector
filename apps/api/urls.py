from django.urls import path, include

from . import views

app_name = 'api'
urlpatterns = [
    path('breeds/predict/', views.predict_breed, name='predict_breed'),
    path('models/character/create/', views.character_model_create, name='character_model_create'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
