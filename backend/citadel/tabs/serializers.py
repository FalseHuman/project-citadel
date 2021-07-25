from rest_framework import serializers
from .models import *


class PaysSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username')

    class Meta:
        model = Pays
        fields = ('id', 'title', 'body', 'cost', 'data',
                  'type_of_pays', 'month', 'author_name')

    def create(self, validated_data):
        author = validated_data['author']
        validated_data['author'] = User.objects.get(
            username=author['username'])
        return Pays.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    pays = PaysSerializer(many=True, read_only=True)

    class Meta:
        model = User
        depth = 1
        fields = ('username', 'photo', 'first_name',
                  'last_name', 'email', 'photo', 'pays')
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'},
        }


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'photo')
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.username = validated_data['username']
        instance.email = validated_data['email']
        instance.photo = validated_data['photo']

        instance.save()

        return instance
