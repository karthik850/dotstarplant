from django.urls import path
from . import views
from.views import postlistview,postdetailview,postcreateview,postdeleteview,postupdateview,userpostlistview,BlogPostLike,postlistview1,followview,send_request,accept_request,request_page,reject_request,userpostlistview1,BlogPostLike1,disconnect,commentcreateview,commentcreateview1,disconnect1,saveposts,savedpostlist


urlpatterns = [
    path('',views.postlistview1,name="blog-home"),
    #path('user/<str:username>/',userpostlistview.as_view(),name="user-posts"),
    path('user/<str:username>/',views.userpostlistview1,name="user-posts"),
    path('myposts/',views.myposts,name="myposts"),
    path('mysearch/',views.searchposts,name="mysearch"),
    path('posts/<int:pk>/',postdetailview.as_view(),name="post-detail"),
    path('posts/create/',postcreateview.as_view(),name="post-create"),
    path('posts/<int:pk>/update/',postupdateview.as_view(),name="post-update"),
    path('posts/<int:pk>/delete/',postdeleteview.as_view(),name="post-delete"),
    path('blogpost-like/<int:pk>/', views.BlogPostLike, name="blogpost_like"),
    path('blogpost-like1/', views.BlogPostLike1, name="blogpost_like1"),
    path('follow/<str:username>/',views.followview,name="follower"),
    path('disconnect/<str:username>/',views.disconnect,name="disconnect"),
    path('disconnect1/',views.disconnect1,name="disconnect1"),
    path('send_request/<str:username>/',views.send_request,name="send_request"),
    path('accept_request/<int:requestID>/<str:username>/',views.accept_request,name="accept_request"),
    path('request_page',views.request_page,name="request_page"),
    path('reject_request/<int:requestID>/<str:username>/',views.reject_request,name="reject_request"),
    path('about/',views.about,name="blog-about"),
    path('comment/<int:pk>/',views.commentcreateview,name="addcomment"),
    path('comment1/',views.commentcreateview1,name="addcomment1"),
    path('save/',views.saveposts,name="save"),
    path('savedposts/',views.savedpostlist,name="saved-posts"),
]