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
from .models import Post


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
    
    
    
    












    
    
    
    
    
    
    # # first_name = serializers.CharField(required=True)
    # # email = serializers.EmailField(
    # # required=True,
    # # validators=[UniqueValidator(queryset=User.objects.all())]
    # #  )
    # # password = serializers.CharField(
    # #     write_only=True, required=True, validators=[validate_password])

    # class Meta:
    #     model = User
    #     fields = ('first_name','email', 'password')
    #     # extra_kwargs = {
        # 'first_name': {'required': True},
        # 'email': {'required': True},
        # 'password': {'required': True}
        # }

        # def validate_register(self, data):
        #     if data['first_name'] is None and data['first_name'] == '':
        #         raise serializers.ValidationError('Name is Required !!')
        #         return data
            
        #     elif data['email'] is None and data['email'] == '':
        #         raise serializers.ValidationError('Email is Required !!')
        #         return data

        #     elif data['password'] is None and data['password'] == '':
        #         raise serializers.ValidationError('Password is Required !!')
        #         return data

 
                
        # def create(self, validated_data):
        #     user = User.objects.create(
        #     email=validated_data['email'],
        #     first_name=validated_data['firstname'],
        #     )
        #     user.set_password(validated_data['password'])
        #     user.save()
        #     return user


# class UserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ('__all__')

#     def create(self, validated_data):
#         user = User.objects.create(**validated_data)
#         User.objects.create(user=user, **validated_data)
#         return user