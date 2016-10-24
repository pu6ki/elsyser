from django.contrib.auth.models import User, Group
from rest_framework import serializers


class StudentSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=6,
        style={
            'input_type': 'password'
        },
        error_messages={
            "blank": "Password cannot be empty.",
            "min_length": "Password too short.",
        },
    )

    class Meta:
        model = User
        fields = (
            'id', 'username', 'password', 'first_name', 'last_name', 'email',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'read_only': True},
        }

    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']

        username = first_name + '_' + last_name

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])

        user.save()
        Group.objects.get(name='Students').user_set.add(user)

        return user
