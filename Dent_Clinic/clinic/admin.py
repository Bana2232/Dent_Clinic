from django.contrib import admin

from .models import *


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "patronymic", "email", "phone", "specialization", "category"]
    list_filter = ["specialization", "category", "works_since"]
    search_fields = ["first_name", "last_name", "patronymic", "email", "phone"]
    ordering = ["first_name", "last_name", "patronymic"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "patronymic", "email"]
    list_filter = ["gender", "address"]
    search_fields = ["username", "first_name", "last_name", "patronymic", "email", "phone_number", "address"]
    ordering = ["first_name", "last_name", "patronymic"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]
    list_filter = ["name"]
    search_fields = ["name", "slug"]
    ordering = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["patient", "doctor", "date"]
    list_filter = ["patient", "doctor", "date"]
    search_fields = ["patient", "doctor", "date"]
    ordering = ["date"]


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created", "status"]
    list_filter = ["author", "status", "created", "publish"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["status", "publish"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["patient", "rating", "created"]
    list_filter = ["patient", "rating", "created"]
    search_fields = ["comment"]
    ordering = ["created"]


@admin.register(DoctorImages)
class DoctorImagesAdmin(admin.ModelAdmin):
    list_display = ["doctor", "image"]
    list_filter = ["doctor"]


@admin.register(ServiceImages)
class ServiceImagesAdmin(admin.ModelAdmin):
    list_display = ["service", "image"]
    list_filter = ["service"]


@admin.register(PostSubjects)
class PostSubjectsAdmin(admin.ModelAdmin):
    list_display = ["id", "post_subject"]


@admin.register(PostImages)
class PostImagesAdmin(admin.ModelAdmin):
    list_display = ["post", "image"]
    list_filter = ["post"]
