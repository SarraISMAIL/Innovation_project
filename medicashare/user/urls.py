from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns=[
    path('register/',views.register,name="register"),
    path('login/',views.user_login,name="login"),
    path('logout/',views.user_logout,name="logout"),
    path('profile/<str:username>/',views.profile,name="profile"),
    path('newrequest/',views.newrequest,name="newrequest"),
    path('delete-post/<int:post_id>/',views.delete_request_post,name="delete_post"),
    path('update-post/<int:post_id>/',views.update_request,name="update_post"),
    path('notifications/',views.show_notif,name="notification"),
    path('requests/detail/<int:post_id>/',views.post_detail,name="detail"),
    path('notifications/detail/<int:notif_id>/',views.notif_detail,name="notif_detail"),
    path('my-posts/',views.myposts,name="my_posts"),
    path('my-profile/<str:username>/',views.my_profile,name="my_profile"),
    path('update-profile/<str:username>/',views.update_profile,name="update_profile"),
    path('test/',views.test,name='test'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)