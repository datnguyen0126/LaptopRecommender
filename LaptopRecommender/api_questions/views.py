from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api_questions.models import Questions, Answers
from api_questions.serializers import AnswerSerializers, QuestionSerializers


class QuestionViewSet(viewsets.GenericViewSet):
    queryset = Questions.objects.select_related('answers')
    serializer_class = QuestionSerializers
    permission_classes = [AllowAny, ]

    def list(self, request):
        question = Questions.objects.all()
        question_serializer = self.get_serializer(question, many=True)
        return Response(question_serializer.data)

    def retrieve(self, request, *args, **kwargs):
        question = Questions.objects.filter(id=kwargs.get('pk')).first()
        question_serializer = self.get_serializer(question)
        return Response(question_serializer.data)


    def create(self, request):
        pass

    def update(self, request):
        pass

    def destroy(self, request):
        pass

