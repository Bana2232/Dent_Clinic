from django.urls import path
from . import views

app_name = "clinic"

urlpatterns = [
    path("", views.index_page, name="index"),
    path("services/", views.service_list, name="services_list"),
    path("calendar/", views.appointments_calendar, name="appointments"),
    path("blog/", views.post_list, name="post_list"),
    path("profile/", views.profile, name="profile"),
    path("<int:year>/<int:month>/<int:day>/<slug:post>",
         views.post_detail,
         name="post_detail"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("about/", views.about, name="about"),
    path("doctors/<int:doctor_id>", views.doctor_detail, name="doctor_detail"),
    path("change_password", views.change_password, name="change_psw"),
    path("services/<slug:service>", views.service_detail, name="service_detail"),
    path("faq/", views.faq_view, name="faq"),
    path("services/<slug:service_slug>/post_comment", views.post_comment, name="post_comment"),
]
