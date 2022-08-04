from django.db import models


# Step 1: Name the model and inherit from the django Model class
class Game(models.Model):
    # Step 2: Add any fields on the erd
    game_type= models.ForeignKey("GameType", on_delete=models.CASCADE)
    title=models.CharField(max_length=55)
    maker=models.CharField(max_length=55)
    gamer=models.ForeignKey("Gamer", on_delete=models.CASCADE)
    number_of_players=models.IntegerField()
    skill_level=models.IntegerField()
