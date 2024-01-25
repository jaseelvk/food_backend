from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField
from rest_framework import serializers
from dishes.models import Dish , Category, Comment, UserProfile



class DishesSerializer (ModelSerializer):

    category = serializers.StringRelatedField(many=True)
    like = SerializerMethodField()
    is_liked = SerializerMethodField()
    date = SerializerMethodField()

    class Meta : 
        model = Dish 
        fields = ("id","featured_image","date","dish_name","category","user_name","like","is_liked")

    def get_date(self,instance):
        return instance.date.strftime("%d %B %Y")

    
    def get_like(self,instance):
        return instance.like.count()
    
    def get_is_liked(self,instance):
        request = self.context.get("request")
        if instance.like.filter(username=request.user.username).exists():
            return True
        else : 
            return False


class RecipeeSerializer (ModelSerializer):

    date = SerializerMethodField()
    like = SerializerMethodField()
    is_liked = SerializerMethodField()
    category = serializers.StringRelatedField(many=True)

    class Meta : 
        model = Dish 
        fields = ("id","featured_image","date","dish_name","category","ingredients","recipee","user_name","like","is_liked")

    def get_date(self,instance):
        return instance.date.strftime("%d %B %Y")
    
    
    def get_like(self,instance):
        return instance.like.count()
    
    def get_is_liked(self,instance):
        request = self.context.get("request")
        if instance.like.filter(username=request.user.username).exists():
            return True
        else : 
            return False



class EditSerializer (ModelSerializer):

    class Meta : 
        model = Dish 
        fields = ("id","featured_image","date","dish_name","category", "ingredients","recipee","user_name")
    
    

class CategorySerializer (ModelSerializer):

    class Meta : 
        model = Category 
        fields = ("id","name")


class DeleteSerializer(ModelSerializer):
    class Meta : 
        model = Dish
        fields = ("id","is_deleted")

class CommentSerializer(ModelSerializer):

    username = SerializerMethodField()

    class Meta :
        model = Comment
        fields = ("id","date","comment","username", "is_deleted",)

    def get_username(self,instance):
        request = self.context.get("request")

        return instance.username.first_name
    
class ProfileSerializer(ModelSerializer):

    name = SerializerMethodField()
    email = SerializerMethodField()

    class Meta :
        model = UserProfile
        fields = ("profile_image","name","phone","email")
    
    def get_name(self,instance):
        request = self.context.get("request")

        return instance.name.first_name
    
        
    def get_email(self,instance):
        request = self.context["request"].user
        return request.username
    

class EditProfileSerializer(ModelSerializer):

    class Meta :
        model = UserProfile
        fields = ("profile_image","phone")