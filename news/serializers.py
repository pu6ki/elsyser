from rest_framework import serializers

from students.serializers import UserInfoSerializer

from .models import News, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = UserInfoSerializer(read_only=True)
    author_image = serializers.SerializerMethodField()
    content = serializers.CharField(max_length=2048)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'author_image', 'content', 'posted_on', 'edited', 'last_edited_on')

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


class NewsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=3, max_length=100)
    content = serializers.CharField(min_length=5, max_length=10000)
    author = UserInfoSerializer(read_only=True)
    comment_set = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = News
        fields = ('__all__')

    def create(self, validated_data):
        author = self.context['request'].user
        validated_data['class_number'] = self.context['class_number']
        validated_data['class_letter'] = self.context.get('class_letter', '')

        return News.objects.create(author=author, **validated_data)
