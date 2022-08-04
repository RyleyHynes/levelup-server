from django.db import models


# Step 1: Name the model and inherit from the django Model class
class Event(models.Model):
    # Step 2: Add any fields on the erd
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    attendees = models.ManyToManyField("Gamer", through="EventGamer", related_name="events")
