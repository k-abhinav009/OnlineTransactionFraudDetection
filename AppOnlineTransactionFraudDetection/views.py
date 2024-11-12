from django.shortcuts import render,redirect
from django.db.models import Sum,Max
from django import template
from django.contrib.sessions.models import Session
import string
from django.core.files.storage import FileSystemStorage
from django.utils.module_loading import import_string
from datetime import date
from django.http import HttpResponse
from AppOnlineTransactionFraudDetection.models import User_details,Blockrequest, Products, Card_details, Order_details, Cart, Admin_details  
from AppOnlineTransactionFraudDetection.forms import User_details
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User, auth

# Create your views here.

def home(request):
    return render(request,'home.html',{})


def about(request):
    return render(request,"about.html",{})


def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['Username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['Email']
        cardnumber = request.POST['Cardnumber']
        cvv = request.POST['Cvv']
        Expirydate =  request.POST['Expiry_month'] + request.POST['Expiry_year']
        mobile = request.POST['password1']
        maxtrans = request.POST['password1']
        securityquestion1 = request.POST['SecurityQuestion1']
        answer1 = request.POST['SecurityAnswer1']
        securityquestion2 = request.POST['SecurityQuestion2']
        answer2 = request.POST['SecurityAnswer2']
        securityquestion3 = request.POST['SecurityQuestion3']
        answer3 = request.POST['SecurityAnswer3']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                #messages.info('request','username Taken')
                print('username taken')
                return redirect('/register/')

            elif User.objects.filter(email=email).exists():
                messages.info('request','Email Id taken')
                return redirect('/register/')

            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save();
                userid=list(User.objects.aggregate(Max('id')).values())[0]
                register1 = User_details( user_id=userid, Card_number=cardnumber ,cvv= cvv,Expirydate= Expirydate,mobile= mobile,MaxTransAmount=maxtrans,Securityquestion1=securityquestion1,Securityanswer1=answer1,Securityquestion2=securityquestion2,Securityanswer2=answer2,Securityquestion3=securityquestion3,Securityanswer3=answer3 )
                register1.save()
                print('User Created')
                messages.info(request,'User Registered')
                return redirect('/login/')
        else:
            messages.info(request,'Password doesnt match')
            return redirect('/register/')
    else:
        return render(request,"register.html",{})





def login(request):
    if request.method == 'POST':
        print('post')
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            print('login')
            current_user = request.user
            Uid = current_user.id
            if current_user.is_superuser:
                print('superuser')
                return redirect("/dashboard/")
            else:
                sus = User_details.objects.all().filter(user_id=Uid)
                print(sus[0].status)
                if sus[0].status == 'blocked':
                    request.session['blocked'] = 'yes'
                    print(request.session['blocked'])
                    return redirect("/blocked/")
                else:
                    request.session['blocked'] = 'no'
                    print(request.session['blocked'])
                    return redirect("/dashboard/")
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    else:
        return render(request,"login.html",{})


def logout(request):

    current_user = request.user
    if current_user.is_superuser :
        auth.logout(request)
        return redirect('/')
    else:
        Uid = current_user.id
        att = int(0)
        User_details.objects.filter(user_id=Uid).update(attempts=att)
        auth.logout(request)
        Cart.objects.all().delete()
        Session.objects.all().delete()
        return redirect('/')



def dashboard(request):
    products= Products.objects.all()
    return render(request,"Dashboard.html",{'products':products})


def addtocart(request):
    if request.method == 'POST':  
        current_user = request.user
        Uid = current_user.id
        users = User_details.objects.all().filter(user_id=Uid)
        cardnum = request.POST['Credit/Debit']
        cvv = request.POST['Cvv']
        expiry = request.POST['Expiry_month'] + request.POST['Expiry_year']
        cnum=users[0].Card_number
        print(cardnum)
        cv = users[0].cvv
        print(cvv)
        ex =  users[0].Expirydate
        print(expiry)

        if str(cnum) == str(cardnum) and str(cv) == str(cvv) and str(ex) == str(expiry):
            today = date.today()
            current_user = request.user
            d1 = today.strftime("%d/%m/%Y")
            tid = list(Order_details.objects.aggregate(Max('Tid')).values())[0] or 0
            finaltid = int(tid)+1
            Tid = finaltid
            Tdate = d1
            Uid = current_user.id
            Totalamount = int(request.POST['TotalAmount'])       
            Quantity = request.POST['hiddenfieldquantity']
            Quantity=Quantity[:-1]
            productlist = request.POST['hiddenfieldname']
            productlist=productlist[:-1]
            sus = User_details.objects.all().filter(user_id=Uid)
            
            if Totalamount > sus[0].MaxTransAmount: 
                status = 'Pending'
                add_orders = Order_details( Tid=Tid, Uid=Uid ,TotalAmount= Totalamount,date= Tdate,productList= productlist,quantity=Quantity,status=status )
                add_orders.save()
                Cart.objects.all().delete()
                order = Order_details.objects.all().filter(Tid=Tid)
                td= str(Tid)
                request.session['Tid'] = Tid
                messages.info(request,'Order pending for verification') 
                return redirect("/verify/"+ td,{})
            else:
                status = 'Ordered'
                add_orders = Order_details( Tid=Tid, Uid=Uid ,TotalAmount= Totalamount,date= Tdate,productList= productlist,quantity=Quantity,status=status )
                add_orders.save()
                Cart.objects.all().delete()
                messages.info(request,'Order placed successfully') 
                return redirect("/dashboard/")
        else:
            Carts = Cart.objects.all()
            #Cart.objects.all().aggregate(Sum('cost'))['cost__sum'] or 0.00
            total = list(Cart.objects.aggregate(Sum('total')).values())[0] or 0.00 
            messages.info(request,'details doesnt match')    
            return render(request,"AddtoCart.html",{'Carts':Carts,'total': total})


    else:
        Carts = Cart.objects.all()
        #Cart.objects.all().aggregate(Sum('cost'))['cost__sum'] or 0.00
        total = list(Cart.objects.aggregate(Sum('total')).values())[0] or 0.00     
        return render(request,"AddtoCart.html",{'Carts':Carts,'total': total})


def productdetails(request,id):
    if request.method == 'POST':
        userid = request.POST['uid']
        product_name = request.POST['pname']
        cost = request.POST['pcost']
        category = request.POST['category']
        Quantity = request.POST['Quantity']
        pid = request.POST['pid']
        if Cart.objects.filter(Pname=product_name).exists():
            sus = Cart.objects.all().filter(Pname=product_name)
            totalqty= int(Quantity) + int(sus[0].qty)
            totalamount= int(cost) * int(totalqty)
            #update query
            Cart.objects.filter(id=sus[0].id).update(qty=totalqty,total=totalamount)           
        else:
            totalamount= int(cost) * int(Quantity)
            add_cart = Cart( Pid=pid, Pname=product_name ,qty= Quantity,cost= cost,Uid= userid,total=totalamount,category=category )
            add_cart.save()              
        return redirect('/addtocart/',{})
        
    else:
        product = Products.objects.get(id=id)
        return render(request,"ProductDetails.html",{'product':product})


def deleteFromcart(request,id):
    Carts = Cart.objects.get(id=id)
    Carts.delete()
    messages.info(request,'Item removed from cart')
    return redirect('/addtocart/',{})


def ordersuccess(request):
    return render(request,"OrderSuccess.html",{})


def verify1(request,id): 
    if request.method == 'POST':
        
        current_user = request.user
        Uid = current_user.id
        product = User_details.objects.all().filter(user_id=Uid)
        if int(product[0].attempts) <= 2:
            print('enter')
            answer1 = request.POST['answer1']
            answer2 = request.POST['answer2']
            answer3 = request.POST['answer3']
            Securityanswer1 = product[0].Securityanswer1
            Securityanswer2 = product[0].Securityanswer2
            Securityanswer3 = product[0].Securityanswer3
            if Securityanswer1 == answer1 and  Securityanswer2 == answer2 and Securityanswer3 == answer3:
                print('success')
                Tid = request.session['Tid']
                Order_details.objects.filter(Tid=Tid).update(status='Ordered')
                return redirect("/dashboard/")
            else:
                print('fail') 
                att = int(product[0].attempts)+1
                User_details.objects.filter(user_id=Uid).update(attempts=att)
                q1 = product[0].Securityquestion1
                q2 = product[0].Securityquestion2
                q3 = product[0].Securityquestion3
                Tid = request.POST['tid']
                Orders = Order_details.objects.all().filter(Tid=Tid)
                td= str(Tid)
                messages.info(request,'Answer Doesnt match in 3 attempts you will be blocked' )
                return redirect("/verify/"+ td,{'q1':q1,'q2':q2,'q3':q3,'Orders':Orders})
                #return render(request,"verify.html",{'q1':q1,'q2':q2,'q3':q3})

        else:
            current_user = request.user
            Uid = current_user.id
            print('block')
            User_details.objects.filter(user_id=Uid).update(status='blocked')
            return render(request,"blocked.html",{})
    else:
        Tid = request.session['Tid']
        print(Tid)
        Orders = Order_details.objects.all().filter(Tid=Tid)
        current_user = request.user
        Uid = current_user.id
        product = User_details.objects.all().filter(user_id=Uid)
        q1 = product[0].Securityquestion1
        q2 = product[0].Securityquestion2
        q3 = product[0].Securityquestion3
        td= str(Tid)
        #return redirect("/verify/"+ td,{'q1':q1,'q2':q2,'q3':q3,'Orders':Orders})
        return render(request,"verify.html",{'q1':q1,'q2':q2,'q3':q3,'Orders':Orders})



def blocked(request):
    if request.method == 'POST':
        userid = request.POST['Uid']
        cardnumber = request.POST['CardNumber']
        cvv = request.POST['Cvv']
        issue =  request.POST['Issue']
        current_user = request.user
        Uid = current_user.id
        blockid = Blockrequest.objects.all().filter(user_id=Uid)
        if Blockrequest.objects.filter(user_id=userid).exists():
            user = User_details.objects.all().filter(user_id=Uid)
            messages.info(request,'Request previously generated') 
            return render(request,'blockedUser.html',{'user':user})
        else:
            block = Blockrequest(user_id=userid, Card_number=cardnumber ,cvv= cvv,Issue= issue )
            block.save()
            user = User_details.objects.all().filter(user_id=Uid)
            messages.info(request,'Request Generated') 
            return render(request,'blockedUser.html',{'user':user})
            

    else:
        current_user = request.user
        Uid = current_user.id
        user = User_details.objects.all().filter(user_id=Uid)
        print(user[0].user_id)       
        return render(request,'blockedUser.html',{'user':user})
       


def vieworders(request,):
    Order= Order_details.objects.all()
    return render(request,'vieworders.html',{'Order':Order})




def addproduct(request):
    if request.method == 'POST':
        pid = list(Products.objects.aggregate(Max('Pid')).values())[0] or 0
        finalpid = int(pid)+1
        pid = finalpid
        ProductName = request.POST['ProductName']
        Category = request.POST['Category']
        subcategory = request.POST['subcategory']
        cost = request.POST['cost']
        Description = request.POST['Description']
        quantity = request.POST['quantity']
        filesupload = request.FILES['file_upload']
        addproduct = Products( Pid=pid, pname=ProductName ,category= Category,subcategory= subcategory,cost= cost,desc=Description,quantity=quantity,image=filesupload,)
        addproduct.save()
        messages.info(request,'Product Added')
        return redirect('/addproduct/')
    else:
        return render(request,'addproduct.html',{}) 

def updatestatus(request,id):
    Order_detail = Order_details.objects.get(id=id)
    Order_details.objects.filter(id=id).update(status='Accepted')
    messages.info(request,'Order Accepted')
    return redirect('/vieworders/',{})


def unblock(request,id):
    blockid = Blockrequest.objects.get(id=id)
    print(blockid.user_id)
    User_details.objects.filter(user_id=blockid.user_id).update(status='Unblocked')
    blockid.delete()
    messages.info(request,'User Unblocked')
    return redirect('/unblockrequests/',{})


def unblockrequests(request):
    Order= Blockrequest.objects.all()
    return render(request,'unblockusers.html',{'Order':Order})
    