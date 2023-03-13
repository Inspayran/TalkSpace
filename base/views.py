from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from accounts.forms import MyUserCreationForm
from accounts.models import MyUser
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Topic, Room, Message
from .forms import RoomForm, UserForm


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        if not password:
            messages.error(request, 'Please enter your password')
            return render(request, 'base/login.html')

        try:
            user = MyUser.objects.get(username=username)
        except MyUser.DoesNotExist:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    return render(request, 'base/login.html')


def logout_user(request):
    logout(request)
    return redirect('home')


def register_page(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {
        'form': form,
    }
    return render(request, 'base/register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q),
    )
    topics = Topic.objects.all()[0:6]
    room_messages = Message.objects.all()
    rooms_count = Room.objects.count()

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_messages': room_messages,
        'rooms_count': rooms_count,
    }
    return render(request, 'base/home.html', context)


def room_page(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants,
    }
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def create_room(request):
    topics = Topic.objects.all()
    form = RoomForm()

    if request.method == 'POST':
        topic_name = request.POST.get('topic').capitalize()
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {
        'form': form,
        'topics': topics,
    }
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topic = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('room', room.id)

    context = {
        'room': room,
        'form': form,
        'topic': topic,
    }
    return render(request, 'base/update_room.html', context)


def profile_page(request, pk):
    user = MyUser.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    rooms_count = Room.objects.count()

    context = {
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics,
        'rooms_count': rooms_count,
        'user': user,
    }
    return render(request, 'base/profile.html', context)


def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete_room.html', {'obj': room, })


def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete_room.html', {'obj': message, })


def update_user(request, pk):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('profile', user.id)

    return render(request, 'base/update_user.html', {'form': form})


def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {
        'topics': topics,
    }
    return render(request, 'base/topics.html',context)
