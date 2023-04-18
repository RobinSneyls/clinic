from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'))


class PatientRegistrationForm(UserCreationForm):
    # gender = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=GENDER_CHOICES)

    def __init__(self, *args, **kwargs):
        super(PatientRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['gender'].required = True
        self.fields['first_name'].label = "Имя"
        self.fields['last_name'].label = "Фамилия"
        self.fields['email'].label = "Email"
        self.fields['phone_number'].label = "Номер телефона"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Повторите пароль"
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

        # self.fields['gender'].widget = forms.CheckboxInput()

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Введите имя',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Введите фамилию',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Введите Email',
            }
        )
        self.fields['phone_number'].widget.attrs.update(
            {
                'placeholder': 'Введите номер телефона',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Введите пароль',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Повторите пароль',
            }
        )

    class Meta:
        model = User

        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2', 'gender' ]
        error_messages = {
            'first_name': {
                'required': 'First name is required',
                'max_length': 'Name is too long'
            },
            'last_name': {
                'required': 'Last name is required',
                'max_length': 'Last Name is too long'
            },
            'gender': {
                'required': 'Gender is required'
            }
        }

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.role = "patient"
        if commit:
            user.save()
        return user


class DoctorRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(DoctorRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Имя"
        self.fields['last_name'].label = "Фамилия"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Повторите пароль"
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Введите имя',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Введите фамилию',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Введите E-mail',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Введите пароль',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Повторите пароль',
            }
        )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        error_messages = {
            'first_name': {
                'required': 'First name is required',
                'max_length': ' First Name is too long'
            },
            'last_name': {
                'required': 'Last name is required',
                'max_length': 'Last Name is too long'
            }
        }

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.role = "doctor"
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].widget.attrs.update({'placeholder': 'Введите Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Введите пароль'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError("Пользователь уже существувет.")
            if not self.user.check_password(password):
                raise forms.ValidationError("Пароль слабый")
            if not self.user.is_active:
                raise forms.ValidationError("Пользователь заблокированы")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user


class PatientProfileUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PatientProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Введите имя',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Введите фамилию',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Email',
            }
        )
        self.fields['phone_number'].widget.attrs.update(
            {
                'placeholder': 'Номер телефона',
            }
        )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number"]


class DoctorProfileUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DoctorProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Введите имя',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Введите фамилию',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Email',
            }
        )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]