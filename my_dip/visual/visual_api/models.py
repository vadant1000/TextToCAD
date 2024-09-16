from django.db import models


class Visual(models.Model):
    name = models.TextField(blank=True, default='')
    type = models.TextField(blank=True, default='')

