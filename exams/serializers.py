from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.generics import get_object_or_404

from students.serializers import ClassSerializer, SubjectSerializer, TeacherAuthorSerializer
from students.models import Class

from .models import Exam


class ExamSerializer(serializers.ModelSerializer):
    topic = serializers.CharField(
        required=True,
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
        fields = ('__all__')
        depth = 1

    def create(self, validated_data):
        request = self.context['request']

        author = request.user.teacher
        subject = author.subject

        clazz = get_object_or_404(Class, **self.context['clazz_data'])

        return Exam.objects.create(subject=subject, author=author, clazz=clazz, **validated_data)


class ExamReadSerializer(ExamSerializer):
    subject = SubjectSerializer(read_only=True)
    clazz = ClassSerializer(read_only=True)
    author = TeacherAuthorSerializer(read_only=True)
