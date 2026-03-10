from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from django.template.loader import render_to_string

from allauth.account.forms import SignupForm


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    '''username = forms.CharField(label="Имя пользователя")
    password1 = forms.CharField(label="Пароль")
    password2 = forms.CharField(label="Повторите пароль")'''

    class Meta:
        model = User
        fields = ("username", 
                  "first_name", 
                  "last_name", 
                  "email", 
                  "password1", 
                  "password2", )



class CommonSignupForm(SignupForm):
    
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)

        html_content = render_to_string(
            'email_messages/hello_message.html',
            {
                'user': user, 
                #'activate_url': activate_url
            }
        )

        send_mail(
            subject='Регистрация в приложении News Portal',
            message='Вы успешно зарегистрировались в приложении News Portal' \
            'Подтвердите свою почту',
            html_message=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return user
        

