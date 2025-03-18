from django.db import models
import datetime

class BaseAIReview(models.Model):
    question = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        abstract = True
        managed = False
        db_table = 'responses'

    def __str__(self):
        return self.question[:50]

class ProgrammingReview(BaseAIReview):
    class Meta(BaseAIReview.Meta):
        db_table = 'responses'

class BrainKnockReview(BaseAIReview):
    class Meta(BaseAIReview.Meta):
        db_table = 'responses'

class BusinessReview(BaseAIReview):
    class Meta(BaseAIReview.Meta):
        db_table = 'responses'

class ParseReview(BaseAIReview):
    class Meta(BaseAIReview.Meta):
        db_table = 'responses'

class MailReview(BaseAIReview):
    class Meta(BaseAIReview.Meta):
        db_table = 'responses'

class RecipeReview(BaseAIReview):
    class Meta(BaseAIReview.Meta):
        db_table = 'responses'

class TranslationReview(BaseAIReview):
    class Meta(BaseAIReview.Meta):
        db_table = 'responses'

class YoutubeReview(BaseAIReview):
    class Meta(BaseAIReview.Meta):
        db_table = 'responses'

# データベースとモデルのマッピング
DATABASE_MODELS = {
    'default': ProgrammingReview,
    'brain_knock': BrainKnockReview,
    'business': BusinessReview,
    'parse': ParseReview,
    'mail': MailReview,
    'recipe': RecipeReview,
    'translation': TranslationReview,
    'youtube': YoutubeReview,
}

# データベース名と表示名のマッピング
DATABASE_LABELS = {
    'default': 'プログラミング',
    'brain_knock': 'ブレインノック',
    'business': 'ビジネス提案',
    'parse': 'HTML解析',
    'mail': 'ビジネスメール',
    'recipe': 'レシピ',
    'translation': '翻訳',
    'youtube': 'YouTube要約',
}

# database_names = [
#     "gemini_brain_knock",
#     "gemini_business_sujest",
#     "gemini_parse",
#     "gemini_mail",
#     "gemini_programming",
#     'gemini_recipe',
#     'gemini_translation',
#     'gemini_youtube',
# ]