from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.core.validators import validate_email, ValidationError

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

from .models import Class, Subject, Student, Exam, News, Homework


class UserSerializer(serializers.ModelSerializer):

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

    email = serializers.EmailField(
        max_length=100,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Student with this email already exists.'
            )
        ],
    )


    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password',
        )
        extra_kwargs = {
            'username': {'read_only': True},
            'password': {'write_only': True}
        }


class UserLoginSerializer(serializers.Serializer):

    email_or_username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})


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


    def save(self):
        user_data = self.validated_data['user']
        user_data['username'] = user_data['first_name'] + '_' + user_data['last_name']

        user = User.objects.create_user(**user_data)
        Token.objects.create(user=user)
        self.validated_data['user'] = user

        clazz, _ = Class.objects.get_or_create(**self.validated_data['clazz'])
        self.validated_data['clazz'] = clazz

        return Student.objects.create(**self.validated_data)


class StudentProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    clazz = ClassSerializer()


    class Meta:
        model = Student
        fields = ('user', 'clazz', 'profile_image')


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ('title',)


class ExamSerializer(serializers.ModelSerializer):

    subject = SubjectSerializer()


    class Meta:
        model = Exam
        fields = ('subject', 'topic', 'date')


class AuthorSerializer(serializers.ModelSerializer):

    username = serializers.CharField()


    class Meta:
        model = User
        fields = ('username',)


class NewsSerializer(serializers.ModelSerializer):

    title = serializers.CharField(min_length=3, max_length=60)
    content = serializers.CharField(min_length=5, max_length=1000)


    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'posted_on', 'author')
        depth = 1


    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        return News.objects.create(author=user, **validated_data)


class HomeworkSerializer(serializers.ModelSerializer):

    subject = SubjectSerializer()
    clazz = ClassSerializer()
    details = serializers.CharField(allow_blank=True)
    materials = serializers.FileField(use_url=False)


    class Meta:
        model = Homework
        fields = ('subject', 'clazz', 'deadline', 'details', 'materials')
