from rest_framework import serializers

from .models import Exam


class ExamsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exam
        fields = ('id', 'subject', 'date', 'clazz', 'topic')

    def create(self, validated_data):
        subject = validated_data.pop('subject')
        clazz = validated_data.pop('clazz')

        return Exam.objects.create(
            subject=subject,
            clazz=clazz,
            **validated_data
        )
