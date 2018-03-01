from __future__ import unicode_literals
from django.db import models
import re
from datetime import date
import bcrypt



class UserManager(models.Manager):
    def register(self, post_data):
        errors = []
        if len(post_data["name"]) < 1:
            errors.append("Your name must be entered.")
        elif len(post_data["name"]) < 3:
            errors.append("Name must contain at least 3 characters.")

        if len(post_data["username"]) < 1:
            errors.append("A username must be entered.")
        elif len(post_data["username"]) < 3:
            errors.append("Your username must contain at least 3 characters.")
        else:
            matching = User.objects.filter(username=post_data["username"].lower())
            if len(matching) > 0:
                errors.append("Username already exists! Please choose a unique username.")

        if len(post_data["password"]) < 1:
            errors.append("Password must be selected!")
        elif len(post_data["password"]) < 8:
            errors.append("Password must be at least 8 characters.")

        if len(post_data["confirm"]) < 1:
            errors.append("Confirm password is required")
        elif post_data["password"] != post_data["confirm"]:
            errors.append("Confirm password must match Password")
        
        if str(date.today()) < str(post_data['hired']):
            errors.append("Please input the date you were hired. Date cannot be in the future.")

        if len(errors) > 0:
            return (False, errors)
        else:
            user = User.objects.create(
                name=post_data["name"],
                username=post_data["username"].lower(), 
                password=bcrypt.hashpw(post_data["password"].encode(), bcrypt.gensalt()),
                hired=post_data["hired"],
            )
            return (True, user)

    def login(self, post_data):
        
        response = {
            "errors": [],
            "is_valid": True,
            "user": None
        }

        if len(post_data["username"]) < 1:
            response["errors"].append("Please enter the username you selected upon registration.")
        else:
            matching = User.objects.filter(username=post_data["username"].lower())
            if len(matching) < 1:
                response["errors"].append("Unknown username.")

        if len(post_data["password"]) < 1:
            response["errors"].append("Password is required to login.")
        elif len(post_data["password"]) < 8:
            response["errors"].append("Passwords must be at least 8 characters long.")

        if len(response["errors"]) < 1:
            user = matching[0]
            if bcrypt.checkpw(post_data["password"].encode(), user.password.encode()):
                response["user"] = user
            else:
                response["errors"].append("Password is incorrect.")

        if len(response["errors"]) > 0:
            response["is_valid"] = False

        return response


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    hired = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class ItemManager(models.Manager):
    def itemcheck(self, postData, id):
        errors=[]
        if len(postData['name']) < 1 :
            errors.append("Item/product name field cannot be empty.")
        elif len(postData['name']) < 3 :
            errors.append("Item/product name must be at least 3 characters long.")

        if len(postData['desc']) < 2 :
            errors.append("A brief item summary of two or more characters must be included.")
        elif len(postData['desc']) > 255 :
            errors.append("Item summary must be under 255 characters.")
    
        
        if len(errors) > 0:
            return (False, errors)
        else:
            wish = Wishlist.objects.create(
                name=postData['name'],
                desc=postData['desc'],
                creator=User.objects.get(id=id),
                )
            return (True, wish)
            
    def wishCheck(self, wisher_id, id):
        errors=[]
        if len(User.objects.filter(id=id).filter(wisher=wisher_id)) > 0:
            errors.append("You have already added this item to your list!")
            return (False, errors)
        else:
            a = Wishlist.objects.get(id=wisher_id)
            b= User.objects.get(id=id)
            a.others.add(b)
            return (True, a)

    def unwishCheck(self, wisher_id, id):
            a = Wishlist.objects.get(id=wisher_id)
            b = User.objects.get(id=id)
            a.others.remove(b)
            return (a)



class Wishlist(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="createe")
    others = models.ManyToManyField(User, related_name="wisher")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    desc = models.CharField(max_length=255)
    objects = ItemManager()