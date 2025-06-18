from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    birthdate = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.username

    def get_matches(self):
        """Возвращает список пользователей, с которыми есть совпадение."""
        matches_as_user1 = Match.objects.filter(user_id_1=self).values_list('user_id_2', flat=True)
        matches_as_user2 = Match.objects.filter(user_id_2=self).values_list('user_id_1', flat=True)
        matched_user_ids = list(matches_as_user1) + list(matches_as_user2)
        return User.objects.filter(id__in=matched_user_ids)

class Like(models.Model):
    liker = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes_sent', on_delete=models.CASCADE)
    liked = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('liker', 'liked')


class Match(models.Model):
    """Модель для хранения совпадений между пользователями."""
    user_id_1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='matches_as_user1', on_delete=models.CASCADE)
    user_id_2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='matches_as_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_id_1', 'user_id_2')  # Уникальность пары пользователей

    def __str__(self):
        return f"Match: {self.user_id_1} <-> {self.user_id_2}"


class Message(models.Model):
    """Модель для хранения сообщений между пользователями."""
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages_received', on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"


class Preference(models.Model):
    """Модель для хранения предпочтений пользователя."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preference')
    preferred_gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"Preferences of {self.user}"


class UserPhoto(models.Model):
    """Модель для хранения фотографий пользователя."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photos')
    photo_url = models.URLField(max_length=255)
    is_profile = models.BooleanField(default=False)

    def __str__(self):
        return f"Photo of {self.user} (Profile: {self.is_profile})"
