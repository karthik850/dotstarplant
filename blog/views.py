from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.contrib import messages
from .models import posts,comments,savedposts
from django.contrib.auth.models import User
from django.views.generic import ListView,DeleteView,DetailView,UpdateView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from user.models import profile,friend_request
from django.template.loader import render_to_string
from django.core.paginator import Paginator
num=0
# Create your views here.
#def home(request):
   # return render(request,'blog/home.html',{'posts':posts.objects.all})

@login_required
def myposts(request):
    num=1
    c=0
    posts1=posts.objects.filter(author=request.user).order_by('-date_posted')
    paginator = Paginator(posts1,10)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    for i in friend_request.objects.all():
        if request.user == i.to_user:
            c+=1
    return render(request,'blog/user_post.html',{'page_obj':page_obj,'a':num,'title':"myposts",'fcount':c})
@login_required
def searchposts(request):
    num=2
    a=request.GET["val1"]
    b=0
    count=0
    if a!="":
        try:
            b=User.objects.get(username=a)
        except:
            pass
        if b:
            posts1=posts.objects.filter(author=b).order_by('-date_posted')
            paginator = Paginator(posts1,10)
            page_number=request.GET.get('page')
            page_obj=paginator.get_page(page_number)
            for i in friend_request.objects.all():
                if request.user == i.to_user:
                    count+=1
            #return HttpResponse(c)
            return render(request,'blog/user_post.html',{'page_obj':page_obj,'a':num,'b':b,"title":"searchpost",'fcount':count})
        else:
            alert("nouser")
            return HttpResponseRedirect(reverse('blog-home'))
    else:
        return HttpResponseRedirect(reverse('blog-home'))

def postlistview1(request):
    num=0
    c=0
    l=[]
    if request.user.username == "":
        return render(request,'blog/getstarted.html')
    else:
        l.append(User.objects.get(username=request.user))
        for i in request.user.profile.followers.all():
            l.append(User.objects.get(username=i))
        l=list(set(l))
        posts1=posts.objects.filter(author__in=l).order_by('-date_posted')
        paginator = Paginator(posts1,10)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        for i in friend_request.objects.all():
            if request.user == i.to_user:
                c+=1
        context={'page_obj':page_obj,'a':num,'title':"homepage",'fcount':c}
        return render(request,'blog/posts_list.html',context)
#present not using this view
class postlistview(ListView):
    model=posts
    num=0

    def get(self,request):
        p=posts.objects.all().order_by('-date_posted')
        context={'posts':posts.objects.all().order_by('-date_posted'),'a':num,'title':"homepage"}
        return render(request,'blog/posts_list.html',context)


def userpostlistview1(request,username):
    c=0
    user=User.objects.get(username=username)
    posts1=posts.objects.filter(author=user).order_by('-date_posted')
    paginator = Paginator(posts1,10)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    for i in friend_request.objects.all():
            if request.user == i.to_user:
                c+=1
    context={'page_obj':page_obj,'friend_request':friend_request.objects.all(),'fcount':c,'name':user}

    return render(request,'blog/user_post.html',context)

#present not using this view
class userpostlistview(ListView):
    model=posts
    template_name='blog/user_post.html'
    context_object_name = 'posts'
    ordering=['-date_posted']

    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return HttpResponse(user)
       # return posts.objects.filter(author=user).order_by('-date_posted')  #context_object_name='num'

