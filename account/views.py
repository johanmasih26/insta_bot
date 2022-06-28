from .serializers import PostSerializer
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
from django.contrib.auth import login

class get_posts(APIView):
    def get(self, request):
        posts = Post.objects.filter(id=1).first()
        serializer = PostSerializer(posts)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data=request.data
            if not data.get('email'):return Response({'status_code':str(status.HTTP_400_BAD_REQUEST),'status_message':'email is required'})
            if not data.get('password'):return Response({'status_code':str(status.HTTP_400_BAD_REQUEST),'status_message':'password is required'})
            user_obj = User.objects.filter(email=data.get('email')).first()
            print('####' ,data.get('email'),user_obj)
            if user_obj:
                if not check_password(data.get('password'), user_obj.password):
                    return Response({'status_code':str(status.HTTP_400_BAD_REQUEST),'status_message':'password not valid !'})                   # token = Token.objects.create(user=user_obj)
            if user_obj is not None:
                token_obj, created = Token.objects.get_or_create(user=user_obj)
                login(request, user_obj)
                request.session['session_token'] = token_obj.key     
            print('you are logged in !############3')
            return Response({"status": "success login token",'session_token':token_obj.key,})
        except Exception as e:
            return Response({'status_code':status.HTTP_500_INTERNAL_SERVER_ERROR,'status_message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            if request.session['session_token']:
                token_obj=Token.objects.get(key=request.session['session_token'])
                token_obj.delete()  
                del self.request.session['session_token']
                self.request.session.modified = True
                return Response({"status": "success logout token"})
        except Exception as e:
            return Response({'status_code':status.HTTP_500_INTERNAL_SERVER_ERROR,'status_message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"status": "success logout token"})


class RegisterView(APIView):
    def post(self,request,*args,**kwargs):
        try:
            data=request.data
            if not data.get('name'):return Response({'status_code':status.HTTP_400_BAD_REQUEST,'status_message':'name is required'})
            if not data.get('email'):return Response({'status_code':status.HTTP_400_BAD_REQUEST,'status_message':'email is required'})
            if not data.get('password'):return Response({'status_code':status.HTTP_400_BAD_REQUEST,'status_message':'password is required'})
            user = User.objects.filter(email=data.get('email')).first()
            if user:
                return Response({'status_code':status.HTTP_200_OK,'status_message':'User already Exit !'})
            user_obj = User(username=data.get('email'),first_name=data.get('name'),email=data.get('email'), password=make_password(data.get('password')))
            user_obj.save()
            return Response({'status_code':status.HTTP_200_OK,'status_message':'Success register saved'})
        except Exception as e:
            return Response({'status_code':status.HTTP_500_INTERNAL_SERVER_ERROR,'status_message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostCreateView(APIView):
    def post(self,request,*args,**kwargs):
        try:
            if request.session['session_token']:
                    
                data=request.data
                session_token = request.session['session_token']    
                token = Token.objects.filter(key=session_token).first()
                user_obj = User.objects.filter(email=token.user).first()
                if user_obj:
                    
                    if not self.request.POST.get('title'):return Response({'status_code':status.HTTP_400_BAD_REQUEST,'status_message':'title is required'})
                    description = self.request.POST.get('description')
                    file = self.request.FILES.get('image')
                    if  not description and not file:
                        return Response({'status_code':status.HTTP_400_BAD_REQUEST,'status_message':'Image or Description is required'})
                    post = Post(user=user_obj,title=self.request.POST.get('title'), description=self.request.POST.get('description'),image=self.request.FILES.get('image'))
                    post.save()
            
                return Response({'status_code':status.HTTP_200_OK,'status_message':'Success post created'})
        except Exception as e:
            return Response({'status_code':status.HTTP_500_INTERNAL_SERVER_ERROR,'status_message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostDetailView(APIView):
    response = {}
    def get(self,request, pk, *args,**kwargs):
        try:
            if request.session['session_token']:
                session_token = request.session['session_token']    
                token = Token.objects.filter(key=session_token).first()
                user_obj = User.objects.filter(email=token.user).first()
                if user_obj:
                    post = user_obj.post_set.filter(id=pk).first()
                    serialized_post = PostSerializer(post)
                return Response({
                    'status_code':status.HTTP_200_OK,
                    'status_message':'Success',
                    'post':serialized_post.data,
                    })
        except Exception as e:
            return Response({'status_code':status.HTTP_500_INTERNAL_SERVER_ERROR,'status_message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VotePostView(APIView):
    response = {}
    def post(self,request, *args,**kwargs):
        try:
            if request.session['session_token']:
                data = request.data
                session_token = request.session['session_token']    
                token = Token.objects.filter(key=session_token).first()
                user_obj = User.objects.filter(email=token.user).first()
                if user_obj:
                    post_obj = Post.objects.filter(id=data.get('post_id')).first()
                    print(request.user,'##########',request.user.id)
                    # vote_obj = Vote(post=post_obj, voter=request.user)
                    # vote_obj.save()
                    
                    
                return Response({
                    'status_code':status.HTTP_200_OK,
                    'status_message':'Success like or dislike',
                    # 'post':serialized_post.data,
                    })
        except Exception as e:
            return Response({'status_code':status.HTTP_500_INTERNAL_SERVER_ERROR,'status_message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
