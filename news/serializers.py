from django.contrib.auth.models import User

from rest_framework import serializers

from students.serializers import UserInfoSerializer

from .models import News, Comment


class AbstractPostSerializer(serializers.ModelSerializer):
    author = UserInfoSerializer(read_only=True)

    class Meta:
        fields = ('author', 'posted_on', 'edited', 'last_edited_on')


class CommentSerializer(AbstractPostSerializer):
    author_image = serializers.SerializerMethodField()
    content = serializers.CharField(max_length=2048)

    class Meta:
        model = Comment
        fields = AbstractPostSerializer.Meta.fields + ('id', 'author_image', 'content')

    def get_author_image(self, obj):
        author = obj.author

        try:
            field = author.student
        except AttributeError:
            field = author.teacher

        return field.profile_image_url

    def create(self, validated_data):
        news = self.context['news']
        request = self.context['request']

        author = request.user

        return Comment.objects.create(news=news, author=author, **validated_data)


class CommentReadSerializer(CommentSerializer):
    author = UserInfoSerializer(read_only=True)


class NewsSerializer(AbstractPostSerializer):
    title = serializers.CharField(min_length=3, max_length=100)
    content = serializers.CharField(min_length=5, max_length=10000)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = News
        fields = AbstractPostSerializer.Meta.fields + (
            'id', 'title', 'content', 'class_number', 'class_letter', 'comments'
        )

    def create(self, validated_data):
        author = self.context['request'].user
        validated_data['class_number'] = self.context['class_number']
        validated_data['class_letter'] = self.context.get('class_letter', '')

        news = News.objects.create(author=author, **validated_data)

        return news
