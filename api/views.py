from django.shortcuts import render
from api.serializers import UserSerializer,QuestionSerializer,AnswerSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from api.models import Questions,Answers
from rest_framework import authentication,permissions
from rest_framework.decorators import action

# Create your views here.

class UserView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()

class QuestionView(ModelViewSet):
    serializer_class=QuestionSerializer
    queryset=Questions.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["GET"],detail=False)
    def my_questions(self,request,*args,**kw):
        qs=request.user.questions_set.all()
        serializer=QuestionSerializer(qs,many=True)
        return Response(data=serializer.data)
    @action(methods=["post"],detail=True)
    def add_answer(self,request,*args,**kw):
        id=kw.get("pk")
        ques=Questions.objects.get(id=id)
        user=request.user
        serializer=AnswerSerializer(data=request.data,context={"question":ques,"user":user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    @action(methods=["GET"],detail=True)
    def list_answers(self,request,*args,**kw):
            id=kw.get("pk")
            ques=Questions.objects.get(id=id)
            qs=ques.answers_set.all()
            serializer=AnswerSerializer(qs,many=True)
            return Response(data=serializer.data)


class AnswerView(ModelViewSet):
    serializer_class=AnswerSerializer
    queryset=Answers.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    @action(methods=["get"],detail=True)
    def upvote(self,request,*args,**kw):
        ans=self.get_object()
        usr=request.user
        ans.upvote.add(usr)
        return Response(data="created")




