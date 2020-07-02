from django.db import models
import re
from django.contrib import messages

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):           
            errors['email'] = "Please enter a valid email address"
        if User.objects.filter(email=postData['email']).exists():
            errors['email'] = "An account has already been created with this email"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords do not match"
        return errors

class PostManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['post_content']) < 1:
            errors['post_content'] = "Nothing to say? Get outta here!"
        return errors

class CommentManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['comment_content']) < 1:
            errors['comment_content'] = "Uhh, you like, can't have a blank comment."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=65)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Post(models.Model):
    post_content = models.CharField(max_length=5000)
    user = models.ForeignKey(User, related_name="posts", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()

class Comment(models.Model):
    comment_content = models.CharField(max_length=5000)
    user = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()

