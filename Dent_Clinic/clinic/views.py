import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mail

from .forms import UserRegistrationForm, LoginForm, EditProfileForm, CustomPasswordChangeForm, MakeAppointment, \
    ReviewForm
from .models import BlogPost, Doctor, Appointment, Service, Review
from .func import make_calendar_page


def index_page(request):
    user = request.user
    appointments = Appointment.objects.filter(patient=user.id)

    return render(request, "index.html",
                  {"user": user,
                   "appointments": appointments})


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("clinic:index")

    else:
        form = UserRegistrationForm()

    return render(request, "register.html",
                  {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd["username"],
                                password=cd["password"])

            if user is not None:
                login(request, user)
                return redirect(reverse("clinic:profile"))

    else:
        form = LoginForm(request)

    return render(request, "login.html",
                  {"form": form})


def logout_view(request):
    logout(request)
    return redirect(reverse("clinic:profile"))


def service_list(request):
    services = Service.objects.all()

    return render(request, "service_list.html",
                  {"services": services})


def service_detail(request, service):
    serv = get_object_or_404(Service, slug=service)
    comments = Review.objects.filter(service__id=serv.id)

    paginator = Paginator(comments, 4)
    page_number = request.GET.get("page", 1)

    try:
        comments = paginator.page(page_number)

    except EmptyPage:
        comments = paginator.page(1)

    except PageNotAnInteger:
        comments = paginator.page(1)

    doctors = Doctor.objects.all()
    sent = False

    if request.method == "POST":
        form = MakeAppointment(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)

            appointment.patient = request.user
            appointment.target = serv

            subject = f"Запись на приём"
            message = f"Вы записались на приём к {appointment.doctor} на {appointment.date}.\n"

            send_mail(subject, message, "zubenkop2705@gmail.com",
                      [request.user.email])

            appointment.save()
            sent = True
    else:
        form = MakeAppointment()

    return render(request, "service_detail.html",
                  {"service": serv, "doctors": doctors,
                   "form": form, "sent": sent,
                   "comments": comments, "paginator": paginator})


def faq_view(request):
    return render(request, "faq.html")


def post_list(request):
    posts_list = BlogPost.published.all()

    paginator = Paginator(posts_list, per_page=9)
    page_number = request.GET.get("page", 1)

    try:
        posts = paginator.page(page_number)

    except EmptyPage:
        posts = paginator.page(1)

    except PageNotAnInteger:
        posts = paginator.page(1)

    return render(request, "post_list.html",
                  {"posts": posts, "paginator": paginator})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(BlogPost,
                             status=BlogPost.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request, "post_detail.html",
                  {"post": post})


def profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = EditProfileForm(request.POST, instance=request.user)

            if form.is_valid():
                form.save()
                return redirect(reverse("clinic:profile"))

        else:
            form = EditProfileForm(instance=request.user)

    else:
        form = None

    return render(request, "profile.html",
                  {"user": request.user,
                   "form": form})


@login_required
def change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect(reverse("clinic:profile"))

    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, "change_password.html",
                  {"user": request.user,
                   "form": form})


def appointments_calendar(request):
    user = request.user
    appointments = user.patient_appointments.all()

    today = datetime.datetime.today()

    day = int(request.GET.get("day", today.day))
    month = int(request.GET.get("month", today.month))
    year = int(request.GET.get("year", today.year))

    next_month = (month + 1) % 12 if month != 11 else 12
    prev_month = month - 1 if month != 1 else 12

    next_year = year + 1 * (next_month == 1)
    prev_year = year - 1 * (prev_month == 12)

    selected_date = datetime.date(year=year,
                                  month=month, day=day)

    cal = make_calendar_page(datetime.date(year=year,
                                           month=month, day=1))

    clicked = request.GET.get("clicked", "False")
    clicked = clicked == "True"

    app_id = request.GET.get("app_id", None)

    if clicked and app_id:
        sel_app = appointments.get(id=app_id)

    else:
        sel_app = None

    show = request.GET.get("show", "1")
    now = timezone.now()

    if show == "1":
        appointments = appointments.filter(date__gt=now)

    elif show == "2":
        appointments = appointments.filter(date__lt=now)

    filt_date = request.GET.get("filt_date", None)

    if filt_date:
        filt_date = list(map(int, filt_date.split(".")))
        filt_date = datetime.date(day=filt_date[0], month=filt_date[1], year=filt_date[2])

        appointments = appointments.filter(date__date=filt_date)

    paginator = Paginator(appointments, 8)
    page_number = request.GET.get("page", 1)

    try:
        appointments = paginator.page(page_number)

    except EmptyPage:
        appointments = paginator.page(1)

    except PageNotAnInteger:
        appointments = paginator.page(1)

    return render(request, "appointments_page.html",
                  {"calendar": cal, "sel_date": selected_date,
                   "prev_month": prev_month, "next_month": next_month,
                   "prev_year": prev_year, "next_year": next_year,
                   "clicked": clicked, "appointments": appointments,
                   "sel_app": sel_app, "show": show,
                   "now": now})


def post_comment(request, service_slug):
    service = get_object_or_404(Service, slug=service_slug)

    if request.method == "POST":
        form = ReviewForm(data=request.POST)

        if form.is_valid():
            comment = form.save(commit=False)

            comment.service = service
            comment.patient = request.user

            comment.save()

        return redirect("clinic:service_detail", service_slug)

    else:
        form = ReviewForm()

    return render(request, "comment_form.html",
                  {"form": form})


def about(request):
    doctors = Doctor.objects.all()

    return render(request, "about.html",
                  {"doctors": doctors})


def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor,
                               id=doctor_id)

    return render(request, "doctor_detail.html",
                  {"doctor": doctor})


def users_only(request):
    ...
