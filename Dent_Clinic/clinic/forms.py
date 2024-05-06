from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.templatetags.static import static
from django.utils.safestring import SafeText

from .models import User, Appointment, Review

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column


class UserRegistrationForm(UserCreationForm):
    patronymic = forms.CharField(label='Отчество', max_length=30, required=False)
    gender = forms.ChoiceField(label='Пол', choices=User.Gender.choices, initial=User.Gender.MALE)
    date_of_birth = forms.DateField(label='Дата рождения', required=False,
                                    widget=forms.DateInput(attrs={'type': 'date'}))
    phone_number = forms.CharField(label='Телефон', max_length=20, required=False)
    address = forms.CharField(label='Адрес', max_length=250, required=False)

    agrees_with_terms = forms.BooleanField(
        label=SafeText(f"Согласен с <a href='{static('document.jpg')}' download>условиями пользования</a>"),
        initial=False,
        required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username', "first_name", "last_name", 'patronymic', 'gender', 'email', 'password1', 'password2',
            'date_of_birth', 'phone_number',
            'address')


class LoginForm(AuthenticationForm):
    ...


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'patronymic', 'date_of_birth',
                  'address', 'email', 'phone_number']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control is-valid'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control is-valid'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control is-valid'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control is-valid',
                                                    'type': 'date'}, format="%Y-%m-%d"),
            'phone_number': forms.TextInput(attrs={'class': 'form-control is-valid'}),
            'address': forms.TextInput(attrs={'class': 'form-control is-valid'}),
            'email': forms.EmailInput(attrs={'class': 'form-control is-valid'}),
        }

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column("first_name"),
                Column("last_name"),
                Column("patronymic")
            ),

            Row(
                Column("date_of_birth"),
                Column("address")
            ),

            Row(
                Column("phone_number"),
                Column("email")
            )
        )


class CustomPasswordChangeForm(PasswordChangeForm):
    ...


class MakeAppointment(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["doctor", "date"]
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "datetime-local",
                                               "class": "form-select"}, format="%Y-%m-%dT%H:%M"),
            "doctor": forms.Select(attrs={"class": "form-select"})
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["comment", "rating"]
