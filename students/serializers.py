import re

import requests

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.validators import validate_email, ValidationError

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Class, Subject, Student, Teacher, Grade
from .utils import send_verification_email, generate_activation_key


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=3,
        max_length=30,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='User with this username already exists.'
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
                message='User with this email already exists.'
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
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def validate_username(self, username):
        pattern = re.compile(r'^(?=.*[a-z])[a-z0-9]+$')

        if not pattern.match(username):
            raise serializers.ValidationError(
                'Username should be present with alphanumeric characters.'
            )

        return username


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

        try:
            validate_email(email_or_username)
            user_request = User.objects.get(email=email_or_username)
            email_or_username = user_request.username
        except (ValidationError, User.DoesNotExist):
            pass

        user = authenticate(username=email_or_username, password=password)

        if not user:
            raise serializers.ValidationError('Unable to log in with provided credentials.')

        attrs['user'] = user

        return attrs


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ('__all__')


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    clazz = ClassSerializer()

    class Meta:
        model = Student
        fields = ('user', 'clazz')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data['user'], is_active=False)

        clazz, _ = Class.objects.get_or_create(**validated_data['clazz'])

        activation_key = generate_activation_key()
        student = Student.objects.create(user=user, clazz=clazz, activation_key=activation_key)

        send_verification_email(user)

        return student


class UserInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=3, max_length=30)
    first_name = serializers.CharField(min_length=3, max_length=30)
    last_name = serializers.CharField(min_length=3, max_length=30)
    email = serializers.EmailField(read_only=True, max_length=100)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

    def update(self, instance, validated_data):
        username = validated_data.get('username', '')

        if User.objects.exclude(pk=instance.pk).filter(username=username):
            raise serializers.ValidationError('User with this username already exists.')

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
        fields = ('__all__')


class DefaultProfileSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    profile_image_url = serializers.URLField(allow_blank=False)

    def validate_profile_image_url(self, value):
        response = requests.head(value)
        content_type = response.headers.get('content-type')

        if not content_type.startswith('image/'):
            raise serializers.ValidationError('URL is not a picture.')

        return value

    def update(self, instance, validated_data):
        user_data = validated_data.get('user', {})
        username = user_data.get('username', '')

        if User.objects.exclude(pk=instance.user.pk).filter(username=username):
            raise serializers.ValidationError('User with this username already exists.')

        instance.user.__dict__.update(**user_data)
        instance.user.save()

        instance.__dict__.update(**validated_data)
        instance.save()

        return instance


class StudentProfileSerializer(DefaultProfileSerializer):
    clazz = ClassSerializer()

    class Meta:
        model = Student
        fields = ('__all__')


class TeacherProfileSerializer(DefaultProfileSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = Teacher
        fields = ('__all__')


class DefaultAuthorSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)


class StudentAuthorSerializer(DefaultAuthorSerializer):
    clazz = ClassSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ('__all__')


class TeacherAuthorSerializer(DefaultAuthorSerializer):
    class Meta:
        model = Teacher
        fields = ('__all__')


class GradesSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = Grade
        fields = ('__all__')

    def create(self, validated_data):
        subject = self.context['subject']
        student = self.context['student']

        return Grade.objects.create(subject=subject, student=student, **validated_data)
