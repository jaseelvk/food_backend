import uuid

from django.db import models


class Dish (models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    dish_name = models.CharField(max_length=255)
    category = models.ManyToManyField("dishes.Category")
    ingredients = models.TextField()
    recipee = models.TextField()
    user_name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    featured_image = models.FileField(upload_to="media/Dish_image",null=True,blank=True)
    
    like = models.ManyToManyField("auth.User")
    class Meta: 
        verbose_name_plural = "Dishes"
        ordering = ["-date"]

    def __str__(self):
        return self.dish_name
    

class Category (models.Model):
    name = models.CharField(max_length=255)

    class Meta : 
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
    
class UserProfile (models.Model):
    name = models.OneToOneField("auth.User",on_delete=models.CASCADE)
    phone = models.CharField(max_length=12,blank=True,null=True)
    profile_image = models.FileField(upload_to="profile/",blank=True,null=True)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)



class Comment (models.Model):
    parent_comment = models.ForeignKey('dishes.Comment',related_name="master_comment",blank=True,null=True,on_delete=models.CASCADE)
    comment = models.TextField()
    username = models.ForeignKey("auth.User",on_delete=models.CASCADE)
    dish = models.ForeignKey("dishes.Dish",on_delete=models.CASCADE)    
    is_deleted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)

    class Meta :
        ordering = ["-date"]


    def __str__(self):
        return self.comment



