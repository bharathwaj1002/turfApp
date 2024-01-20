from django.db import models

class Booking(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    session = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=10)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)