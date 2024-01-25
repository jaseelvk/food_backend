from django.urls import path
from api.v1.dishes import views



urlpatterns = [
    path('', views.dishes),
    path('view/<uuid:id>/', views.recipee),
    path('editRecipee/<uuid:id>/', views.EditRecipee),
    path('create/get_categories/', views.get_categories),
    path('create/', views.create),
    path('mypost/', views.mypost),
    path('mypost/delete/<uuid:id>/', views.delete),
    path('mypost/edit/<uuid:id>/', views.edit),
    path('likes/<uuid:id>/', views.postLikes),
    path('comment/<uuid:id>/', views.postComment),
    path('list/comments/<uuid:id>/', views.listComment),
    path('profile/', views.profile),
    path('profile/view/', views.profileDetails),
    

] 
