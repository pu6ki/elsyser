from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.core.validators import validate_email, ValidationError

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

from .models import Class, Subject, Student, Exam, News, Homework, Comment


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=3,
        max_length=30,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Student with this username already exists.'
            )
        ]
    )
    first_name = serializers.CharField(min_length=3, max_length=30)
    last_name = serializers.CharField(min_length=3, max_length=30)
    email = serializers.EmailField(
        max_length=100,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Student with this email already exists.'
            )
        ],
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=6,
        style={'input_type': 'password'},
        error_messages={
            'blank': 'Password cannot be empty.',
            'min_length': 'Password too short.',
        },
    )


    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password',
        )


class UserLoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )


    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        if email_or_username and password:
            try:
                validate_email(email_or_username)
                user_request = get_object_or_404(User, email=email_or_username)
                email_or_username = user_request.username
            except ValidationError:
                pass

            user = authenticate(username=email_or_username, password=password)

            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg)
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "email or username" and "password"'
            raise serializers.ValidationError(msg)

        attrs['user'] = user

        return attrs


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ('number', 'letter')


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    clazz = ClassSerializer()


    class Meta:
        model = Student
        fields = ('user', 'clazz')
        depth = 1


    def save(self):
        user = User.objects.create_user(**self.validated_data['user'])
        Token.objects.create(user=user)
        self.validated_data['user'] = user

        clazz, _ = Class.objects.get_or_create(**self.validated_data['clazz'])
        self.validated_data['clazz'] = clazz

        return Student.objects.create(**self.validated_data)


class UserInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=3, max_length=30)
    first_name = serializers.CharField(min_length=3, max_length=30)
    last_name = serializers.CharField(min_length=3, max_length=30)
    email = serializers.EmailField(read_only=True, max_length=100)


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


    def update(self, instance, validated_data):
        username = validated_data.get('username', '')

        if User.objects.exclude(pk=instance.pk).filter(username=username):
            raise serializers.ValidationError(
                'Teacher with this username already exists.'
            )

        instance.__dict__.update(**validated_data)
        instance.save()

        return instance


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    clazz = ClassSerializer()
    profile_image = serializers.ImageField(use_url=True)


    class Meta:
        model = Student
        fields = ('user', 'clazz', 'profile_image', 'info')
        depth = 1


    def update(self, instance, validated_data):
        user_data = validated_data.get('user', {})
        username = user_data.get('username', '')

        if User.objects.exclude(pk=instance.user.pk).filter(username=username):
            raise serializers.ValidationError(
                'Student with this username already exists.'
            )

        instance.user.__dict__.update(**user_data)
        instance.user.save()

        instance.__dict__.update(**validated_data)
        instance.save()

        return instance


class SubjectSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=50,
        allow_blank=False,
        validators=[
            UniqueValidator(
                queryset=Subject.objects.all(),
                message='Subject with this title already exists.'
            )
        ]
    )


    class Meta:
        model = Subject
        fields = ('title',)


class StudentAuthorSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    profile_image = serializers.ImageField(use_url=True)


    class Meta:
        model = Student
        fields = ('user', 'profile_image')


class TeacherAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class ExamSerializer(serializers.ModelSerializer):
    topic = serializers.CharField(
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
        fields = ('id', 'subject', 'clazz', 'topic', 'date', 'details', 'author')
        depth = 1


    def create(self, validated_data):
        request = self.context['request']
        author = request.user

        return Exam.objects.create(author=author, **validated_data)


    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()

        return instance


class ExamReadSerializer(ExamSerializer):
    subject = SubjectSerializer(read_only=True)
    clazz = ClassSerializer(read_only=True)
    author = TeacherAuthorSerializer(read_only=True)


class CommentSerializer(serializers.ModelSerializer):
    posted_by = StudentAuthorSerializer(read_only=True)
    content = serializers.CharField(max_length=2048)


    class Meta:
        model = Comment
        fields = (
            'id',
            'posted_by', 'content',
            'posted_on',
            'edited', 'last_edited_on'
        )
        depth = 1


    def create(self, validated_data):
        news = self.context['news']

        request = self.context['request']
        posted_by = request.user.student


        return Comment.objects.create(
            news=news, posted_by=posted_by, **validated_data
        )


    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()

        return instance


class NewsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=3, max_length=100)
    content = serializers.CharField(min_length=5, max_length=10000)
    author = StudentAuthorSerializer(read_only=True)
    comment_set = CommentSerializer(read_only=True, many=True)


    class Meta:
        model = News
        fields = (
            'id',
            'title', 'content',
            'posted_on', 'author',
            'comment_set',
            'edited', 'last_edited_on'
        )
        depth = 2


    def create(self, validated_data):
        request = self.context['request']
        author = request.user.student

        return News.objects.create(author=author, **validated_data)


    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()

        return instance


class HomeworkSerializer(serializers.ModelSerializer):
    details = serializers.CharField(max_length=256, allow_blank=True)


    class Meta:
        model = Homework
        fields = ('id', 'subject', 'clazz', 'deadline', 'details', 'author')
        depth = 1


    def create(self, validated_data):
        request = self.context['request']
        author = request.user

        return Homework.objects.create(author=author, **validated_data)


    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()

        return instance


class HomeworkReadSerializer(HomeworkSerializer):
    subject = SubjectSerializer(read_only=True)
    clazz = ClassSerializer(read_only=True)
    author = TeacherAuthorSerializer(read_only=True)
