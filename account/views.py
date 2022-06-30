from datetime import datetime
import os
from .serializers import LoginSerializer, PostSerializer, RegisterSerializer, VoteSerializer
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import  PostSerializer
from .models import Post, Vote
from rest_framework.permissions import IsAuthenticated, AllowAny

class get_posts(APIView):
    def get(self, request):
        posts = Post.objects.filter(id=1).first()
        serializer = PostSerializer(posts)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data    
            print('########1', data)
            serializer = LoginSerializer(data=request.data)
            print('#######3',serializer)
            context={ 'request': self.request }
            if serializer.is_valid(raise_exception=True):
                user_obj = User.objects.filter(email=data.get('email')).first()    
                token_obj, created = Token.objects.get_or_create(user=user_obj)
                print('yes####')
                return Response({'status_code':status.HTTP_200_OK,'status_message':'Success','session_token':token_obj.key})
                

        except Exception as e:
            return Response({'status_code':status.HTTP_500_INTERNAL_SERVER_ERROR,'status_message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'key':'value'})

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        try:
                token_obj=Token.objects.filter(key=self.request.POST.get('session_token')).first()
                token_obj.delete()  
                return Response({"status": "success logout token"})
        except Exception as e:
            return Response({'status_code':status.HTTP_500_INTERNAL_SERVER_ERROR,'status_message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RegisterView(APIView):
    permission_classes = [AllowAny]
    # serializer_class = RegisterSerializer

    def post(self,request,*args,**kwargs):
        try:
            data=request.data
            request.data._mutable = True
            request.data['username'] = request.data.get('email')
            request.data._mutable = False
            # data.update({'username': data.get('email')})
            serializer = RegisterSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status_code':status.HTTP_200_OK,'status_message':'Success register saved'})
            else:
                return Response({'status_code':status.HTTP_200_OK,'status_message':serializer.errors})
        except Exception as e:
            return Response({'status_code':status.HTTP_500_INTERNAL_SERVER_ERROR,'status_message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,*args,**kwargs):
        try:
            from datetime import datetime
            
            data = request.data
            request.data._mutable = True
            request.data['user'] = request.user.id
            request.data._mutable = False
            print('hello ######')

            serializer = PostSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()


            return Response({'status_code':status.HTTP_200_OK,'status_message':'Success post created', 'data':serializer.data})
        except Exception as e:
            return Response({'status_code':status.HTTP_500_INTERNAL_SERVER_ERROR,'status_message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request, pk, *args,**kwargs):
        try:
            user_obj = request.user
            if user_obj:
                post = user_obj.post_set.filter(id=pk).first()
                serialized_post = PostSerializer(post, many=False)
            return Response({
                'status_code':status.HTTP_200_OK,
                'status_message':'Success',
                'post':serialized_post.data,
                })
        except Exception as e:
            return Response({'status_code':status.HTTP_500_INTERNAL_SERVER_ERROR,'status_message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class VotePostView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request, *args,**kwargs):
        try:
            post_obj = Post.objects.filter(id=request.data.get('post_id')).first()
            request.data._mutable = True
            request.data['post'] = post_obj.id
            request.data['voter'] = request.user.id
            request.data._mutable = False
            data1 = request.data 

            vote = Vote.objects.filter(post=post_obj, voter=request.user).first()
            if vote:
                vote.delete()
            else:
                serialize = VoteSerializer(data=data1)
                if serialize.is_valid():
                    serialize.save()






            return Response({
                'status_code':status.HTTP_200_OK,
                'status_message':'Success',
                })
        except Exception as e:
            return Response({'status_code':status.HTTP_500_INTERNAL_SERVER_ERROR,'status_message':'invalid session token !!'})
