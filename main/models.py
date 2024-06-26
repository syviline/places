from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage


# Create your models here.
class Place(models.Model):
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name='Название')
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True, default="user_images/default.jpg", verbose_name='Фото')
    search = models.TextField()  # contains name + description + address in lower case,
    # search uses this field

    description = models.TextField(null=True, verbose_name='Описание')  # description of place
    address = models.CharField(max_length=255, verbose_name='Адрес')  # адрес
    latitude = models.DecimalField(max_digits=22, decimal_places=20, verbose_name='Широта')  # широта
    longitude = models.DecimalField(max_digits=23, decimal_places=20, verbose_name='Долгота')  # долгота
    hashtags = models.TextField(null=True, verbose_name='Хэштеги')  # хэштеги
    is_public = models.BooleanField(default=True, verbose_name='Опубликовать')
    views = models.IntegerField(default=0, null=False)

    def save(self, *args, **kwargs):
        # Get reference of previous version of this place
        old_place = Place.objects.filter(pk=self.pk).first()
        self.search: models.TextField
        self.search = (self.name + " " + self.description + " " + self.address + " " + self.hashtags).lower()
        # Deletes current photo, if any, from Place when updating it
        if old_place and old_place.photo:
            if old_place.photo != self.photo:
                self.delete_photo(old_place.photo)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Check if there current Place has a photo and deletes it when deleting a Place
        if self.photo:
            self.delete_photo(self.photo)

        super().delete(*args, **kwargs)

    def delete_photo(self, photo):
        # If there is a photo on local storage for current Place, deletes it when deleting a Place
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)

    def __str__(self):
        photo_str = self.photo.url if self.photo else 'no photo'
        return f'{self.pk}: {self.name}, visited? {self.visited} on {self.date_visited}\nPhoto: {photo_str}'


class Serie(models.Model):
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(null=True, verbose_name='Описание')  # description of place
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True, default="user_images/default.jpg", verbose_name='Фото')
    search = models.TextField()  # contains name + description + address in lower case,
    # search uses this field
    is_public = models.BooleanField(default=True, verbose_name='Опубликовать')
    places = models.ManyToManyField(Place)
    views = models.IntegerField(default=0, null=False)