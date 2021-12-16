"""
    Defines urls for social media
"""

from django.urls import path
#from rest_framework_swagger.views import get_swagger_view
from mysocialapp import views

#schema_view = get_swagger_view(title='SOCIAL MEDIA API')
urlpatterns = [
    #path('', schema_view),

    # Admin
    path('create-post-like/', views.PostLikesCreateAPIView.as_view(), name='create-post-like'),  
    path('posts-likes/', views.PostLikesAPIView.as_view(), name='post-likes'),  
    path('post-like-status-count/<int:pk>/', views.PostLikesStatusCountAPIView.as_view(), name='post-like-status-count'), 

    # User
    path('list-post-like/', views.PostLikesListAPIView.as_view(), name='list-post-like'), 
    path('post-like-response/<int:pk>/', views.UserResponseAPIView.as_view(), name='post-like-response'),  
     
]