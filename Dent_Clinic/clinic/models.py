from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone

from datetime import date


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=BlogPost.Status.PUBLISHED)


class Doctor(models.Model):
    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)

    date_of_birth = models.DateField()

    email = models.EmailField()
    phone = models.CharField(max_length=20)

    class Specialization(models.TextChoices):
        WITHOUT_SPEC = "WS", "Нет"
        FIRST_SPEC = "FS", "Первая"
        SECOND_SPEC = "SS", "Вторая"
        HIGHER_SPEC = "HS", "Высшая"

    specialization = models.CharField(max_length=100)
    category = models.CharField(max_length=2, choices=Specialization.choices,
                                default=Specialization.WITHOUT_SPEC)
    works_since = models.DateField(null=True)
    bio = models.TextField()

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"

    @property
    def experience_years(self):
        dif = (date.today() - self.works_since).days // 365

        if dif == 0:
            return "менее года"

        if str(dif)[-1] == 1:
            return f"{dif} год"

        return f'{dif} {"года" if "2" <= str(dif)[-1] <= "4" and dif != 14 else "лет"}'

    @property
    def get_years_old(self):
        dif = (date.today() - self.date_of_birth).days // 365

        if str(dif)[-1] == "1":
            return f"{dif} год"

        return f'{dif} {"года" if "2" <= str(dif)[-1] <= "4" else "лет"}'

    def __str__(self):
        return self.full_name


class User(AbstractUser):
    class Gender(models.TextChoices):
        FEMALE = "F", "Женский"
        MALE = "M", "Мужской"

    patronymic = models.CharField(max_length=30, null=True, verbose_name="Отчество")
    gender = models.CharField(max_length=1,
                              choices=Gender.choices,
                              default=Gender.MALE, null=True,
                              verbose_name="Пол")

    date_of_birth = models.DateField(null=True, verbose_name="Дата рождения")
    registration_date = models.DateField(auto_now_add=True, null=True, verbose_name="Дата регистрации")

    phone_number = models.CharField(max_length=20, null=True, verbose_name="Номер телефона")
    address = models.CharField(max_length=250, null=True, verbose_name="Адрес")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username


class Service(models.Model):
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def get_absolute_url(self):
        return reverse("clinic:service_detail", args=[self.slug])

    def __str__(self):
        return self.name


class Appointment(models.Model):
    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

        ordering = ["-date"]
        indexes = [models.Index(fields=["-date"])]

    patient = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="patient_appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,
                               related_name="doctor_appointments")
    date = models.DateTimeField()
    target = models.ForeignKey(Service, on_delete=models.CASCADE,
                               related_name="service_appointments",
                               null=True)

    def __str__(self):
        return f"Запись к {self.doctor}"

    @property
    def time_before_appoinment(self):
        dif = timezone.now() - self.date

        if dif.days == 0:
            return f"Сегодня в {self.date.strftime('%H:%M')}"

        if dif.days == 1:
            return f"Завтра в {self.date.strftime('%H:%M')}"

        if dif.days < 0:
            return f"Приём завершён {self.date.strftime('%d %B %Y')}"

        return f'{self.date.strftime("%d %B %Y")}'


class BlogPost(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Черновик"
        PUBLISHED = "PB", "Опубликован"

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique_for_date="created")

    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.PUBLISHED)

    created = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

        ordering = ["-publish"]
        indexes = [models.Index(fields=["-publish"])]

    def get_absolute_url(self):
        return reverse("clinic:post_detail", args=[self.publish.year,
                                                   self.publish.month,
                                                   self.publish.day,
                                                   self.slug])


class Review(models.Model):
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв {self.patient} {self.created}"


class DoctorImages(models.Model):
    class Meta:
        verbose_name = "Фотография врача"
        verbose_name_plural = "Фотографии врачей"

    def image_path(self, filename):
        return f"clinic/static/DoctorsPhoto/{str(self.doctor.id)}/{filename}"

    doctor = models.ForeignKey(Doctor,
                               on_delete=models.CASCADE,
                               related_name="doctor_image")
    image = models.ImageField(upload_to=image_path)


class ServiceImages(models.Model):
    class Meta:
        verbose_name = "Изображение услуги"
        verbose_name_plural = "Изображения услуг"

    def image_path(self, filename):
        return f"clinic/static/ServiceImages/{str(self.service.id)}/{filename}"

    service = models.ForeignKey(Service,
                                on_delete=models.CASCADE,
                                related_name="service_image")
    image = models.ImageField(upload_to=image_path,
                              default="clinic/static/no_photo.png")


class ServiceVideo(models.Model):
    class Meta:
        verbose_name = "Видео услуги"
        verbose_name_plural = "Видео услуг"

    def video_path(self, filename):
        return f"clinic/static/ServiceVideo/{str(self.service.id)}/{filename}"

    service = models.ForeignKey(Service,
                                on_delete=models.CASCADE,
                                related_name="service_video")
    video = models.FileField(upload_to=video_path)


class PostImages(models.Model):
    class Meta:
        verbose_name = "Изображение поста"
        verbose_name_plural = "Изображения постов"

    def image_path(self, filename):
        return f"clinic/static/PostImages/{str(self.post.id)}/{filename}"

    post = models.ForeignKey(BlogPost,
                             on_delete=models.CASCADE,
                             related_name="post_image")

    image = models.ImageField(upload_to=image_path)
