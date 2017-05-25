from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from students.serializers import ClassSerializer, SubjectSerializer, TeacherAuthorSerializer
from .models import Exam


class ExamSerializer(serializers.ModelSerializer):
    topic = serializers.CharField(
        max_length=60,
        validators=[
            UniqueValidator(
                queryset=Exam.objects.all(),
                message='Exam with this topic already exists.'
            )
        ]
    )
    details = serializers.CharField(max_length=1000, allow_blank=True)

    class Meta:
        model = Exam
        fields = (
            'id', 'subject', 'clazz', 'topic', 'date', 'details', 'author'
        )
        depth = 1

    def create(self, validated_data):
        request = self.context['request']
        author = request.user.teacher
        subject = author.subject

        return Exam.objects.create(
            subject=subject, author=author, **validated_data
        )

    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()

        return instance


class ExamReadSerializer(ExamSerializer):
    subject = SubjectSerializer(read_only=True)
    clazz = ClassSerializer(read_only=True)
    author = TeacherAuthorSerializer(read_only=True)
