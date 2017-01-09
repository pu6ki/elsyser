from rest_framework import serializers

from materials.models import Material
from students.serializers import SubjectSerializer, TeacherAuthorSerializer


class MaterialSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=3, max_length=150, allow_blank=True)
    section = serializers.CharField(min_length=3, max_length=150, allow_blank=True)
    content = serializers.CharField(allow_blank=False)
    subject = SubjectSerializer(read_only=True)
    video_url = serializers.URLField(allow_blank=True)


    class Meta:
        model = Material
        fields = (
            'id',
            'title', 'section', 'content',
            'class_number', 'subject',
            'video_url',
            'author'
        )
        depth = 1


    def create(self, validated_data):
        subject = self.context['subject']

        request = self.context['request']
        author = request.user.teacher

        return Material.objects.create(
            subject=subject, author=author, **validated_data
        )


    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()

        return instance


class MaterialReadSerializer(MaterialSerializer):
    author = TeacherAuthorSerializer(read_only=True)
