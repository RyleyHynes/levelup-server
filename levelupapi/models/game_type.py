from django.db import models


# Step 1: Name the model and inherit from the Django Model class
class GameType(models.Model):
    # Step 2: Add any fields on the erd
    label = models.CharField(max_length=55)
