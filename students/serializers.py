from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils.six import BytesIO

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser

from .models import Class, Subject, Student, Exam, News


class ClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        fields = ('number', 'letter')


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ('title',)


class ExamSerializer(serializers.ModelSerializer):

    subject = SubjectSerializer()

    class Meta:
        model = Exam
        fields = ('subject', 'topic', 'date')


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ('title', 'content', 'date')


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=6,
        style={
            'input_type': 'password',
        },
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
            'password': {'write_only': True},
        }


class StudentSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    clazz = ClassSerializer()

    class Meta:
        model = Student
        fields = ('user', 'clazz')

    def save(self):
        user_data = self.validated_data['user']

        first_name = user_data['first_name']
        last_name = user_data['last_name']
        username = first_name + '_' + last_name
        email = user_data['email']

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        user.set_password(user_data['password'])
        user.save()

        Token.objects.create(user=user)

        login(self.context['request'], user)
        self.validated_data['user'] = user

        clazz, _ = Class.objects.get_or_create(**self.validated_data['clazz'])
        self.validated_data['clazz'] = clazz

        return Student.objects.create(**self.validated_data)


class StudentProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    clazz = ClassSerializer()

    class Meta:
        model = Student
        fields = ('user', 'clazz')
