from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.signals import user_logged_out,user_logged_in
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from.models import profile
from .models import friend_request
from django.dispatch import receiver
from django.contrib import messages
# Create your views here.
@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    msg = 'You have securely logged in {name} '.format(name=user.username)
    messages.add_message(request, messages.INFO, msg)
@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    msg = 'You have securely logged out. Thank you for visiting.'
    messages.add_message(request, messages.INFO, msg)
def register(request):
    form = UserRegisterForm()
    if request.method=="POST":
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f"you have succesfully created and logged as {username}")
            login(request,user)
            return redirect('blog-home')
    return render(request,"user/register.html",{"form":form,"title":"register"})



def profile1(request):
    c=0
    if request.method=="POST":
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,"account updated")
    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profile)
    for i in friend_request.objects.all():
        if request.user == i.to_user:
            c+=1
    
    return render(request,"user/profile.html",{'u_form':u_form,"p_form":p_form,"title":"profile","fcount":c})

