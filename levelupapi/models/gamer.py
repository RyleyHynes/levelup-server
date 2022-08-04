from django.db import models
from django.contrib.auth.models import User

# Step 1: Name the model and inherit from the django Model class
class Gamer(models.Model):
    # Step 2: Add any fields on the erd
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)

# Many to Many relationship with Gamer and Events