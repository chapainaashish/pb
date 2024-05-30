from django.db import models


class ContactEntry(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.subject


class Subscriber(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.email
