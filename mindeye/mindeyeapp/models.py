from django.db import models


# Create your models here.
class Mindeye(models.Model):
    prompt=models.CharField(max_length=300)
    ai_image=models.ImageField(upload_to='ai_image')
    uid=models.ForeignKey("FormDataForm",on_delete=models.CASCADE,default=1)
    
class FormDataForm(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password=models.CharField(max_length=100)
    usertype=models.CharField(max_length=100, default='user')
 


