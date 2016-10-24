from django.contrib.auth.models import User, Group
from django.contrib.auth import login

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token


class StudentSerializer(serializers.ModelSerializer):

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

    def create(self, validated_data):
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')

        username = first_name + '_' + last_name

        email = validated_data.pop('email')

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        user.set_password(validated_data.pop('password'))

        user.save()

        Group.objects.get(name='Students').user_set.add(user)
        Token.objects.create(user=user)

        login(self.context['request'], user)

        return user
