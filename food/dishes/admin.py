from django.contrib import admin
from dishes.models import Dish, Category, UserProfile, Comment


class AdminDish(admin.ModelAdmin):
    list_display = ["id","dish_name","user_name"]

    
admin.site.register(Dish,AdminDish)


admin.site.register(Category)

class AdminUserProfile(admin.ModelAdmin):
    list_display = ["name","phone"]
admin.site.register(UserProfile, AdminUserProfile)


admin.site.register(Comment)


