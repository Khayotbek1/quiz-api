from django.urls import path
from .views import *

urlpatterns = [
    path('quizzes/create/', QuizCreateView.as_view()),
    path('questions/create/', QuizCreateView.as_view()),
    path('options/create/', AnswerOptionCreateView.as_view()),

    path('quizzes/available/', AvailableQuizListView.as_view()),
    path('quizzes/<int:pk>/', QuizDetailView.as_view()),
    path('submit/', SubmitQuizView.as_view()),
    path('submissions/', SubmissionHistoryView.as_view()),
]