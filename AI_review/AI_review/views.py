from django.shortcuts import render
from django.core.paginator import Paginator
from .models import DATABASE_MODELS, DATABASE_LABELS

def ai_review_list(request):
    reviews = AIReview.objects.all()
    context = {'reviews': reviews}
    return render(request, 'ai_review/list.html', context)

def review_list(request):
    # データベースの選択（デフォルトは'default'）
    selected_db = request.GET.get('database', 'default')
    
    # 選択されたデータベースに対応するモデルを取得
    model = DATABASE_MODELS[selected_db]
    
    # データの取得
    reviews = model.objects.using(selected_db).all().order_by('-timestamp')
    
    # ページネーション（1ページあたり10件）
    paginator = Paginator(reviews, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'databases': DATABASE_LABELS.items(),
        'selected_db': selected_db,
        'current_db_label': DATABASE_LABELS[selected_db],
    }
    
    return render(request, 'AI_review/review_list.html', context)