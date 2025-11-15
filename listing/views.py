from django.shortcuts import render , get_object_or_404 , redirect , HttpResponse
from django.db.models import Q
from .models import CustomUser
from .models import Room ,RoomImage , BookingRequest , CustomUser

#  login , logout , authenticate 
from django.contrib.auth import authenticate, login, logout  
from django.contrib import messages
from django.contrib.auth.decorators import login_required


#  For pagination 
from django.core.paginator import Paginator

# Create your views here.


def home(request):
    room_list = Room.objects.all().order_by('-created_at')
    paginator = Paginator(room_list, 8)  # show 8 rooms per page
    page_number = request.GET.get('page')
    rooms = paginator.get_page(page_number)
    return render(request, "home.html", {"rooms": rooms})


def room_detail(request,pk):
    room=get_object_or_404(Room ,pk=pk)
    return render (request,"room_detail.html" , {"room":room})


def Search(request):
    if request.method=="GET":
        query=request.GET.get("query")
        if query is not None :
            r= Room.objects.filter(Q(title__icontains=query)|Q(description__icontains=query)|Q(address__icontains=query)|Q(price_per_month__icontains=query))
        # ✅ Pagination setup
            paginator = Paginator(r, 8)  # 8 items per page (change as you wish)
            page_number = request.GET.get("page")
            rooms = paginator.get_page(page_number)
        return render (request , "home.html",{"rooms":rooms})
    redirect("home")

def Filter(request):
    if request.method == "GET":
        location = request.GET.get("location")
        min_price = request.GET.get("price_min")
        max_price = request.GET.get("price_max")
        room_type = request.GET.get("room_type")
        availability = request.GET.get("available")
        if min_price:
            try:
                 min_price = int(min_price)
            except ValueError:
                  min_price = None

        if max_price:
             try:
                max_price = int(max_price)
             except ValueError:
                 max_price = None
        print(request.GET)
        # Base queryset
        r= Room.objects.all()

        # ✅ Apply filters dynamically
        if location  and min_price is not None and max_price is not None  :
            r = Room.objects.filter(Q(address__icontains=location)&Q(price_per_month__gte=min_price, price_per_month__lte=max_price))
        elif location  or min_price or max_price or  availability  :
            r = Room.objects.filter(Q(address__icontains=location)|Q(price_per_month__gte=min_price, price_per_month__lte=max_price))
        elif location : 
            r = Room.objects.filter(address__icontains=location)
        else : 
            r=Room.objects.all()
        
        # elif min_price and max_price:
        #     r = Room.objects.filter(price_per_month__gte=min_price, price_per_month__lte=max_price)
        # elif availability:
        #    r = Room.objects.filter(availability__exact=availability)
        # if room_type:
        #     r = r.filter(room_type__icontains=room_type)

        # ✅ Pagination setup
        paginator = Paginator(r, 8)
        page_number = request.GET.get("page")
        rooms = paginator.get_page(page_number)

        return render(request, "home.html", {"rooms": rooms})

    return redirect("home")


def Register_as(request):
    if request.method == "POST":
        username= request.POST.get("username")
        email=request.POST.get("email")
        phone= request.POST.get("phone")
        password=request.POST.get("password")
        address=request.POST.get("address")
        user_ty=request.POST.get("user_type")
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Try another one.")
            return redirect("register") 
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            phone=phone,
            address=address,
            password=password , # hashed automatically
            user_type=user_ty
        )
        return redirect("login_as")


    return render (request,"Register.html")

def Login_as(request):
    if request.method=='POST':
        username=request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username , password=password)
        if user is not None :
            login(request, user)
            request.session['username'] = username
            return redirect("home")
        else :
                return redirect ("login_as")
    return render(request , "Login.html")
     
def Logout_as(request):
    logout(request)
    return redirect("home")


#  Booking 
@login_required(login_url='/Login/')

def Booking_as(request):
      
           user= request.user
           bookings=BookingRequest.objects.filter(user=user)
           return render (request , "Booking.html", {"bookings":bookings})


def Booking_req(request,pk):
    if request.method== 'POST':
        start_date=request.POST.get("start_date")
        end_date= request.POST.get("end_date")
        if request.user:
              
              Book=BookingRequest.objects.create(room_id=pk,start_Date=start_date ,user=request.user, end_Date=end_date)
              Book.save()
              print(Book)
              bookings=BookingRequest.objects.filter(user=request.user)
              print(bookings)

              return render ( request ,"Booking.html",{"bookings":bookings})
        
        else  : 
             return redirect ("login_as")
        
    

def Booking_cancle(request,pk ):
    if request.method == "POST":
        book = BookingRequest.objects.filter(user=request.user ,pk=pk)
        book.delete()
        return redirect ("booking")
    

#  from notifications.models import Notification

def send_message(request, room_id):
    if request.method == "POST":
        text = request.POST.get("text")
        room = Room.objects.get(id=room_id)
        receiver = room.Owner  # if renter sends message, owner is receiver
        sender = request.user
        # Create a notification for the receiver

        return redirect("chat_room", room_id=room.id)
    
# def Notifications (request):
#      return render (request , "Notification.html", {"Notifi":Notifi})

@login_required(login_url="login_as")
def Account_Center (request):
        if request.user.user_type=="Owner":
             rooms = Room.objects.filter(Owner=request.user)
        if request.user.user_type=="Renter":
             rooms= BookingRequest.objects.filter(renter=request.user)
        
        data = {
             "rooms":rooms,
             "user":request.user,
               }

        return render (request , "Account.html",{"data":data})

def edit_Profile(request):
     if request.method=="POST":
          user=request.user
          user.first_name = request.POST.get('first_name')
          user.last_name = request.POST.get('last_name')
          user.email = request.POST.get('email')
          user.phone = request.POST.get('phone')
          user.address = request.POST.get('address')
          user.user_type = request.POST.get('user_type')
          user.save() 
          return redirect("account")    
     return render (request , "Edit_Profile.html")
    
def add_room(request):
    if request.method=="POST":
         title=request.POST.get("title")
         dis=request.POST.get("description")
         price=request.POST.get("price")
         add= request.POST.get("address")
         images = request.FILES.getlist('images')  # multiple images
         room=Room.objects.create(
              title=title,
              description=dis,
              price_per_month=price,
              address=add

         )
         room.Owner = request.user  # assign logged-in user as owner
         room.save()
                     # Save each image
         for img in images:
              r_img = RoomImage.objects.create(room=room, image=img)
              r_img.save()
         return redirect("account")


    return render(request ,"Add_Room.html")


# update room by owner

def update_Room(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if request.method == "POST":
        room.title = request.POST.get("title")
        room.description = request.POST.get("description")
        room.price_per_month = request.POST.get("price")
        room.address = request.POST.get("address")
        room.availability= request.POST.get("availability")

        # Update images if new ones are uploaded
        images = request.FILES.getlist('images')
        if images:
            # Optionally delete old images
            RoomImage.objects.filter(room=room).delete()

            # Save new images
            for img in images:
                RoomImage.objects.create(room=room, image=img)

        room.save()
        return redirect("room_detail", pk=room.id)

    return render(request, "Update_Room.html", {"room": room})


#  Delete Room 
def delete_Room(request , pk ):
     if request.method=="POST":
          room = Room.objects.filter(pk=pk)
          room.delete()
          redirect("account")
     return render(request ,"Account.html") 
          

def about_Us(request):
     return render (request ,"About_us.html" )
     
     
