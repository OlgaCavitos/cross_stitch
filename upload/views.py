
# Create your views here.

from django.shortcuts import render, redirect
from django.conf import settings
import os



from .forms import UploadForm, CanvasForm
from .models import UploadedImage
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Calculation
from .forms import CalculationForm
from .forms import FeedbackForm
from .utils import pixelize_and_count

def upload_and_calculate(request):
    uploaded_image = None
    pixelized_image_url = None
    colors_stats = None
    total_thread_length = None

    if request.method == "POST":
        upload_form = UploadForm(request.POST, request.FILES)
        canvas_form = CanvasForm(request.POST)

        if upload_form.is_valid() and canvas_form.is_valid():   #маємо перевірити чи додано файлб якщо ні сповіщення
            uploaded_image = upload_form.save()

            input_path = uploaded_image.image.path
            output_filename = f"pixelized_{uploaded_image.pk}.png"
            output_path = os.path.join(settings.MEDIA_ROOT, output_filename)

            colors_stats, total_thread_length = pixelize_and_count(input_path, output_path)
            pixelized_image_url = settings.MEDIA_URL + output_filename

            # якщо користувач авторизований то зберігаємо
            if request.user.is_authenticated:
                Calculation.objects.create(
                    user=request.user,
                    number=request.user.calculations.count() + 1,
                    comment="Створено запис автоматично",
                    result=total_thread_length
                )
                messages.success(request, "Розрахунок виконано і збережено")
            else:
                # показуємо результат без редіректу
                messages.info(request, "Розрахунок виконано. Щоб зберегти його, зареєструйтесь.")
    else:
        upload_form = UploadForm()
        canvas_form = CanvasForm()

    return render(request, "upload_and_calculate.html", {
        "upload_form": upload_form,
        "canvas_form": canvas_form,
        "uploaded_image": uploaded_image,
        "pixelized_image_url": pixelized_image_url,
        "colors_stats": colors_stats,
        "total_thread_length": total_thread_length,
    })



from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Calculation

class CalculationListView(LoginRequiredMixin, ListView):
    model = Calculation
    template_name = "calculations/list.html"
    context_object_name = "calculations"

    def get_queryset(self):
        return Calculation.objects.filter(user=self.request.user)


class CalculationDetailView(LoginRequiredMixin, DetailView):
    model = Calculation
    template_name = "calculations/detail.html"
    context_object_name = "calculation"

    def get_queryset(self):
        return Calculation.objects.filter(user=self.request.user)


class CalculationCreateView(LoginRequiredMixin, CreateView):
    model = Calculation
    fields = ["comment", "result"]
    template_name = "calculations/create.html"
    success_url = reverse_lazy("calculation_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.number = Calculation.objects.filter(user=self.request.user).count() + 1
        return super().form_valid(form)


class CalculationUpdateView(LoginRequiredMixin, UpdateView):
    model = Calculation
    fields = ["number", "comment", "result"]
    template_name = "calculations/edit.html"
    success_url = reverse_lazy("calculation_list")

    def get_queryset(self):
        return Calculation.objects.filter(user=self.request.user)


class CalculationDeleteView(LoginRequiredMixin, DeleteView):
    model = Calculation
    template_name = "calculations/delete.html"
    success_url = reverse_lazy("calculation_list")

    def get_queryset(self):
        return Calculation.objects.filter(user=self.request.user)



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Вітаємо {username}")
                return redirect('home')   # головна сторінка
            else:
                messages.error(request, "Неправильне ім'я користувача або пароль")
    else:
        form = LoginForm()
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
    messages.success(request, "Ви успішно вийшли із системи.")
    return redirect("home")




def home_page(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback')  # залишаємося на сторінці з формою
    else:
        form = FeedbackForm()

    return render(request, "feedback.html", {"form": form})



