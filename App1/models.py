from django.db import models
from matplotlib.pyplot import cla

# Create your models here.
class Register(models.Model):
    name=models.CharField(max_length=150)
    email=models.CharField(max_length=150)
    country=models.CharField(max_length=150)
    city=models.CharField(max_length=150)
    zipcode=models.CharField(max_length=150)
    address=models.TextField()
    verification_code=models.CharField(max_length=10)
    status=models.CharField(max_length=10)
    class Meta:
        db_table="register"