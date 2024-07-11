from django.db import models
import uuid
from .models import User, UserDialog

class AIDialog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_dialog = models.OneToOneField(UserDialog, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return self.text[:50]



class ChatRoom(models.Model):
    id = models.AutoField(primary_key=True)
    chat_room_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    analyze_target_name = models.CharField(max_length=100)
    analyze_target_relation = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.chat_room_id)
