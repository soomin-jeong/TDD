from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.conf import settings


class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=CASCADE)

    @property
    def name(self):
        return self.item_set.first().text

    def get_absolute_url(self):
        return reverse('lists:view-list', args=[self.id])

    @staticmethod
    def create_new(first_item_text, owner=None):
        list_ = List.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list=list_)
        return list_


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=CASCADE)




