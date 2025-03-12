from django.shortcuts import render
from .models import AIReview

def ai_review_list(request):
    reviews = AIReview.objects.all()
    context = {'reviews': reviews}
    return render(request, 'ai_review/list.html', context)