from django.db import models
from .models import User

class TreeMap(models.Model):
    id = models.AutoField(primary_key=True)
    tree_map_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tree_level = models.IntegerField(default=0)
    happiness = models.FloatField(default=0.0)
    anger = models.FloatField(default=0.0)
    sadness = models.FloatField(default=0.0)
    pleasure = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.tree_map_id)

class TreeDetail(models.Model):
    id = models.AutoField(primary_key=True)
    tree_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tree_map = models.ForeignKey(TreeMap, on_delete=models.CASCADE)
    tree_growth_level = models.IntegerField(default=0)
    location_x = models.FloatField(default=0.0)
    location_y = models.FloatField(default=0.0)
    
    def __str__(self):
        return str(self.tree_id)
