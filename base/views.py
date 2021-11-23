from django.http.response import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import redirect, render
from .models import Group, Task, Message
from base.forms import UserForm, SignUpForm, GroupForm, MessageForm, TaskForm, EditProfileForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q

User = get_user_model()


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'base/pages/home.html')


@login_required(login_url='login')
def dashboard(request):
    task_form = TaskForm()
    query = request.GET.get('q') if request.GET.get('q') is not None else ''
    tasks = request.user.task_set.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )
    groups = Group.objects.filter(
        Q(host=request.user) |
        Q(members=request.user)
    )
    context = {'task_form': task_form, 'tasks': tasks, 'groups': groups, 'query': query}
    return render(request, 'base/pages/dashboard.html', context)


def about(request):
    return render(request, 'base/pages/about.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'GET':
        return render(request, 'base/pages/auth/register.html', {'form': SignUpForm()})

    elif request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = new_user.username.lower()
            new_user.save()
            
            login(request, new_user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid form request.')
            return redirect('register')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'GET':
        form = UserForm()
        return render(request, 'base/pages/auth/login.html', {'form': form})

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Password Incorrect.')
            return redirect('login')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@login_required(login_url='login')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required(login_url='login')
def groups(request):
    query = request.GET.get('q') if request.GET.get('q') is not None else ''
    groups = Group.objects.filter(
        Q(host=request.user) |
        Q(members=request.user)
    ).filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )
    context = {'groups': groups, 'query': query, 'back': True}
    return render(request, 'base/pages/groups/feed.html', context)


@login_required(login_url='login')
def show_group(request, uuid):
    try:
        group = Group.objects.get(uuid=uuid)
    except:
        return HttpResponseNotFound('Group does not exist.')

    show_group_allowed = group.host == request.user or group.members.filter(uuid__contains=request.user.uuid).exists()

    if show_group_allowed:
        query = request.GET.get('q') if request.GET.get('q') is not None else ''
        tasks = group.task_set.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
        group_messages = group.message_set.all
        task_form = TaskForm()
        message_form = MessageForm()

        context = {
            'group': group,
            'uuid': group.uuid,
            'tasks': tasks,
            'group_messages': group_messages,
            'task_form': task_form,
            'message_form': message_form,
        }
        return render(request, 'base/pages/groups/show.html', context)
    else:
        return HttpResponseForbidden('You are not allowed to do that.')


@login_required(login_url='login')
def group_members(request, uuid):
    try:
        group = Group.objects.get(uuid=uuid)
    except:
        return HttpResponseNotFound('Group does not exist.')
    
    group_members_allowed = group.host == request.user or group.members.filter(uuid__contains=request.user.uuid).exists()
    
    if group_members_allowed:
        
        if request.method == 'GET':
            query = request.GET.get('q') if request.GET.get('q') is not None else ''
            members = group.members.filter(username__icontains=query)
            
            context = {'members': members, 'uuid': group.uuid, 'host': group.host, 'query': query, 'back': True}
            return render(request, 'base/pages/groups/members.html', context)

        elif request.method == 'POST':
            try:
                new_member = User.objects.get(username=request.POST.get('username'))
            except:
                messages.error(request, 'User does not exist.')
                return redirect('group_members', uuid=uuid)

            if new_member == group.host:
                return HttpResponseBadRequest('You cannot add yourself.')

            if request.user == group.host:
                group.members.add(new_member)
                group.save()

                return redirect('group_members', uuid=uuid)
            else:
                return HttpResponseForbidden('You are not allowed to do that.')
        else:
            return HttpResponseNotAllowed(['GET', 'POST'])
    else:
        return HttpResponseForbidden('You are not allowed to do that.')


@login_required(login_url='login')
def delete_member(request, group_uuid, member_uuid):
    if request.method == 'POST':
        try:
            group = Group.objects.get(uuid=group_uuid)
        except:
            return HttpResponseNotFound('Group does not exist.')

        if request.user == group.host:
            try:
                user = User.objects.get(uuid=member_uuid)
            except:
                return HttpResponseNotFound('User does not exist.')
            group.members.remove(user)
            group.save()
            
            return redirect('group_members', uuid=group.uuid)
        else:
            return HttpResponseForbidden('You are not allowed to do that.')
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required(login_url='login')
def group_messages(request, uuid):
    message_form = MessageForm()
    query = request.GET.get('q') if request.GET.get('q') is not None else ''
    try:
        group = Group.objects.get(uuid=uuid)
    except:
        return HttpResponseNotFound('Group does not exist.')
    
    group_messages_allowed = group.host == request.user or group.members.filter(uuid__contains=request.user.uuid).exists()

    if group_messages_allowed:
        group_messages = group.message_set.filter(
            Q(body__icontains=query) |
            Q(user__username__icontains=query)
        )
        context = {'group_messages': group_messages, 'uuid': group.uuid, 'message_form': message_form, 'query': query}
        return render(request, 'base/pages/groups/messages.html', context)
    else:
        return HttpResponseForbidden('You are not allowed to do that.')


@login_required(login_url='login')
def create_group(request):
    if request.method == 'GET':
        group_form = GroupForm()
        return render(request, 'base/pages/groups/create.html', {'group_form': group_form})

    elif request.method == 'POST':
        group_form = GroupForm(request.POST)

        if group_form.is_valid():
            new_group = group_form.save(commit=False)
            new_group.host = request.user
            new_group.save()
            
            return redirect('groups')
        else:
            messages.error(request, 'Invalid form request.')
            return redirect('create_group')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@login_required(login_url='login')
def update_group(request, uuid):
    try:
        group = Group.objects.get(uuid=uuid)
    except:
        return HttpResponseNotFound('Group does not exist.')

    if group.host != request.user:
        return HttpResponseForbidden('You are not allowed to do that.')

    if request.method == 'GET':
        group_form = GroupForm(instance=group)
        context = {'group_form': group_form, 'uuid': group.uuid, 'back': True}
        return render(request, 'base/pages/groups/edit.html', context)

    elif request.method == 'POST':
        group_form = GroupForm(request.POST, instance=group)
        if group_form.is_valid():
            group_form.save()
            return redirect('show_group', uuid=uuid)
        else:
            messages.error(request, 'Invalid form request.')
            return redirect('update_group', uuid=uuid)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@login_required(login_url='login')
def delete_group(request, uuid):
    if request.method == 'POST':
        try:
            group = Group.objects.get(uuid=uuid)
        except:
            return HttpResponseNotFound('Group does not exist.')

        if group.host == request.user:
            group.delete()
            return redirect('groups')
        else:
            return HttpResponseForbidden('You are not allowed to do that.')
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required(login_url='login')
def show_task(request, uuid):
    try:
        task = Task.objects.get(uuid=uuid)
    except:
        return HttpResponseNotFound('Task does not exist.')

    show_task_allowed = task.user == request.user or task.group and task.group.host == request.user or task.group.members.filter(uuid__contains=request.user.uuid).exists()

    if show_task_allowed:
        return render(request, 'base/pages/tasks/show.html', {'task': task, 'back': True})
    else:
        return HttpResponseForbidden('You are not allowed to do that.')


@login_required(login_url='login')
def create_group_task(request, uuid):
    try:
        group = Group.objects.get(uuid=uuid)
    except:
        return HttpResponseNotFound('Group does not exist.')

    create_group_task_allowed = group.host == request.user or group.members.filter(uuid__contains=request.user.uuid).exists()
    if not create_group_task_allowed:
        return HttpResponseForbidden('You are not allowed to do that.')

    if request.method == 'GET':
        task_form = TaskForm()
        context = {
            'task_form': task_form,
            'uuid': group.uuid,
            'back': True
        }
        return render(request, 'base/pages/tasks/create.html', context)

    elif request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            new_task = task_form.save(commit=False)
            new_task.user = request.user
            new_task.group = group
            new_task.save()
            return redirect('show_group', uuid=uuid)
        else:
            messages.error(request, 'Invalid form request.')
            return redirect('create_group_task', uuid=uuid)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@login_required(login_url='login')
def create_task(request):
    if request.method == 'GET':
        task_form = TaskForm()
        context = {'task_form': task_form, 'back': True}
        return render(request, 'base/pages/tasks/create.html', context)
    elif request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            new_task = task_form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid form request.')
            return redirect('dashboard')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@login_required(login_url='login')
def update_task(request, uuid):
    try:
        task = Task.objects.get(uuid=uuid)
    except:
        return HttpResponseNotFound('Task does not exist.')
        
    update_task_allowed = task.user == request.user or task.group and task.group.host == request.user

    if update_task_allowed:
        if request.method == 'GET':
            task_form = TaskForm(instance=task)
            return render(request, 'base/pages/tasks/edit.html', {'task_form': task_form, 'uuid': uuid, 'back': True})

        elif request.method == 'POST':
            task_form = TaskForm(request.POST, instance=task)
            if task_form.is_valid():
                task_form.save()
                
                if task.group:
                    return redirect('show_group', uuid=task.group.uuid)
                else:
                    return redirect('dashboard')
            else:
                messages.error(request, 'Invalid form request.')
                return redirect('update_task', uuid=uuid)
        else:
            return HttpResponseNotAllowed(['GET', 'POST'])
    else:
        return HttpResponseForbidden('You are not allowed to do that.')


@login_required(login_url='login')
def toggle_task_done(request, uuid):
    if request.method == 'POST':
        try:
            task = Task.objects.get(uuid=uuid)
        except:
            return HttpResponseNotFound('Task does not exist.')

        toggle_task_done_allowed = task.user == request.user or task.group and task.group.host == request.user or task.group.members.filter(uuid__contains=request.user.uuid).exists()

        if toggle_task_done_allowed:
            task.done = not task.done
            task.save()
            
            if task.group:
                return redirect('show_group', uuid=task.group.uuid)
            else:
                return redirect('dashboard')
        else:
            return HttpResponseForbidden('You are not allowed to do that.')
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required(login_url='login')
def delete_task(request, uuid):
    if request.method == 'POST':
        try:
            task = Task.objects.get(uuid=uuid)
        except:
            return HttpResponseNotFound('Task does not exist.')

        delete_task_allowed = task.user == request.user or task.group and task.group.host == request.user

        if delete_task_allowed:
            task.delete()

            if task.group:
                return redirect('show_group', uuid=task.group.uuid)
            else:
                return redirect('dashboard')
        else:
            return HttpResponseForbidden('You are not allowed to do that.')
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required(login_url='login')
def send_message(request, uuid):
    if request.method == 'POST':
        try:
            group = Group.objects.get(uuid=uuid)
        except:
            return HttpResponseNotFound('Group does not exist.')
            
        send_message_allowed = group.host == request.user or group.members.filter(uuid__contains=request.user.uuid).exists()

        if send_message_allowed:
            message_form = MessageForm(request.POST)

            if message_form.is_valid():
                new_message = message_form.save(commit=False)
                new_message.user = request.user
                new_message.group = group
                new_message.save()
            else:
                messages.error(request, 'Invalid form request.')
            
            return redirect('show_group', uuid=uuid)

        else:
            return HttpResponseForbidden('You are not allowed to do that.')
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required(login_url='login')
def delete_message(request, uuid):
    if request.method == 'POST':
        try:
            message = Message.objects.get(uuid=uuid)
        except:
            return HttpResponseNotFound('Message does not exist.')

        delete_message_allowed = message.user == request.user or message.group.host == request.user

        if delete_message_allowed:
            message.delete()
            return redirect('show_group', uuid=message.group.uuid)
        else:
            return HttpResponseForbidden('You are not allowed to do that.')
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required(login_url='login')
def profile(request, uuid):
    try:
        user = User.objects.get(uuid=uuid)
    except:
        return HttpResponseNotFound('User does not exist.')

    return render(request, 'base/pages/profile.html', {'user': user})


@login_required(login_url='login')
def edit_profile(request):
    form = EditProfileForm(instance=request.user)
    
    if request.method == 'GET':
        return render(request, 'base/pages/edit_profile.html', {'form': form, 'back': True})

    elif request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, 'Invalid form request.')

        return redirect('profile', uuid=request.user.uuid)

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])