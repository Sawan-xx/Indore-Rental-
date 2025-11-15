from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils import timezone



# Create your models here.

#  Room model 
from django.db import models




class CustomUser(AbstractUser):
    # Add your custom fields here
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    user_type = models.CharField(max_length=10, default='Renter',choices=[("Owner","Owner"),('Renter','Renter')])

    def __str__(self):
        return self.username
    


class Room(models.Model):

    Owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    availability = models.CharField(max_length=50,default="Available", choices=[("Available", "Available"), ("Not Available", "Not Available")])

    def __str__(self):
        return self.title
    
# NEW MODEL FOR IMAGES
class RoomImage(models.Model):
    room = models.ForeignKey(Room, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='rooms/%Y/%m/')
    caption = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Image for {self.room.title}"



#  Booking Model For Booking room 
User = get_user_model()

class BookingRequest(models.Model):
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='renter_requests')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_requests')
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    start_Date=models.DateField( auto_now=False, auto_now_add=False)
    end_Date=models.DateField( auto_now=False, auto_now_add=False)
    status  = models.CharField(max_length=50, default="Pending",choices=[("Pending", "Pending"), ("Confirmed", "Confirmed"),("Cancelled","Cancelled")])
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.renter} → {self.room.title} ({self.status})"
    



