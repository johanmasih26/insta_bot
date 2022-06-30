import os
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Post, Vote


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('__all__')

    def validate(self, attrs):
        description = attrs.get('description')
        image = attrs.get('image')
        if not description and  not image:
            raise serializers.ValidationError('Description or Image is required', code='authorization')
        allowed_type = ['.png']
        ext = os.path.splitext(attrs.get('image').name)[1]
        
        if ext not in allowed_type:
            raise serializers.ValidationError(' only png required', code='authorization')
        return attrs

    
    



class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
     )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])


    class Meta:
        model = User
        fields = ("username","name", "email", "password")
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            first_name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

    
    

class LoginSerializer(serializers.Serializer):
  
    email = serializers.CharField(label="email",write_only=True)
    password = serializers.CharField(
        label="password",style={'input_type': 'password'},trim_whitespace=False,write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
    
    
    
    

class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('__all__')

    
    
    
    