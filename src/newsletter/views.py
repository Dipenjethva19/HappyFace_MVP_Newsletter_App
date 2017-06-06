from django.conf import settings
from django.shortcuts import render
from .forms import ContactForm, SignUpForm
from django.core.mail import send_mail
from .models import SignUp


# Create your views here.
def home(request):
    title = 'Sign Up Now'
    # if request.user.is_authenticated:
    #     title = 'Welcome To my App. %s' % request.user
    # if request.method == 'POST':
    #     print(request.POST)
    form = SignUpForm(request.POST or None)
    context = {
        'title': title,
        'form': form
    }

    if form.is_valid():
        instance = form.save(commit=False)
        full_name = form.cleaned_data.get("full_name")
        if not full_name:
            full_name = "new any user"
        instance.full_name = full_name

        # if not instance.full_name:
        #     instance.full_name = 'Any User'
        form.save()
        context = {
            "title": 'Thank You'
        }

    if request.user.is_authenticated() and request.user.is_staff:
        for instance in SignUp.objects.all():
            print(instance.email)
        queryset = SignUp.objects.all()
        context = {
            'queryset': queryset
        }

    return render(request, "home.html", context)


def contact(request):
    title = 'Contact Us'
    form = ContactForm(request.POST or None)
    if form.is_valid():
        for key in form.cleaned_data:
            # print(key)
            # print(form.cleaned_data.get(key))
            form_email = form.cleaned_data.get('email')
            form_message = form.cleaned_data.get('message')
            form_full_name = form.cleaned_data.get('full_name')
            some_html_message = """
            <h1>Hello</h1>
            """
            # print(email,message,full_name)
            subject = 'EmailTesting'
            from_email = settings.EMAIL_HOST_USER
            to_email = [from_email, ]

            contact_message = "%s: %s via %s" % (
                form_full_name,
                form_message,
                form_email
            )
            send_mail(
                subject,
                contact_message,
                from_email,
                to_email,
                html_message=some_html_message,
                fail_silently=False
            )
            send_mail(
                'Subject here',
                'Here is the message.',
                'from@example.com',
                ['to@example.com'],
                fail_silently=False,
            )
    context = {
        'form': form,
        'title': title
    }
    return render(request, 'forms.html', context)
