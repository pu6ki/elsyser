from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from notifications.signals import notify

from students.models import Class
from students.serializers import ClassSerializer, SubjectSerializer, TeacherAuthorSerializer

from .models import Exam


class ExamSerializer(serializers.ModelSerializer):
    clazz = ClassSerializer()
    topic = serializers.CharField(required=True, max_length=60)
    details = serializers.CharField(max_length=10000, allow_blank=True, required=False)

    class Meta:
        model = Exam
        fields = ('id', 'subject', 'date', 'clazz', 'topic', 'details', 'author')
        depth = 1

    def create(self, validated_data):
        request = self.context['request']

        author = request.user.teacher
        subject = author.subject
        clazz = get_object_or_404(Class, **validated_data.pop('clazz'))

        exam = Exam.objects.create(subject=subject, author=author, clazz=clazz, **validated_data)

        recipient_list = User.objects.filter(student__clazz=clazz)
        notify.send(exam, recipient=recipient_list, verb=' was created.')

        return exam

    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()

        return instance


class ExamReadSerializer(ExamSerializer):
    subject = SubjectSerializer(read_only=True)
    clazz = ClassSerializer(read_only=True)
    author = TeacherAuthorSerializer(read_only=True)
