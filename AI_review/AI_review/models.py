from django.db import models
import datetime

class AIReview(models.Model):
    question = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False  # 既存のテーブルを使用することを示す
        db_table = 'responses'  # 実際のテーブル名を指定

def __str__(self):
    return self.question[:50] # 表示用に短縮