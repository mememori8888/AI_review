from django.urls import path
from . import views

app_name = 'AI_review'

urlpatterns = [
    path('', views.review_list, name='review_list'),
]