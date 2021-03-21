from django.db import models
from re import compile

email_regex = compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# Create your models here.
class UserManager(models.Manager):
    @staticmethod
    def basic_validation(post_data, update_password=True):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First Name must be 2 or more characters"
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last Name must be 2 or more characters"
        if not email_regex.match(post_data['email_address']):
            errors['email_address'] = "Please enter a valid email address"
        if update_password:
            if post_data['password'] != post_data['confirm_password']:
                errors['password'] = "Passwords do not match"
            if len(post_data['password']) < 8:
                errors['password'] = "Password must be 8 characters or longer"
        return errors


class QuoteManager(models.Manager):
    @staticmethod
    def basic_validation(post_data):
        errors = {}
        if len(post_data['author']) < 3:
            errors['author'] = "Author must be more than 3 characters"
        if len(post_data['quote']) < 10:
            errors['quote'] = "Quote must be more than 10 characters"
        return errors


class LikeManager(models.Manager):
    @staticmethod
    def basic_validation(post_data):
        errors = {}
        # todo create validation for likes
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Quote(models.Model):
    posted_by = models.ForeignKey(User, related_name='quotes', on_delete=models.CASCADE)
    quotation = models.TextField()
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    objects = QuoteManager()


class Like(models.Model):
    liked_by = models.ForeignKey(User, related_name='liked_quotes', on_delete=models.CASCADE)
    quote = models.ForeignKey(Quote, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    objects = LikeManager()
