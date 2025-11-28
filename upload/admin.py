from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import UploadedImage, Calculation, Feedback

class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "uploaded_at")


class CalculationAdmin(admin.ModelAdmin):
    list_display = ("number", "user", "comment", "result", "created_at")
    fields = ("number", "user", "comment", "result", "created_at")
    readonly_fields = ("created_at",)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("name", "comment", "created_at")
    search_fields = ("name", "comment")
    date_hierarchy = "created_at"


# Реєстрація моделей у адмінці
admin.site.register(UploadedImage, UploadedImageAdmin)
admin.site.register(Calculation, CalculationAdmin)
admin.site.register(Feedback, FeedbackAdmin)