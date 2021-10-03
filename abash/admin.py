from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

class Property_ImagesAdmin(admin.StackedInline):
    model = Property_Images

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    model = Property
    inlines = [Property_ImagesAdmin]
    

#Register your models here.
admin.site.register(User_Details)
#admin.site.register(User)
admin.site.register(Property_Images)
admin.site.register(Room)
admin.site.register(Location)
admin.site.register(Booking)
admin.site.register(Property_rating)
admin.site.register(App_rating)


