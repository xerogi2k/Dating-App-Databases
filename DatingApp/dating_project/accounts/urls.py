from django.urls import path
from . import views

urlpatterns = [
    # Главная страница с регистрацией и входом
    path('', views.home, name='home'),

    # Регистрация при запуске
    path('register/', views.register, name='register'),

    # Вход в аккаунт
    path('login/', views.user_login, name='login'),

    # Выход из аккаунта
    path('logout/', views.user_logout, name='logout'),

    # Список всех пользователей
    path('users/', views.user_list, name='user_list'),

    # Детальная страница пользователя
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),

    # Профиль пользователя
    path('profile/<int:user_id>/', views.user_profile, name='profile'),

    # Редактирование профиля (требует авторизации)
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    # Рекомендуемые профили
    path('recommended/', views.recommended_profiles, name='recommended_profiles'),

    # Лайки
    path('like/<int:user_id>/', views.like_profile, name='like_profile'),

    # Мэтчи
    path('matches/', views.matches_view, name='matches'),
]
