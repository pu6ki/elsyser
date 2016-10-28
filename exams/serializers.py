from rest_framework import serializers

from .models import Exam


class ExamsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exam
        fields = ('id', 'subject', 'date', 'clazz', 'topic')

    def create(self, validated_data):
        return Exam.objects.create(**validated_data)
