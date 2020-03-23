from django.db import models

# Create your models here.
class Reviews(models.Model):
    reviews=models.TextField()
    ratings=models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.reviews}{self.ratings}'

