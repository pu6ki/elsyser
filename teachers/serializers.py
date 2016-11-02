from rest_framework import serializers

from students.models import Exam


class ExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exam
        fields = ('subject', 'topic', 'clazz', 'date')

    def save(self):
        return Exam.objects.create(**self.validated_data)

    def update(self, instance, validated_data):
        instance.subject = validated_data.get('subject', instance.subject)
        instance.topic = validated_data.get('topic', instance.topic)
        instance.clazz = validated_data.get('clazz', instance.clazz)
        instance.date = validated_data.get('date', instance.date)

        return instance
