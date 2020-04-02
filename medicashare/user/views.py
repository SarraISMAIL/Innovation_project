from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render,redirect,reverse,HttpResponseRedirect
from .forms import UserCreationForm ,UserUpdateForm , ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from .models import Post ,Notification
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User

def register(request):
    if request.user.is_authenticated :
        #return redirect(f'/profile/{request.user.username}/')
        return redirect('profile',username=request.user.username)
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            #username = form.cleaned_data['username']
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            messages.success(request, f' {new_user} You are registered successfuly')
            return redirect('login')
            
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {
        'form': form,
    })


@never_cache
def user_login(request):
    if request.user.is_authenticated :
        #return redirect(f'/profile/{request.user.username}/')
        return redirect('profile',username=request.user.username)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #return redirect('/profile/{}/'.format(username))
            return redirect('profile',username=request.user.username)
        else:
            messages.warning(
                request, 'username or password incorrect ')

    return render(request, 'login.html',{'title': 'login',})

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login')
def profile(request,username):
    posts = Post.objects.filter(show_post="yes")
    #nots = Notification.objects.filter(receiver=request.user)
    nots_not_seen = len(Notification.objects.filter(receiver=request.user,status="no"))
    context={
        'posts':posts,
        'nb_nots':nots_not_seen,
        'title':f'MedicaShare | {request.user}',
        'fullname':f'{request.user.first_name}-{request.user.last_name}'
    }
    return render(request,'home.html',context)

####  Post functions ###
 
@login_required(login_url='login')
def post_detail(request,post_id):
    post = get_object_or_404(Post, pk=post_id)
    # if () : click help 
    if request.method == 'POST':
        new_notif =Notification(
            post=post,
            sender=request.user,
            receiver =post.author,
            status="no",
        )
        new_notif.save()
        messages.success(request,f'{post.author} received a msg , and may contact you sooner ')
        return redirect('/requests/detail/{}/'.format(post.id))

    
    context={
        'post':post,
        'title':'Details',
    }
    return render(request,'detail.html',context)

@login_required(login_url='login')
def delete_request_post(request,post_id):
    post_todelete = get_object_or_404(Post, pk=post_id)
    if request.method =='POST':
        post_todelete.show_post ="no"
        post_todelete.save()
        return redirect('my_posts')

    context={
        'post':post_todelete,
        'title':'Delete post',
    }
    return render(request,'delete_post.html',context)

@login_required(login_url='login')   
def update_request(request,post_id):
    post_to_update = get_object_or_404(Post, pk=post_id)
    if request.method =='POST':
        post_to_update.title=request.POST['object']
        post_to_update.content=request.POST['content']
        post_to_update.current_place=request.POST['c_place']

        post_to_update.save()
        messages.success(request,'your post was updated succesfuly ')
        #return redirect(f'/requests/detail/{post_to_update.id}/')

    context={
        'post':post_to_update,
        'title':'Update post',
    }
    return render(request,'update_request.html',context)


@login_required(login_url='login')
def newrequest(request):
    if request.method == 'POST':
        title = request.POST['object']
        content = request.POST['content']
        c_place = request.POST['c_place']
        newpost = Post(
            title=title,
            current_place=c_place,
            content=content,
            author=request.user,
            show_post="yes",
            )
        newpost.save()
        messages.success(
                request, 'Your request was successfuly submited ')
        #url='/requests/detail/{}/'.format(newpost.id)
        #return redirect(url)
    return render(request, 'new_post.html',{'title':"Add new request "})

    
@login_required(login_url='login')
def show_notif(request):
    notifications = Notification.objects.filter(receiver=request.user)
    for notif in notifications :
        notif.status="yes"
        notif.save()
    context={
        'notifications':notifications,
        'title':"Notifications",
    }
    return render(request,'notif.html',context)

@login_required(login_url='login')
def notif_detail(request,notif_id):
    notif = get_object_or_404(Notification,pk=notif_id)
    context={
        'notif':notif,
        'title':'Notifications',
    }
    return render(request,'notif_detail.html',context)
def myposts(request):
    context={
        'title':'My posts',
        'posts':Post.objects.filter(author=request.user,show_post="yes")
    }
    return render(request,'myposts.html',context)

@login_required(login_url='login')
def my_profile(request,username):
    profil = get_object_or_404(User,username=username)
    context={
        'title':f'{request.user.first_name} {request.user.last_name}',
        'profil':profil,
    }
    return render(request,'my_profile.html',context)

@login_required(login_url='login')
def update_profile(request,username):
    profil = get_object_or_404(User,username=username)
    if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = ProfileUpdateForm(
                request.POST, request.FILES, instance=request.user.profile)
            if user_form.is_valid and profile_form.is_valid:
                try:
                    user_form.save()
                    profile_form.save()
                    messages.success(request, 'update success !')
                except:
                    messages.error(request, 'something went wrong , try again ')
            
                
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context={
        'title':'update profile ',
        'profil':profil,
        'user_form': user_form,
        'profile_form': profile_form,
    } 
    return render(request,'update_profile.html',context)

    """
    profil = get_object_or_404(User,username=username)
    if request.method =='POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        phone_number = request.POST['phone_number']
        image = request.POST['image']

        profil.first_name =fname
        profil.last_name =lname
        profil.profile.phone_number = phone_number
        profil.profile.image = image
        profil.profile.save()
        profil.save()

        messages.success(request,'update success ')
    
    context={
        'title':'update profile ',
        'profil':profil,
    }
    return render(request,'update_profile.html',context)"""


def test(request):
    if request.method=='POST':
        subject ='Thank you fro joining us'
        message ='enter this code to accomplish your registartions \n 45568 \n MedicaShare Staff'
        from_email = settings.EMAIL_HOST_USER
        to = [request.POST['email']]

        send_mail(subject,message,from_email,to,fail_silently=True)
    return render(request,'test.html')
