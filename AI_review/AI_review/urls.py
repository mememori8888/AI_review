from django.urls import path
from . import views

urlpatterns = [
path('', views.ai_review_list, name='ai_review_list'),
]