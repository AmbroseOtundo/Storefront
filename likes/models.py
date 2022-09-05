from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.auth.models import User

class LikedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # content_type shows the content the user has liked
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # ref that particular object
    object_id = models.PositiveBigIntegerField()
    # showing that particular object
    content_object = GenericForeignKey()