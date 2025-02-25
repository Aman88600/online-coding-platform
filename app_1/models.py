from django.db import models

# Create your models here.
class Coders(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"username = {self.username} email = {self.email} password = {self.password}"

class Problems(models.Model):
    problem_name = models.CharField(max_length=20)
    problem_description = models.CharField(max_length=100)

    def __str__(self):
        return f"problem = {self.problem_name}"