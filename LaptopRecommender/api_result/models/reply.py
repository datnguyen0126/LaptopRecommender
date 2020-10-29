from django.db import models

from api_questions.models import Answers


class Reply(models.Model):
    content = models.TextField(blank=True, null=True)
    answer = models.ForeignKey(Answers, related_name='option', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reply'

