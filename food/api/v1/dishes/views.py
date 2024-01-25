
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import UpdateAPIView

from dishes.models import Dish, Category, Comment, UserProfile
from api.v1.dishes.serializers import DishesSerializer,RecipeeSerializer, CategorySerializer,\
DeleteSerializer,EditSerializer, CommentSerializer, ProfileSerializer,EditProfileSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def dishes(request):
    instances = Dish.objects.filter(is_deleted = False)
    q = request.GET.get("q")
    print(q)

    if q :
        instances = instances.filter(dish_name__icontains = q)

    filter = request.GET.get("filter")
    if filter : 
        ids = filter.split(",")
        instances = instances.filter(category__in=ids)
        instances = instances.distinct()

    context = {
        "request" : request
    }
    serializer = DishesSerializer(instances, many= True,context = context)
    response_data = {
        "status_code" : 6000,
        "data" : serializer.data,
        "message" : "succecss"
    }
    return Response (response_data)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def recipee(request, id):
    if Dish.objects.filter(pk=id).exists():    
        instance = Dish.objects.get(pk=id)
        context = {
        "request" : request
        }
        serializer = RecipeeSerializer(instance,context = context)
        response_data = {
            "status_code" : 6000,
            "data" : serializer.data,
            "message" : "success"
        }
        return Response (response_data)
    else:
        response_data =  {
            "status_code" : 6001,
            "message" : "oops..! recipee not found"
        }
        return Response (response_data)
    

