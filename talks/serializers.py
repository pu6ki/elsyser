from rest_framework import serializers

from students.serializers import UserInfoSerializer
from .models import Talk


class TalksSerializer(serializers.ModelSerializer):
    author = UserInfoSerializer(read_only=True)
    topic = serializers.CharField(required=True, max_length=500)
    description = serializers.CharField(required=True, max_length=10000)

    class Meta:
        model = Talk
        fields = ('id', 'author', 'topic', 'description', 'date', 'video_url', 'num_vote_up') 

    def create(self, validated_data):
        request = self.context['request']
        author = request.user

        return Talk.objects.create(author=author, **validated_data)
