from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')


def __str__(self):
    return f'{self.user.username} Profile'


def save(self):
    super().save()

    img = Image.open(self.image.path)
    (width, height) = img.size     
    size = ( 100, 100)
    img.resize(size, Image.ANTIALIAS)

    # if img.height > 70 or img.width > 70:
    #     output_size = (50, 50)
    #     img.thumbnail(output_size)
    img.save(self.image.path)


class Country(models.Model):
    name = models.CharField(max_length=30)


class City(models.Model):
    name = models.CharField(max_length=30)
    country = models.CharField(max_length=40)
    population = models.PositiveIntegerField()


class prodid(models.Model):
    prodid = models.CharField(max_length=50)
