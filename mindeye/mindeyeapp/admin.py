from django.contrib import admin
from .  models import Mindeye
from . models import FormDataForm


# Register your models here.
class MindeyeAdmin(admin.ModelAdmin):
    list_display = ('prompt','ai_image')

admin.site.register(Mindeye,MindeyeAdmin)

class FormDataFormAdmin(admin.ModelAdmin):
    list_display=('name','email','password')

admin.site.register(FormDataForm,FormDataFormAdmin)
