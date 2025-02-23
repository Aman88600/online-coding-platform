from django.db import models

# Create your models here.
class Coders(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"username = {self.username} email = {self.email} password = {self.password}"