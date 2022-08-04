from django.db import models


# Step 1: Name the model and inherit from the django Model class
class EventGamer(models.Model):
    # Step 2: Add any fields on the erd
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)

