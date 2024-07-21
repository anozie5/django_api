from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# model for user
class UserAccount (AbstractUser):
    name = models.CharField (max_length = 20)
    def __str__(self):
        return self.username
    
class Todo (models.Model):
    about = models.ForeignKey(UserAccount, on_delete = models.CASCADE)
    job = models.TextField ()
    created_on = models.DateTimeField (auto_now_add = True)
    updated_on = models.DateTimeField (auto_now = True)
    def __str__(self):
        return self.about



