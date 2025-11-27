
# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import os


from .forms import UploadForm, CanvasForm
from .models import UploadedImage
from .utils import pixelize_and_count
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Calculation
from .forms import CalculationForm


def upload_and_calculate(request):
    upload_form = UploadForm()
    canvas_form = CanvasForm()
    uploaded_image = None
    pixelized_image_url = None
    colors_stats = None
    total_thread_length = None

    if request.method == "POST":
        upload_form = UploadForm(request.POST, request.FILES)
        canvas_form = CanvasForm(request.POST)

        # зберігаємо зображення, якщо валідне
        if upload_form.is_valid():
            uploaded_image = upload_form.save()

        # якщо зображення є, виконуємо розрахунок кольорів (без параметрів канви)
        if uploaded_image:
            input_path = uploaded_image.image.path
            output_filename = f"pixelized_{os.path.basename(input_path)}"
            output_path = os.path.join(settings.MEDIA_ROOT, output_filename)

            colors_stats, total_thread_length = pixelize_and_count(
                input_path,
                output_path,
                max_colors=30
            )
            pixelized_image_url = settings.MEDIA_URL + output_filename

    return render(request, "upload_and_calculate.html", {
        "upload_form": upload_form,
        "canvas_form": canvas_form,
        "uploaded_image": uploaded_image,
        "pixelized_image_url": pixelized_image_url,
        "colors_stats": colors_stats,
        "total_thread_length": total_thread_length
    })



@login_required
def calculation_list(request):
    calculations = request.user.calculations.all()
    return render(request, "calculations/list.html", {"calculations": calculations})

@login_required
def calculation_create(request):
    if request.method == "POST":
        form = CalculationForm(request.POST)
        if form.is_valid():
            calc = form.save(commit=False)
            calc.user = request.user
            calc.save()
            return redirect("calculation_list")
    else:
        form = CalculationForm()
    return render(request, "calculations/create.html", {"form": form})

@login_required
def calculation_delete(request, pk):
    calc = get_object_or_404(Calculation, pk=pk, user=request.user)
    calc.delete()
    return redirect("calculation_list")



def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    elif request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Вітаємо {username}")
                return redirect('home')
            else:
                messages.error(request, "Неправильне ім'я користувача або пароль")
        return render(request, "login.html", {"form": form})

def register_view(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "register.html", {"form": form})
    elif request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Реєстрація успішна")
            return redirect ('upload_and_calculate')
        return render(request, "register.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "Ви успішни вийшли із системи")
    return redirect('login')




