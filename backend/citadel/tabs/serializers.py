from re import template
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import PKOnlyObject
from collections import OrderedDict
from .models import *


class TemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Templates
        fields = ['body_template']

    def create(self, validated_data):
        validated_data['person'] = self.context['request'].user
        return Templates.objects.create(**validated_data)


class NotesSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(NotesSerializer, self).__init__(*args, **kwargs)

        if 'labels' in self.fields:
            raise RuntimeError(
                'You cant have labels field defined '
                'while using MyModelSerializer'
            )

        self.fields['labels'] = SerializerMethodField()

    def get_labels(self, *args):
        labels = {}

        for field in self.Meta.model._meta.get_fields():
            if field.name in self.fields:
                labels[field.name] = field.verbose_name

        return labels
    class Meta:
        model = Notes
        fields = ('id', 'title', 'body')

    def create(self, validated_data):
        validated_data['person'] = self.context['request'].user
        return Notes.objects.create(**validated_data)


class PaysSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(PaysSerializer, self).__init__(*args, **kwargs)

        if 'labels' in self.fields:
            raise RuntimeError(
                'You cant have labels field defined '
                'while using MyModelSerializer'
            )

        self.fields['labels'] = SerializerMethodField()

    def get_labels(self, *args):
        labels = {}

        for field in self.Meta.model._meta.get_fields():
            if field.name in self.fields and field.name not in ['month', 'id']:
                labels[field.name] = field.verbose_name

        return labels
    class Meta:
        model = Pays
        fields = ('id', 'title', 'body', 'cost', 'data',
                  'type_of_pays', 'month')


    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return Pays.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)

        if 'labels' in self.fields:
            raise RuntimeError(
                'You cant have labels field defined '
                'while using MyModelSerializer'
            )

        self.fields['labels'] = SerializerMethodField()

    def get_labels(self, *args):
        labels = {}

        for field in self.Meta.model._meta.get_fields():
            if field.name in self.fields:
                labels[field.name] = field.verbose_name

        return labels
    class Meta:
        model = User
        fields = ('username', 'photo', 'first_name',
                  'last_name', 'email', 'photo', 'email_send')


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email_send', 'email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def update(self, instance, validated_data):
        if 'email' in validated_data:
            try:
                user = User.objects.get(email=validated_data['email'])
                if instance.username != user.username:
                    raise serializers.ValidationError(
                        {'email': 'Этот email уже используется'})
            except User.DoesNotExist:
                pass
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["photo"]

    def save(self, *args, **kwargs):
        if self.instance.photo:
            self.instance.photo.delete()
        return super().save(*args, **kwargs)


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
