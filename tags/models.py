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




class Tag(models.Model):
    label = models.CharField(max_length=255)

class TaggedItem(models.Model):
    # what tag is applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # type of product to generate generic models relationship with use of content type
    product = models.ForeignKey(ContentType,  on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey()
 