@api_view(["GET"])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create(request):

    dish_name = request.data["dish_name"]
    ingredients = request.data["ingredients"]
    recipee = request.data["recipee"]
    user_name = request.user.username
    featured_image = request.data["featured_image"]
    categories_ids = request.data.get("category")

    selected_categories_ids = [int(id) for id in categories_ids.split(',')]
    
    print(selected_categories_ids)

    instance = Dish.objects.create(
        dish_name = dish_name,
        ingredients = ingredients,
        recipee = recipee,
        user_name = user_name,
        featured_image = featured_image

    )

    selected_categories = Category.objects.filter(id__in=selected_categories_ids)
    instance.category.add(*selected_categories)

    instance.save()

    response_data = {
            "status_code" : 6000,
            "message" : "sucecss"
        }
    return Response (response_data)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_user_profile(request):

    if request.user:
        user_profile, created = UserProfile.objects.get_or_create(name=request.user)

        return Response({"message": "UserProfile created successfully"}, status=200)
    else:
        return Response({"message": "User not found"}, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def mypost(request):

    instance = Dish.objects.filter(user_name = request.user.username , is_deleted = False)

    context = {
        "request" : request
    }
    serializer = RecipeeSerializer(instance,many=True,context = context)
    response_data = {
        "status_code" : 6000,
        "data" : serializer.data,
        "message" : "sucecss"
        }
    return Response (response_data)


@api_view(["POST"])
@permission_classes([AllowAny])
def delete(request, id):
    if Dish.objects.filter(id=id).exists():
        instance = Dish.objects.get(id=id)
        serializer  = DeleteSerializer(instance,data=request.data,partial = True)
        print(instance)
        if serializer.is_valid():
            serializer.save()

        response_data = {
        "status_code" : 6000,
        "message" : "sucecssfully deleted"
        }
        return Response(response_data)
    else:
        response_data = {
        "status_code" : 6001,
        "message" : "post not found"
        }
        return Response(response_data)


@api_view(["GET"])
@permission_classes([AllowAny])
def EditRecipee(request, id):
    if Dish.objects.filter(pk=id).exists():    
        instance = Dish.objects.get(pk=id)
        context = {
        "request" : request
        }
        serializer = EditSerializer(instance,context = context)
        response_data = {
            "status_code" : 6000,
            "data" : serializer.data,
            "message" : "sucecss"
        }
        return Response (response_data)
    else:
        response_data =  {
            "status_code" : 6001,
            "message" : "oops..! recipee not found"
        }
        return Response (response_data)



@api_view(["POST"])
@permission_classes([AllowAny])
def edit(request, id):
    if Dish.objects.filter(pk=id).exists():
        instance = Dish.objects.get(pk=id)

        dish_name = request.data.get("dish_name", instance.dish_name)
        ingredients = request.data.get("ingredients", instance.ingredients)
        recipee = request.data.get("recipee", instance.recipee)
        featured_image = request.data.get("featured_image", instance.featured_image)

        categories_ids = request.data.get("category")
        selected_categories_ids = [int(id) for id in categories_ids.split(',')]

        instance.dish_name = dish_name
        instance.ingredients = ingredients
        instance.recipee = recipee
        instance.featured_image = featured_image

        instance.category.clear()
        selected_categories = Category.objects.filter(id__in=selected_categories_ids)
        instance.category.add(*selected_categories)

        instance.save()

        response_data = {
            "status_code": 6000,
            "message": "Successfully updated"
        }
        return Response(response_data)
    else:
        response_data = {
            "status_code": 6001,
            "message": "Post not found"
        }
        return Response(response_data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postLikes(request, id):
    if Dish.objects.filter(id=id).exists():
        instance = Dish.objects.get(id=id)

        if instance.like.filter(username = request.user.username).exists():
            instance.like.remove(request.user)
            message  = "like removed"

        else:
            instance.like.add(request.user)
            message  = "liked"

        response_data =  {
                "status_code" : 6000,
                "message" : message                                                                                     
            }
        return Response(response_data)
    else:
        response_data =  {
            "status_code" : 6001,
            "message" : "oops..! place not found"
        }
        return Response (response_data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postComment(request, id):
    if Dish.objects.filter(pk=id).exists():
        instance = Dish.objects.get(pk=id)
        comment = request.data["comment"]
        username = request.user

        try:
            parent_comment = request.data["parent_comment"]
        except:
            parent_comment = None

        Comment.objects.create(
            comment = comment,
            username = username,
            dish = instance
        )
        if parent_comment:
            if Comment.objects.filter(pk=parent_comment).exists():
                parent = Comment.objects.get(pk=parent_comment)
                instance.parent_comment = parent
                instance.save()

        response_data =  {
                "status_code" : 6000,
                "message" : "comment Succesfully posted"                                                                                     
            }
        return Response(response_data)
    else:
        response_data =  {
            "status_code" : 6001,
            "message" : "oops..! place not found"
        }
        return Response (response_data)
    

@api_view(["GET"])
@permission_classes([AllowAny])
def listComment(request, id):
    if Dish.objects.filter(pk=id).exists():
        dish = Dish.objects.get(pk=id)

        instance= Comment.objects.filter(dish=dish,parent_comment = None)
        context = {
            "request" : request
        }

        serializer = CommentSerializer(instance,many = True,context= context)

        response_data =  {
                "status_code" : 6000,
                "data" : serializer.data,
                "message" : "comment Succesfully posted"                                                                                     
            }
        return Response(response_data)
    else:
        response_data =  {
            "status_code" : 6001,
            "message" : "oops..! place not found"
        }
        return Response (response_data)
    

        
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def profile(request):
    if UserProfile.objects.filter(name = request.user).exists():
        instance = UserProfile.objects.get(name = request.user)

        context = {
            "request" : request
        }
        serializer = EditProfileSerializer(instance, data=request.data, context = context)
        if serializer.is_valid():
            serializer.save()

            response_data = {
                "status_code" : 6000,
                "message" : "successfully updated"
            }

            return Response(response_data)
        else :

            response_data = {
                "status_code" : 6001,
                "message" : "validation_error",
                "data" : serializer.errors
            }
                    
            return Response(response_data)
        
    else:
            response_data = {
                            "status_code" : 6001,
                            "message" : "user not found",
                        }
                                
            return Response(response_data)

    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profileDetails(request):
    if request.user :
        instance = UserProfile.objects.get(name=request.user)
        context = {
            "request" : request
        }

        serializer = ProfileSerializer(instance, context = context)

        response_data =  {
                "status_code" : 6000,
                "data" : serializer.data,
                "message" : "success"
            }
        
        return Response (response_data)
    else:
        response_data =  {
            "status_code" : 6001,
            "message" : "oops..! user not found"
        }
        return Response (response_data)