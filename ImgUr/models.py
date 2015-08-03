from django.db import models


class Subscriber(models.Model):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=64)

    class Meta:
        db_table = "subscribers"
