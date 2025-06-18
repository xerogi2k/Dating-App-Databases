from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout
from .models import User, Like, Match
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def home(request):
    """Главная страница с выбором действия."""
    return render(request, 'accounts/home.html')


def register(request):
    """Регистрация пользователя."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile', user_id=user.id)  # Перенаправление на профиль
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    """Страница авторизации."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)  # Авторизация пользователя
            return redirect('profile', user_id=user.id)
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password'})
    return render(request, 'accounts/login.html')

def user_list(request):
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})

def user_detail(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'accounts/user_detail.html', {'user': user})

@login_required
def user_profile(request, user_id):
    """Страница профиля пользователя."""
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'accounts/user_profile.html', {'user': user})

@login_required
def user_logout(request):
    """Выход из аккаунта."""
    logout(request)
    return redirect('home')
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=request.user.user_id)  # Редирект на страницу профиля
    else:
        form = UserForm(instance=request.user)  # Заполняем форму данными пользователя

    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def recommended_profiles(request):
    """Страница с рекомендованными анкетами."""
    user = request.user

    # Фильтруем пользователей: противоположный пол и одинаковый город
    recommended_users = User.objects.filter(
        gender='male' if user.gender == 'female' else 'female',
        location=user.location
    ).exclude(id=user.id)  # Исключаем текущего пользователя

    return render(request, 'accounts/recommended_profiles.html', {'recommended_users': recommended_users})

@login_required
def like_profile(request, user_id):
    """Лайк профиля пользователя."""
    liked_user = User.objects.get(id=user_id)
    Like.objects.get_or_create(liker=request.user, liked=liked_user)
    return redirect('recommended_profiles')  # Возвращаемся на страницу рекомендаций

@login_required
def matches_view(request):
    """Отображает список уникальных совпадений для текущего пользователя."""
    user = request.user
    matches_as_user1 = Match.objects.filter(user_id_1=user).values_list('user_id_2', flat=True)
    matches_as_user2 = Match.objects.filter(user_id_2=user).values_list('user_id_1', flat=True)

    # Уникальные матчи для текущего пользователя
    matched_user_ids = set(matches_as_user1) | set(matches_as_user2)
    matches = User.objects.filter(id__in=matched_user_ids)

    return render(request, 'accounts/matches.html', {'user': user, 'matches': matches})