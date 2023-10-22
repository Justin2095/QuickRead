from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile_url = serializers.HyperlinkedIdentityField(
        view_name='profile-detail')

    class Meta:
        model = User
        depth = 1
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email',
                  'profile', 'profile_url')


class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        depth = 1
        model = Subject
        fields = ('url', 'id', 'name', 'hours_per_week', 'user')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user_url = serializers.HyperlinkedIdentityField(view_name='user-detail')
    user = serializers.ReadOnlyField(source='user.id')
    id = serializers.IntegerField(source='pk', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Profile
        depth = 1
        fields = ('url', 'id', 'username', 'email', 'first_name', 'last_name',
                  'about', 'user', 'user_url')

    def get_full_name(self, obj):
        request = self.context['request']
        return request.user.get_full_name()

    def update(self, instance, validated_data):
        # pobiera User
        user_data = validated_data.pop('user', None)
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)

        # pobiera Profile
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.user.save()
        instance.save()
        return instance


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    subject = serializers.ReadOnlyField(source='subject.name')

    class Meta:
        depth = 1
        model = Article
        fields = ('url', 'id', 'article_title', 'article_author',
                  'article_summary', 'article_content', 'subject')


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    subject = serializers.ReadOnlyField(source='subject.name')

    class Meta:
        depth = 1
        model = Topic
        fields = ('url', 'id', 'name', 'subject')


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    topic = serializers.ReadOnlyField(source='topic.name')

    class Meta:
        depth = 1
        model = Note
        fields = ('url', 'id', 'title', 'content', 'topic')


class FlashcardSerializer(serializers.HyperlinkedModelSerializer):
    subject = serializers.ReadOnlyField(source='subject.name')

    class Meta:
        depth = 1
        model = Flashcard
        fields = ('url', 'id', 'term', 'definition', 'subject')