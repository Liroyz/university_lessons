from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Schedule
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Кем вы являетесь??")


class ScheduleForm(forms.ModelForm):

    teacher = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='teacher'),
        label='Преподаватель',
        empty_label=None,
        to_field_name='username',
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Выберите преподавателя',
    )

    class Meta:
        model = Schedule
        fields = ['title', 'date', 'start_time', 'end_time', 'location', 'description', 'teacher']

    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].queryset = User.objects.filter(role='teacher')
        self.fields['teacher'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"


class ScheduleFilterForm(forms.Form):

    search = forms.CharField(required=False, label='Поиск по названию')
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Дата')
    teacher = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='teacher'),
        required=False,
        label='Преподаватель',
        to_field_name='username',
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Выберите преподавателя',
        empty_label='Все преподаватели'
    )

    def __init__(self, *args, **kwargs):
        super(ScheduleFilterForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"