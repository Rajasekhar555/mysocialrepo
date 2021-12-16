from django.shortcuts import render
import operator
from itertools import chain
from functools import reduce

from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import (FileUploadParser, FormParser, MultiPartParser)

from mysocialapp.utilities import querySet_to_list
from mysocialapp.customMessages import CustomMessage
from mysocialapp.models import PostLikes,UserResponse,UserTagWeitage
from mysocialapp.serializers import PostLikesSerialzer,PostLikesListSerialzer,PostLikesResponseSerialzer

class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class PostLikesCreateAPIView(generics.CreateAPIView):
    """
        This API for Admin must be able to add posts 
        containing images and description
    """
    msg_ob = CustomMessage()
    permission_classes = (IsAuthenticated, IsSuperUser,)
    serializer_class = PostLikesSerialzer
    parser_class = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.create(validated_data=serializer.validated_data,user=request.user)
            return Response({"status":True, "msg": self.msg_ob.obj_create_success.format(obj_name="Story Card")
            , "response":{}}, status=status.HTTP_200_OK)
        else:
            return Response({"status":False, "msg": self.msg_ob.form_error, "response":{}}
            , status=status.HTTP_400_BAD_REQUEST)

class PostLikesAPIView(generics.ListAPIView):
    """
        This API for Admin must also be able to tag these post in order to 
        identify which post are similar, each tag will have weight, posts will 
        sort by this weight in descending order from most similar post to least similar post
    """
    model = PostLikes
    msg_ob = CustomMessage()
    permission_classes = (IsAuthenticated, IsSuperUser,)
    serializer_class = PostLikesListSerialzer

    def get_queryset(self):
        return self.model.objects.filter(is_active=True).order_by('-weight')

    def get(self, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, fields = ('id','name', 'description'
        , 'tag','weight', 'images'))
        return Response({"status":True, "msg": " ", "response":serializer.data}
        ,status=status.HTTP_200_OK)

class PostLikesStatusCountAPIView(generics.GenericAPIView):
    """
        This API for Admin should be able to view the number 
        of like/disliked of a post
    """
    model = UserResponse
    permission_classes = (IsAuthenticated, IsSuperUser,)

    def get(self, *args, **kwargs):
        res_count = {}
        user_res_list = self.model.objects.filter(story_card=self.kwargs.get('pk'))
        res_count["liked_count"] = user_res_list.filter(status="like").count()
        res_count["disliked_count"] = user_res_list.filter(status="dislike").count()
        return Response({"status":True, "msg": " ", "response":res_count}
        ,status=status.HTTP_200_OK)   



class PostLikesListAPIView(generics.ListAPIView):
    """
        API that returns a list of posts, return 10 post
    """
    model = PostLikes
    msg_ob = CustomMessage()
    permission_classes = (IsAuthenticated, )
    serializer_class = PostLikesListSerialzer

    def get(self, *args, **kwargs):
        tag_weitage_obj = UserTagWeitage.objects.filter(user=1).order_by('-weight').values_list("tag", flat=True)
        tag_list = querySet_to_list(tag_weitage_obj)
        filter_list = [Q(is_active=True)]
        if tag_weitage_obj: 
            filter_list.append(Q(tag__in=tag_list))

        high_weitage_posts = self.model.objects.filter(reduce(operator.and_, filter_list)).order_by('-weight').distinct()
        count_high_weitage_posts = high_weitage_posts.count()
        if count_high_weitage_posts <= 10:
            high_weitage_posts_ids = high_weitage_posts.values_list("id", flat=True)
            high_weitage_ids = querySet_to_list(high_weitage_posts_ids)
            remaing_post = 10 - int(count_high_weitage_posts)
            posts_list = self.model.objects.filter(is_active=True).exclude(id__in=high_weitage_ids).order_by('-weight')[:remaing_post]
            high_weitage_posts = list(chain(high_weitage_posts, posts_list))

        high_weitage_posts_serializer = self.get_serializer(high_weitage_posts, many=True).data
        return Response({"status":True, "msg": " ", "response":high_weitage_posts_serializer}
        ,status=status.HTTP_200_OK)   


class UserResponseAPIView(generics.CreateAPIView):
    """
        API for liking and disliking a post
    """
    model = PostLikes
    serializer_class = PostLikesResponseSerialzer
    msg_ob = CustomMessage()
    permission_classes = (IsAuthenticated)

    def get_object(self):
        try:return self.model.objects.get(pk=self.kwargs.get('pk'))
        except:return None
    
    def post(self, request, *args, **kwargs):
        user_obj = User.objects.get(id=1)
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.create(validated_data=serializer.validated_data, instance=instance, user=user_obj)
            return Response({"status":True, "msg": ""
                                        , "response":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"status":False, "msg":self.msg_ob.form_error, "response":{}}
            , status=status.HTTP_400_BAD_REQUEST) 
    

    
