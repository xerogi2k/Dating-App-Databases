from django import forms
from .models import User

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'gender', 'birthdate', 'location', 'bio', 'profile_picture']

    def clean_password2(self):
        """Проверка совпадения паролей."""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        """Сохранение пользователя с хешированным паролем."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # Хеширование пароля
        if commit:
            user.save()
        return user

# UserForm для редактирования профиля
class UserForm(forms.ModelForm):
    birthdate = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'})  # Встроенный HTML-виджет выбора даты
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'gender', 'birthdate', 'location', 'bio', 'profile_picture']