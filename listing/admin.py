from django.contrib import admin
from .models import CustomUser

# Register your models here.

from .models import Room , RoomImage 

#  it can merge the room and room image 
#  we can add room image and room detail at the same time 
class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomImageInline]
    list_display = ('title', 'price_per_month', 'address', 'created_at')

admin.site.register(RoomImage)


admin.site.register(CustomUser)
