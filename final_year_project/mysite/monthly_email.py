

import time,datetime
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import Donation
from django.template.loader import render_to_string

#Monthly email to users
#--sends to all users that have an account
def monthly_emails():
    now = datetime.datetime.now()
    #sends on the 1st day of the month at 12:00
    if now.hour == 12 and now.minute == 0 and now.day == 1:
        all_users = get_user_model().objects.all()
        donations = Donation.objects.prefetch_related().all()
        for i in donations:
            user_donations = Donation.objects.filter(user_id = user)
            for user in all_users:  
                subject = "Monthly roundup from the Barber Institute!"
                email_template_name = 'mysite/monthly_email_template.txt'
                c = {"email": user.email, "site_name": 'The Barber Institute', "user":user,"firstname":user.first_name,'donations':user_donations}
                email = render_to_string(email_template_name, c)
                send_mail(subject, email, 'barberinstiutetest@gmail.com', [user.email],fail_silently=False)
        time.sleep(24*60*60 - 120)
    else:
        time.sleep(15)