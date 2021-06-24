from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# from blog.models import Post


# User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    email2 = serializers.EmailField(label='COnfirm Email')
    class Meta:
        model=User
        fields = [
            'username',
            'password',
            'email',
            'email2',
        ]

        extra_kwargs = {"password":{"write_only":True}}

    def create(self, validated_data):
        print(validated_data)
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username = username,
            email = email
        )
    def validate(self,data):
        email = data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("the email already exists")
        return data

    def validate_email2(self,value):
        data = self.get_initial()
        email = data.get("email")
        email2 = value
        if email1 != email2:
            raise ValidationError("emails don't match")

        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_blank = True, label='Username')
    token = serializers.CharField(label='Token', allow_blank = True, read_only= True)
    email = serializers.EmailField(label='Email')
    class Meta:
        model=User
        fields = [
            'username',
            'password',
            'email',
            'token',
        ]
        extra_kwargs = {"password":{"write_only":True}}

    def validate(self,data):
        user_obj = None
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        if not email and not username:
            raise ValidationError("A username or email is required")

        user = User.objects.filter(email = email, username = username).distinct()
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username/email is not valid")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials please try again")
        
        data["token"] = "SOME RANDOM TOKEN"

        return data
