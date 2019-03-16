from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv

from pytz import timezone
from datetime import datetime, timedelta
from .models import Threads
from .forms import EditProfileForm, CreateThreadForm, ExtendedUserCreationForm

def index_v(request):
    threads_list = Threads.objects.all().order_by('-id')
    query = request.GET.get("search_Post")
    if query:
        threads_list = threads_list.filter(thread_Name__icontains=query)
    paginator = Paginator(threads_list, 10)
    page = request.GET.get('page')
    try:
        threads = paginator.page(page)
    except PageNotAnInteger:
        threads = paginator.page(1)
    except EmptyPage:
        threads = paginator.page(paginator.num_pages)

    delta = 0
    for thread in threads:
        if thread.thread_Expire == "10 mins":
            delta = timedelta(minutes=10)
        elif thread.thread_Expire == "1 hr":
            delta = timedelta(hours=1)
        elif thread.thread_Expire == "1 day":
            delta = timedelta(days=1)
        elif thread.thread_Expire == "1 week":
            delta = timedelta(weeks=1)
        
        d = thread.created_At
        d1 = d+delta

        print(d)
        print(d1)

        expireTime = d1-datetime.now().replace(tzinfo=timezone('UTC'))

        t = Threads.objects.get(id=thread.id)
        t.thread_TillExpire = str(expireTime)
        t.save()

        if d1 < datetime.now().replace(tzinfo=timezone('UTC')):
            Threads.objects.get(id=thread.id).delete()
        else:
            print("Not Expired")

    context = {
        'title': 'Latest Threads',
        'threads': threads
    }

    return render(request, 'threadApp/main.html', context)

def usersThread_v(request):
    threads_list = Threads.objects.filter(thread_Owner=request.user)
    query = request.GET.get("search_Post")
    if query:
        threads_list = threads_list.filter(thread_Name__icontains=query)

    delta = 0
    for thread in threads_list:
        if thread.thread_Expire == "10 mins":
            delta = timedelta(minutes=10)
        elif thread.thread_Expire == "1 hr":
            delta = timedelta(hours=1)
        elif thread.thread_Expire == "1 day":
            delta = timedelta(days=1)
        elif thread.thread_Expire == "1 week":
            delta = timedelta(weeks=1)
        
        d = thread.created_At
        d1 = d+delta

        expireTime = d1-datetime.now().replace(tzinfo=timezone('UTC'))

        t = Threads.objects.get(id=thread.id)
        t.thread_TillExpire = str(expireTime)
        t.save()

        if d1 < datetime.now().replace(tzinfo=timezone('UTC')):
            Threads.objects.get(id=thread.id).delete()

    context = {
        'title': 'Your Created Threads',
        'threads': threads_list
    }

    return render(request, 'threadApp/usersThread.html', context)

def insertThread_v(request):
    if request.method == 'POST':
        form = CreateThreadForm(request.POST)
        if form.is_valid():
            newThread = form.save(commit=False)
            newThread.thread_Owner = request.user
            newThread.save()
            return redirect('/threadApp/details/' + str(newThread.id))
    else:
        form = CreateThreadForm()

    context = {
        'title': 'Create A Thread',
        'form': form
    }
    
    return render(request, 'threadApp/createThread.html', context)

def uploadThread_v(request):
    if request.method == 'POST' and request.FILES['threadDoc']:
        myfile = request.FILES['threadDoc']
        lines = myfile.read().decode("utf-8").split(", ")
        thread = Threads(thread_Owner=request.user, thread_Name=lines[0], thread_Body=lines[1])
        thread.save()

        return redirect('/threadApp/details/' + str(thread.id))
        
    context = {
        'title': 'Upload A File',
        'info': 'File should be a .txt file and contents should be in format(ThreadName, ThreadBody)'
    }

    return render(request, 'threadApp/uploadFile.html', context)

def details_v(request, id):
    thread = Threads.objects.get(id=id)

    context = {
        'thread': thread
    }

    return render(request, 'threadApp/details.html', context)

def threadEdit_v(request, id):
    thread = Threads.objects.get(id=id)

    if request.method == "POST":
        form = CreateThreadForm(request.POST, instance=thread)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.thread_Owner = request.user
            thread.save()
            return redirect('threadApp:usersThread')
    else:
        form = CreateThreadForm(instance=thread)

    context = {
        'title': 'Edit Thread',
        'form': form,
        'thread': thread
    }

    return render(request, 'threadApp/editThread.html', context)

def threadDelete_v(request, id):
    thread = Threads.objects.get(id=id)
    thread.delete()
    return redirect('threadApp:usersThread')

def threadDownload_v(request, id):
    thread = Threads.objects.get(id=id)

    filename = str(thread.id) + ".txt"
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)

    writer = csv.writer(response)
    writer.writerow([thread.thread_Name])
    writer.writerow([thread.thread_Owner])
    writer.writerow([thread.thread_Body])
    writer.writerow([thread.created_At])

    return response

def signup_v(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('threadApp:index')
    else:
        form = ExtendedUserCreationForm()

    context = {
        'title': 'Signup',
        'form': form
    }
    
    return render(request, 'threadApp/signup.html', context)

def login_v(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('threadApp:index')
    else:
        form = AuthenticationForm()

    context = {
        'title': 'Login',
        'form': form
    }

    return render(request, 'threadApp/login.html', context)

def logout_v(request):
    if request.method == 'POST':
        logout(request)
        return redirect('threadApp:index')

def profile_v(request):

    context = {
        'title': 'Profile',
        'user': request.user
    }

    return render(request, 'threadApp/profile.html', context)

def updateProfile_v(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('threadApp:profile')
    else:
        form = EditProfileForm(instance=request.user)

    context = {
        'title': 'Update Profile',
        'form': form
    }

    return render(request, 'threadApp/updateProf.html', context)

def deleteProfile_v(request):
    user = request.user
    user.delete()
    return redirect('threadApp:index')