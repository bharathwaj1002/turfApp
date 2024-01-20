from django.db import models

class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    date = models.DateField()
    session = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=10)