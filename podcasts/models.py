from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.urls import reverse


User = settings.AUTH_USER_MODEL

class Friend(models.Model):
    users = models.ManyToManyField(User)

# What we do here is what shows up in the database.
class Podcast(models.Model):
    # Every user is assocated with an entry in the User model (default User model imported above)
    user =              models.ForeignKey(User) #class_instance.model_set.all()
    # friend =            models.ForeignKey(Friend) #class_instance.model_set.all()
    title =             models.CharField(max_length=120)
    description =       models.CharField(max_length=500)
    logo =              models.URLField(blank=False, default="http://via.placeholder.com/170x170")
    favorite_episode =  models.URLField(blank=True)
    url =               models.URLField()
    saved_clip =        models.URLField(blank=True, null=True)
    shownotes =         models.URLField(blank=True, null=True)


    def __str__(self):
        return '%s %s' % (self.title, self.id)



def pre_save_receiver(sender, instance, *args, **kwargs):
    instance.title = instance.title.title()

pre_save.connect(pre_save_receiver, sender=Podcast)
