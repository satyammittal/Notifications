from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.db.models.signals import post_save
from notification.models import Stock, NotificationLogs
from django.shortcuts import redirect

def index(request):
    return render(request, 'notification/index.html', {})

def user_login(request):    # Just a simple login functionality to user

    if request.method == 'POST':    # Taking data from push request sent from http client
        username = request.POST.get('username')
        password = request.POST.get('password')
        print username, password

        user = authenticate(username=username, password=password)

        if user:
      
            if user.is_active:
      
                login(request, user)
                return HttpResponseRedirect('/notify/home/')
            else:
       
                return HttpResponse("Your account is activated")
        else:
        
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
     
        return render(request, 'rango/login.html', {})
@login_required
def subscribe(request):
    user = request.user
    sub_stocks = Stock.objects.filter(subscriber = user)
    dis_stocks = Stock.objects.exclude(subscriber = user)
    arr = {
        "sub": sub_stocks,"dis": dis_stocks
    }
    return render(request, 'notification/subscribe.html', arr)
def subscribe2(request):
    user = request.user
    sub_stocks = Stock.objects.filter(subscriber = user)
    dis_stocks = Stock.objects.exclude(subscriber = user)
    arr = {
        "sub": sub_stocks,"dis": dis_stocks
    }
    req = request.POST
    opt = req['option']
    st = Stock.objects.filter(stock_name = opt).first()
    st.subscriber.add(user)
    return render(request, 'notification/subscribe.html', arr)
def unsubscribe(request):
    user = request.user
    sub_stocks = Stock.objects.filter(subscriber = user)
    dis_stocks = Stock.objects.exclude(subscriber = user)
    arr = {
        "sub": sub_stocks,"dis": dis_stocks
    }
    req = request.POST
    opt = req['option']
    st = Stock.objects.filter(stock_name = opt).first()
    st.subscriber.remove(user)
    return render(request, 'notification/subscribe.html', arr)

# home is a function where we decide what a prticular user can see 
# In home page A user can see all changes activities made in database
@login_required     # Using django internal Authentication system to authenticate users
def home(request):
    user = request.user
    log = NotificationLogs.objects.filter(user = user).order_by('-timestamp')
    stocks = Stock.objects.filter(subscriber = user)
    count = NotificationLogs.objects.filter(user = user).count()
    stock_names = []
    for stock in stocks:
        stock_names.append(str(stock.stock_name))
    logs = []
    for l in log:
        log_dtl = {}
        log_dtl["stock_name"] = l.stock.stock_name
        log_dtl["stock_price"] = l.stock_price
        log_dtl["time"] = l.timestamp
        logs.append(log_dtl)

    context_dict = {"stocks_names":stock_names,"logs":logs, "count":count}
    return render(request, 'notification/home.html', context_dict)


@login_required
def update(request):
    user = request.user
    sub_stocks = Stock.objects.filter(subscriber = user)
    arr = {
        "sub": sub_stocks
    }
    return render(request, 'notification/update.html', arr)  

@login_required
def updatevalue(request):
    req = request.POST
    user = request.user
    stock = req['stock']
    value = req['value']
    update_stock = Stock.objects.filter(subscriber = user, stock_name = stock).first()
    update_stock.price = value
    update_stock.save()
    sub_stocks = Stock.objects.filter(subscriber = user)
    arr = {
        "sub": sub_stocks
    }
    return render(request, 'notification/update.html', arr)    

@receiver(post_save, sender=Stock)
def sample(sender, **kwargs):
    updated_stock = kwargs.get('instance')
    users = User.objects.filter(stock = updated_stock)

    for user in users:
        update_flag = True
        previous_logs = NotificationLogs.objects.filter(user = user,stock=updated_stock).order_by('-timestamp')
        if len(previous_logs) >0:
            prev_log = previous_logs[0]
            if prev_log.stock_price == updated_stock.price:
                update_flag = False
        if update_flag == True:
            log = NotificationLogs()
            log.user = user
            log.stock_price = updated_stock.price
            log.stock = updated_stock
            log.save()
 
    
   