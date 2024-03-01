from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import user_passes_test, login_required

# Create your views here.




def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        re_enter_password = request.POST['password1']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        image = request.FILES.get('image')
       
    


        if password == re_enter_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username already exsist')
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.info(request, 'email already exsist')
                return redirect('register')
            
            else:
                user = User.objects.create_user(username=username, email=email, password=password,  phone_number=phone_number, image=image)
                user.save()

                user_login = auth.authenticate(username=username,password=password)
                
                auth.login(request, user_login)
               
                return redirect('home')
              

        
        else:
            messages.info(request, 'invalid data')
            return redirect('register')



    return render(request, 'app/register.html')




def login(request):

    if request.user.is_authenticated:
        return redirect('home')
   
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        
       

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username or password inccorect')

    return render(request, 'app/login.html')



def logout(request):
    auth.logout(request)
    return redirect('login')




def home(request):
    feedbacks = Feedback.objects.all()
    if request.method == "POST":
        user = request.user
        feedback = request.POST['feedback']
        good_or_bad = request.POST['good_or_bad']

        CreateFeedback = Feedback.objects.create(user=user, feedback=feedback,good_or_bad=good_or_bad)
        CreateFeedback.save()
        return redirect('home')

    context = {'feedbacks':feedbacks}


    return render(request, 'app/home.html', context)


def deletecommunity(request, pk):
    community = Community.objects.get(id=pk)

    if request.method == 'POST':

        community.delete()
        if request.user.is_superuser:
            return redirect('admin_panel')
        else:
            return redirect('home')

    return render(request, 'app/delete.html')


def deletefeedback(request, pk):
    feedback = Feedback.objects.get(id=pk)

    if request.method == 'POST':

        feedback.delete()
        return redirect('home')

    return render(request, 'app/delete.html')




def project(request):
    projects = Project.objects.all()    
   

    context = {'projects':projects}
    return render(request, 'app/project.html', context)



def likeproject(request):
    user = request.user.username
    project_id = request.GET.get('project_id')

    project = Project.objects.get(id=project_id)

    likefilter = LikeProject.objects.filter(user=user, project_id=project_id).first()
    

    if likefilter == None:
        newlike = LikeProject.objects.create(user=user, project_id=project_id)
        newlike.save()
        project.no_of_likes = project.no_of_likes+1
        project.save()
        return redirect('project')
    else:
        likefilter.delete()
        project.no_of_likes = project.no_of_likes-1
        project.save()
        return redirect('project')

# ----------like blog end ---------




# @login_required(login_url='login')
def community(request):

    communitys = Community.objects.all()

    if request.method == "POST":
        user = request.user
        question = request.POST['question']
        image = request.FILES.get('image')

        if Community.objects.filter(question=question).exists():
            messages.info(request, 'question already exsist try somethig new')
            return redirect('community_form')
            
        else:
            community_ask = Community.objects.create(user=user, question=question,  image=image)
            community_ask.save()
            return redirect('community')
        
    context = {'communitys':communitys}
    return render(request, 'app/community.html', context)

# @login_required(login_url='login')
def community_post_detail(request, pk):
    
    community = Community.objects.get(id=pk)
    community_comment = community.comment_set.all().order_by('-created')

    
    if request.method == 'POST':
        comment = Comment.objects.create(
            user= request.user,
            community= community,
            body = request.POST.get('body')
        )
        community.no_of_comments = community.no_of_comments +1
    
    commnet_count = len(community_comment)   
    
    context = {'community':community, 'commnet_count':commnet_count,'community_comment':community_comment}
    return render(request, 'app/community_post_detail.html', context)

