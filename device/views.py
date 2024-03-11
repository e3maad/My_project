from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .models import Items,ItemDetails,Cart
from .forms  import CreateUserForm,LoginUserForm
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required(login_url='/auth_login/')
def checkout_V(request):
       template=loader.get_template('phone/checkout.html')
       current_user = request.user.id
       cart=Cart.objects.all().filter(Id_user=current_user).first()
       product=Items.objects.get(id=cart.Id_product)
       context={
            'cart':cart,
            'productname':product,
             'request':request
            
       }
       return HttpResponse(template.render(context=context)) 
def index(request):
   
   
    template=loader.get_template('index.html')
    return HttpResponse(template.render({'request':request}))


@login_required(login_url='/auth_login/')
def add_to_cart(requset,id):
     currentuser=requset.user
     discount=2
     state=False
     device=ItemDetails.objects.select_related('itemsid').filter(id=id)
    
     for item in device:
           net=item.total-discount
     cart = Cart(
      Id_product=item.id,
      Id_user=currentuser.id,
      price=item.price,
      qty=item.qty,
      tax=item.tax,
      total=item.total,
      discount=discount,
      net=net,
      status=state
)
     

     currentuser=requset.user.id
     count=Cart.objects.filter(Id_user=currentuser).count()
     print(count)
     cart.save()
     requset.session['countcart']=count
     return redirect("/")



def details_V(request , id):
     template=loader.get_template('device/details.html')
     
     currentuser=request.user
     print(currentuser.id)
     device=ItemDetails.objects.select_related('itemsid').filter(id=id)
    
     context={
         'device':device,
         'request':request
     }
     return HttpResponse(template.render(context))
@csrf_exempt
def auth_logout(request):
    if request.method=="POST":
        logout(request)
        return redirect("/")


def showdevice(request):
    template=loader.get_template('device/showdevice.html')
    device=ItemDetails.objects.select_related('itemsid')
    return HttpResponse(template.render({'device':device, 'request':request}))


@csrf_exempt
def auth_register(request):
      template=loader.get_template('auth_register.html')
      form=CreateUserForm()
      if request.method=="POST":
           form=CreateUserForm(request.POST)
           if form.is_valid():
                form.save()
                return redirect('auth_login')
      context={'registerform':form}
      return HttpResponse(template.render(context=context))
@csrf_exempt
def auth_logout(request):
     if request.method=="POST" :
          logout(request)
          return redirect("/")
@csrf_exempt
def auth_login(request):
     form=LoginUserForm()
     if request.method=="POST":
          form=LoginUserForm(data=request.POST)
          if form.is_valid():
              username=form.cleaned_data['username']
              password=form.cleaned_data['password']

              user=authenticate(username=username,password=password)
              if user:
                   if user.is_active:
                        login(request,user)
                        return render(request,'index.html')
     context={'form':form}
     return render(request,'auth_login.html',context)
                        

