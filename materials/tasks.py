from celery import shared_task
from django.core.mail import send_mail
import datetime
from materials.models import Course, Subscription
from users.models import User
import pytz


from config.settings import EMAIL_HOST_USER
time_zone = pytz.timezone('Europe/Moscow')


@shared_task
def update_message(pk):
    print('Материалы курса обновились...')
    course = Course.objects.get(pk=pk)
    # print(course.name)
    if course:
        users = User.objects.all()
        if users:
            followed_users_email = []
            for user in users:
                subscription = Subscription.objects.filter(course=pk, user=user.pk)
                if subscription:
                    followed_users_email.append(user.email)
            if len(followed_users_email) > 0:
                print(f'Идет отправка писем... на адреса: {followed_users_email}')
                send_mail(
                    subject=f"Курс '{course.name}'",
                    message=f"Курс '{course.name} был обновлен.",
                    from_email=EMAIL_HOST_USER,
                    recipient_list=followed_users_email,
                )


@shared_task
def filter_last_login():
    users = User.objects.all()
    if users:
        for user in users:
            if user.last_login:
                date = datetime.datetime.now(time_zone)
                condition = datetime.timedelta(weeks=4)
                difference = date - user.last_login
                if difference >= condition:
                    user.is_active = False
                    user.save()
            else:
                user.is_active = False
                user.save()
