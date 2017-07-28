from django.db import models

# What we do here is what shows up in the database.
class Podcast(models.Model):
    title =             models.CharField(max_length=120, null=True)
    description =       models.CharField(max_length=500, null=True)
    logo =              models.URLField(null=True, blank=True)
    favorite_episode =  models.URLField(null=True, blank=True)
    url =               models.URLField(null=True)
    saved_clips1 =      models.URLField(null=True, blank=True)
    saved_clips2 =      models.URLField(null=True, blank=True)
    saved_clips3 =      models.URLField(null=True, blank=True)
    shownotes =         models.URLField(null=True, blank=True)


    def __str__(self):
        return '%s %s' % (self.title, self.id)
