from rest_framework import serializers
from rest_framework import serializers
from users.models import User
from .models import *


class StudentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        read_only_fields = ['id']


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'text']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'options']


class QuizCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'allowed_students', 'is_active']


class QuizDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'questions']


class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text']


class AnswerOptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'question', 'text', 'is_correct']


class StudentAnswerInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = ['question', 'selected_option']


class SubmissionCreateSerializer(serializers.ModelSerializer):
    answers = StudentAnswerInputSerializer(many=True)

    class Meta:
        model = Submission
        fields = ['quiz', 'answers']

    def validate(self, data):
        user = self.context['request'].user
        if Submission.objects.filter(quiz=data['quiz'], student=user).exists():
            raise serializers.ValidationError('You have already submitted this quiz')
        if not data['quiz'].allowed_students.filter(id=user.id).exists():
            raise serializers.ValidationError('You have not allowed to submit this quiz')
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        answers_data = validated_data.pop('answers')
        submission = Submission.objects.create(student=user, **validated_data)

        for answer in answers_data:
            StudentAnswer.objects.create(
                submission=submission,
                question=answer['question'],
                selected_option=answer['selected_option']
            )
        return submission


class StudentAnswerDetailSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.text', read_only=True)
    selected_text = serializers.CharField(source='selected_option.text', read_only=True)
    is_correct = serializers.SerializerMethodField()

    class Meta:
        model = StudentAnswer
        fields = ['question_text', 'selected_text', 'is_correct']

    def get_is_correct(self, obj):
        return obj.selected_option.is_correct


class SubmissionDetailSerializer(serializers.ModelSerializer):
    quiz = serializers.StringRelatedField()
    answers = StudentAnswerDetailSerializer(many=True)
    total_correct = serializers.SerializerMethodField()
    total_questions = serializers.SerializerMethodField()
    score_percent = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = ['id', 'quiz', 'answers', 'submitted_at', 'total_correct', 'total_questions', 'score_percent']

    def get_total_correct(self, obj):
        return obj.answers.filter(selected_option__is_correct=True).count()

    def get_total_questions(self, obj):
        return obj.answers.count()

    def get_score_percent(self, obj):
        total = self.get_total_questions(obj)
        correct = self.get_total_correct(obj)
        return round((correct / total) * 100, 2) if total > 0 else 0.0
