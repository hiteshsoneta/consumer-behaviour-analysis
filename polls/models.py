from django.db import models

# Create your models here.


class review(models.Model):
    text = models.CharField(max_length=1000)
    def __str__(self):
    	return self.text