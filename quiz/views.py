from rest_framework import generics, permissions
from .models import *
from .serializers import *

from users.perminssions import IsTeacher, IsStudent
from django.utils import timezone


class QuizCreateView(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        serializer.save(create_by=self.request.user)


class QuestionCreateView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]



class AnswerOptionCreateView(generics.CreateAPIView):
    queryset = AnswerOption.objects.all()
    serializer_class = AnswerOptionCreateSerializer
    permissions_classes = [permissions.IsAuthenticated, IsTeacher]


class AvailableQuizListView(generics.ListAPIView):
    serializer_class = QuizDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        user = self.request.user
        now = timezone.now()
        return Quiz.objects.filter(
            is_active=True,
            allowed_students=user,
        )

class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]


class SubmitQuizView(generics.CreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

class SubmissionHistoryView(generics.ListAPIView):
    serializer_class = SubmissionDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Submission.objects.filter(student=self.request.user)


