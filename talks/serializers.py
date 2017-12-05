from rest_framework import serializers

from students.serializers import UserInfoSerializer
from .models import Meetup, Talk


class TalkSerializer(serializers.ModelSerializer):
    author = UserInfoSerializer(read_only=True)
    topic = serializers.CharField(required=True, min_length=3, max_length=500)
    description = serializers.CharField(required=True, min_length=5, max_length=10000)
    votes_count = serializers.SerializerMethodField()
    has_voted = serializers.SerializerMethodField()

    class Meta:
        model = Talk
        fields = ('id', 'author', 'topic', 'description', 'video_url', 'votes_count', 'has_voted') 

    def get_votes_count(self, obj):
        return obj.votes.count()

    def get_has_voted(self, obj):
        return obj.votes.exists(self.context['request'].user.id)

    def create(self, validated_data):
        request = self.context['request']
        author = request.user
        
        meetup = self.context['meetup']

        return Talk.objects.create(meetup=meetup, author=author, **validated_data)


class MeetupSerializer(serializers.ModelSerializer):
    description = serializers.CharField(max_length=10000)
    talks = TalkSerializer(many=True, read_only=True)

    class Meta:
        model = Meetup
        fields = ('id', 'date', 'description', 'talks')
