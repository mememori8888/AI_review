from django.db import models
import datetime

class AIReview(models.Model):
    question = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(default=datetime.datetime.now)

def __str__(self):
    return self.question[:50] # 表示用に短縮