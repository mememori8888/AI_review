from django.contrib import admin
from .models import (
    ProgrammingReview,
    BrainKnockReview,
    BusinessReview,
    ParseReview,
    MailReview,
    RecipeReview,
    TranslationReview,
    YoutubeReview,
    
)

class AIReviewAdmin(admin.ModelAdmin):
    list_display = ('question', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('question', 'response')
    ordering = ('-timestamp',)

# 各モデルを同じ管理クラスで登録
admin.site.register(ProgrammingReview, AIReviewAdmin)
admin.site.register(BrainKnockReview, AIReviewAdmin)
admin.site.register(BusinessReview, AIReviewAdmin)
admin.site.register(ParseReview, AIReviewAdmin)
admin.site.register(MailReview, AIReviewAdmin)
admin.site.register(RecipeReview, AIReviewAdmin)
admin.site.register(TranslationReview, AIReviewAdmin)
admin.site.register(YoutubeReview, AIReviewAdmin)
