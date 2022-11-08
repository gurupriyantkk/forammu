from django.shortcuts import render
from api.serializers import UserSerializer,QuestionSerializer,AnswerSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from api.models import Questions
from rest_framework import authentication,permissions
from rest_framework.decorators import action

# Create your views here.

class UserView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()

class QuestionView(ModelViewSet):
    serializer_class=QuestionSerializer
    queryset=User.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["GET"],detail=False)
    def my_questions(self,request,*args,**kw):
        qs=request.user.questions_set.all()
        serializer=QuestionSerializer(qs,many=True)
        return Response(data=serializer.data)

    def add_answer(self,request,*args,**kw):
        id=kw.get("pk")
        ques=Questions.objects.get(id=id)
        user=request.user
        serializer=AnswerSerializer(data=serializer.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)