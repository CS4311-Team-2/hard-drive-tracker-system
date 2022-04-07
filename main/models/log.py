from django.db import models
from django.conf import settings

# Log model
class Log(models.Model):
    time_stamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    action_performed = models.CharField(max_length = 500)

