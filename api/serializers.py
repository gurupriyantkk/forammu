from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Questions,Answers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["email","username","password"]
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class QuestionSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Questions
        fields=["title","description","image","user"]

class AnswerSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    created_date=serializers.CharField(read_only=True)
    class Meta:
        model=Answers
        fields=["question","answer","user"]