class postdetailview(DetailView):
    model=posts
    #not using
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(posts, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        return data

class postcreateview(LoginRequiredMixin,CreateView):
    model=posts
    fields=['title','content','image']
    success_url='/'
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class postupdateview(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=posts
    fields=['title','content','image']
    success_url='/'
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False


class postdeleteview(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = posts
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request,'blog/about.html')


@login_required
def BlogPostLike(request,pk):
    #return HttpResponse(request.GET["posts_id"])
    if request.method=='GET':
        post = get_object_or_404(posts, id=request.GET["posts_id"])
        #return HttpResponse(post.likes.all)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        #return HttpResponseRedirect(reverse('blog-home'))
    else:
        return HttpResponseRedirect(reverse('blog-home'))
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


@login_required
def BlogPostLike1(request):
    #return HttpResponse(request.GET["posts_id"])
    post = get_object_or_404(posts, id=request.GET["id"])
        #return HttpResponse(post.likes.all)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    context={"post":post,"total_likes":post.number_of_likes}
        #return HttpResponseRedirect(reverse('blog-home'))
    if request.is_ajax():
        html = render_to_string('blog/likesection.html',context=context,request=request)
        return JsonResponse({'form':html})


@login_required
def followview(request,username):
    prof=get_object_or_404(profile,id=request.GET["u_id"])
    prof.followers.add(request.user.id)
        #request.user.profile.following.add(request.GET["u_id"])
    return HttpResponseRedirect(reverse('user-posts', args=[str(username)]))


def disconnect(request,username):
    for i in profile.objects.all():
        if i.user.username == request.user.username:
            i.followers.remove(request.GET["u_id"])
            i.request.remove(request.GET["u_id"])
            break
    return HttpResponseRedirect(reverse('user-posts', args=[str(username)]))

def disconnect1(request):
    for i in profile.objects.all():
        if i.user.username == request.user.username:
            i.followers.remove(request.GET["u_id"])
            i.request.remove(request.GET["u_id"])
            break
    context={"user.profile.followers.all":request.user.profile.followers.all}
    if request.is_ajax():
        html = render_to_string('user/myfollowers.html',context=context,request=request)
        return JsonResponse({'form':html})



@login_required
def send_request(request,username):
    prof=get_object_or_404(profile,id=request.GET["u_id"])
    from_user=request.user
    to_user=User.objects.get(username=username)

    Friend_request,created=friend_request.objects.get_or_create(from_user=from_user,to_user=to_user)

    if created:
        #prof.request.add(request.user.id)
        request.user.profile.request.add(request.GET["u_id"])
        return HttpResponseRedirect(reverse('user-posts', args=[str(username)]))
    else:
        return HttpResponseRedirect(reverse('user-posts', args=[str(username)]))


@login_required
def accept_request(request,requestID,username):
    for i in profile.objects.all():
        if i.user.username==username:
            Friend_request=friend_request.objects.get(id=requestID)
            Friend_request.to_user.profile.followers.add(Friend_request.from_user.profile)
            Friend_request.from_user.profile.followers.add(Friend_request.to_user.profile)
            Friend_request.delete()
            i.request.remove(request.user.id)
            break
    return render(request,'blog/request.html',{'friend':friend_request.objects.all()})


@login_required
def request_page(request):
    c=0
    for i in friend_request.objects.all():
            if request.user == i.to_user:
                c+=1
    return render(request,'blog/request.html',{'friend':friend_request.objects.all(),'fcount':c})


@login_required
def reject_request(request,requestID,username):
    for i in profile.objects.all():
        if i.user.username==username:
            Friend_request=friend_request.objects.get(id=requestID)
            Friend_request.delete()
            i.request.remove(request.user.id)
            request.user.profile.request.remove(i.user.id)
            break
    return render(request,'blog/request.html',{'friend':friend_request.objects.all()})

#def cancel_request(request,requestID):
   #pass
def commentcreateview(request,pk):
    comments.objects.create(post=posts.objects.get(id=pk),name=request.user,description=request.POST['desc']).save()
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

def commentcreateview1(request):
    post = get_object_or_404(posts, id=request.POST["id"])
    comments.objects.create(post=posts.objects.get(id=request.POST["id"]),name=request.user,description=request.POST["desc"]).save()
    context={"post":post}
    return HttpResponse("yes")
    #if request.is_ajax():
    #    html = render_to_string('blog/commentsection.html',context=context,request=request)
     #   return JsonResponse({'form':html})
def saveposts(request):
    post=get_object_or_404(posts,id=request.GET["id"])
    #print(request.user)
    user=User.objects.get(username=request.user)
    #print(user)
    if post in user.savedposts.posts.all():
        user.savedposts.posts.remove(post)
    else:
        user.savedposts.posts.add(post)
    context={"post":post,"total_likes":post.number_of_likes}
        #return HttpResponseRedirect(reverse('blog-home'))
    if request.is_ajax():
        html = render_to_string('blog/likesection.html',context=context,request=request)
        return JsonResponse({'form':html})

def savedpostlist(request):
    c=0
    user=User.objects.get(username=request.user)
    posts1=user.savedposts.posts.all().order_by('-date_posted')
    paginator = Paginator(posts1,10)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    for i in friend_request.objects.all():
            if request.user == i.to_user:
                c+=1
    context={'page_obj':page_obj,'friend_request':friend_request.objects.all(),'fcount':c,'name':user}

    return render(request,'blog/posts_list.html',context)