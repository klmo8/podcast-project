from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.urls import reverse
from django.contrib.auth.models import User
# User = settings.AUTH_USER_MODEL

# Credit to Max Goodridge (https://www.youtube.com/watch?v=Fc2O3_2kax8&list=PLw02n0FEB3E3VSHjyYMcFadtQORvl1Ssj).
# The below code for friendships was adapted from his Django tutorial series on YouTube.
class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True)

    # Using a class method because this functionality is very specific to the Friend model (will not be used by any other models)
    # Therefore, we associate the desired functionality directly with the class (rather than implementing in views)
    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def unfriend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)

# What we define here is what shows up in the database.
class Podcast(models.Model):
    # Every user is assocated with an entry in the User model (default User model imported above)
    user =              models.ForeignKey(User) #class_instance.model_set.all()
    title =             models.CharField(max_length=120)
    description =       models.CharField(max_length=500)
    logo =              models.URLField(blank=False, default="http://via.placeholder.com/170x170")
    favorite_episode =  models.URLField(blank=True)
    url =               models.URLField()
    saved_clip =        models.URLField(blank=True, null=True)
    shownotes =         models.URLField(blank=True, null=True)


    def __str__(self):
        return '%s %s %s' % (self.title, self.id, self.user)


# Capitalizes records being saved to the database.
def pre_save_receiver(sender, instance, *args, **kwargs):
    instance.title = instance.title.title()

pre_save.connect(pre_save_receiver, sender=Podcast)
