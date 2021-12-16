from django.db import models
from django.contrib.auth.models import User


class CommonInfo(models.Model):
    '''
    Abstract base classes are useful when you want to put some common information 
    into a number of other models.
     
    '''
    created_on             = models.DateTimeField(auto_now_add=True)
    last_updated_on        = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AddTag(models.Model):
    name                   =models.CharField(max_length=200)
    def __str__(self):
        return self.name

class PostLikes(CommonInfo):
    name                   = models.CharField(max_length=250)
    description            = models.TextField(null=True, blank=True)
    user                   = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_user", null=True, blank=True)
    tag                    = models.ManyToManyField(AddTag,related_name="post_tag")
    weight                 = models.IntegerField(default=0)  # Weitage for tag in a StoryCard
    is_active              = models.BooleanField(default=True)

class AdminInfo(CommonInfo):
    image_post             = models.ForeignKey(PostLikes, on_delete=models.CASCADE, related_name="post_image")
    image                  = models.ImageField(upload_to="attachement/file")
    is_active              = models.BooleanField(default=True)

class UserResponse(CommonInfo):
    IMAGE_POST_STATUS = (
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    )

    image_post             = models.ForeignKey(PostLikes, on_delete=models.CASCADE, related_name="post_tag")
    user                   = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User_response")
    status                 = models.CharField(max_length=100, choices=IMAGE_POST_STATUS)

class UserTagWeitage(models.Model):
    user                   = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_tag_user")
    tag                    = models.ForeignKey(AddTag, on_delete=models.CASCADE, related_name="user_post_tag")
    weight                 = models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name

    class Meta:
        ordering = ['weight']