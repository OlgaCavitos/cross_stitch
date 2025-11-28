from django import forms
from .models import UploadedImage, Feedback
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']

    def clean_image(self):
        img = self.cleaned_data['image']

        # Дозволені формати
        allowed_ext = ('.jpg', '.jpeg', '.png')

        if not img.name.lower().endswith(allowed_ext):
            raise forms.ValidationError("Дозволені файли: JPG, JPEG або PNG.")

        return img



CANVAS_CHOICES = [
    ("Aida 14", "Aida 14"),
    ("Aida 16", "Aida 16"),
    ("Aida 18", "Aida 18"),
]

class CanvasForm(forms.Form):
    canvas_type = forms.ChoiceField(choices=CANVAS_CHOICES, label="Тип канви")
    width_cm = forms.FloatField(
        label="Ширина матеріалу (см)",
        min_value=10,
        max_value=50
    )
    height_cm = forms.FloatField(
    label="Висота матеріалу (см)",
    min_value = 10,
    max_value = 50
    )

    reserve_cm = forms.FloatField(
        label="Припуск (см)",
        # initial=5,
        min_value=3,   # мінімум 3 см
        max_value=5    # максимум 5 см
    )



class LoginForm(forms.Form):
    username = forms.CharField(max_length=70)
    password = forms.CharField(max_length=70,widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



from .models import Calculation

class CalculationForm(forms.ModelForm):
    class Meta:
        model = Calculation
        fields = ["number", "user", "comment", "result"]



class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше ім’я'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ваш коментар'}),
        }