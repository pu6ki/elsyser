from django.contrib.auth.models import User
from django.contrib.auth import login

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

from .models import Student, Exam


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
            'id', 'username', 'first_name', 'last_name', 'email', 'password',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'read_only': True},
        }


class StudentSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Student
        fields = ('user', 'clazz')

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        first_name = user_data.pop('first_name')
        last_name = user_data.pop('last_name')

        username = first_name + '_' + last_name

        email = user_data.pop('email')

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        user.set_password(user_data.pop('password'))
        user.save()

        Token.objects.create(user=user)

        login(self.context['request'], user)

        return Student.objects.create(user=user, **validated_data)

class StudentLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('user__email', 'clazz')

class ExamsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exam
        fields = ('subject', 'date', 'topic')

    def create(self, validated_data):
        return Exam.objects.filter(
            clazz=self.context['request'].user.student.clazz
        )
