from django.db import models

# Create your models here.
class Team(models.Model):
    name = models.TextField()
    wins = models.IntegerField()

    def __str__(self):
        return "Name: {} Wins: {}".format(self.name, self.wins)

