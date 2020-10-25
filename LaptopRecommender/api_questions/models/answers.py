from django.db import models
from api_questions.models.questions import Questions


class Answers(models.Model):
    content = models.CharField(max_length=255, blank=True, null=True)
    question = models.ForeignKey(Questions, related_name='question', on_delete=models.CASCADE)

    class Meta:
        db_table = 'answers'