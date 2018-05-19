import os
from django.contrib import messages
from django.http import HttpResponse
from .forms import *
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View
from datetime import datetime, timedelta
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# ##############################################CLASS BASED VIEWS######################################################
class ThursdayUpdateView(LoginRequiredMixin, UpdateView):
    model = Thursday
    template_name = 'thursdays/thursday_update.html'
    form_class = UpdateThursdayForm

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        thursday_obj = Thursday.objects.get(id=pk)
        assigned_company = thursday_obj.assigned_company

        form = UpdateThursdayForm(initial={'name': assigned_company.name,
                                           'website': assigned_company.website,
                                           'facebook': assigned_company.facebook,
                                           'description': assigned_company.description,
                                           'email_one': assigned_company.email_one,
                                           'email_two': assigned_company.email_two,
                                           'pmm_date': assigned_company.pmm_date})
        return render(request, self.template_name, {'thursday_form': form})

    def post(self, request, **kwargs):
        pk = self.kwargs['pk']
        queried_thursday = Thursday.objects.get(id=pk)
        if request.method == 'POST':
            form = UpdateThursdayForm(request.POST, instance=queried_thursday)
            if form.is_valid():
                thursday = form.save(commit=False)

                company = thursday.assigned_company
                company.website = form.cleaned_data['website']
                company.facebook = form.cleaned_data['facebook']
                company.description = form.cleaned_data['description']
                company.email_one = form.cleaned_data['email_one']
                company.email_two = form.cleaned_data['email_two']
                company.save()

                if form.cleaned_data['name'] is None or form.cleaned_data['name'] == '':
                    thursday.assigned_company = None
                    thursday.scheduled = False
                    company.is_registered = False
                    company.save()

                thursday.save()
                return redirect('/')
        else:
            form = UpdateThursdayForm()
        return render(request, self.template_name, {'thursday_form': form})


class ThursdayListView(ListView):
    model = Thursday
    template_name = 'thursdays/thursday_list.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        """
        :param args:
        :param object_list:
        :param kwargs:
        :return: a context dictionary to be accessed in the template
        """
        context = super(ThursdayListView, self).get_context_data(*args, **kwargs)
        context['thursday_list'] = Thursday.objects.order_by('date').filter(is_currently_available=True)
        return context


class ThursdayDetailView(DetailView):
    template_name = 'thursdays/thursday_detail.html'
    model = Thursday


class ThursdayCreateView(CreateView):
    form_class = ThursdayForm
    template_name = 'thursdays/thursday_form.html'

    def get(self, request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return: a rendering of the proper form
        """
        form_one = self.form_class(None)
        context = {'thursday_form': form_one}
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return: a redirect to the homepage (ListView of Thursday dates)
        """
        if request.method == 'POST':
            form = ThursdayForm(request.POST, request.FILES)
            if form.is_valid():
                company_attempting_to_reserve = form.save(commit=False)
                company_attempting_to_reserve.is_registered = False  # keep the user disabled until confirmation
                company_attempting_to_reserve.pmm_date = form.cleaned_data['pmm_date']
                company_attempting_to_reserve.save()

                scheduled_date = company_attempting_to_reserve.pmm_date
                scheduled_date.assigned_company = None
                scheduled_date.save()

                if request.user.is_superuser:  # ignore tokenizing confirmation email
                    company_attempting_to_reserve.is_registered = True
                    company_attempting_to_reserve.pmm_date = scheduled_date
                    company_attempting_to_reserve.save()

                    scheduled_date.assigned_company = company_attempting_to_reserve
                    scheduled_date.save()

                    current_site = get_current_site(request)
                    mail_subject = 'Approved Pizza My Mind Visit'
                    message = render_to_string('thursdays/approved_visit.html', {
                        'user': company_attempting_to_reserve.name,
                        'domain': current_site.domain,
                        'date': scheduled_date
                    })
                    if company_attempting_to_reserve.email_two:
                        email = EmailMessage(mail_subject, message,
                                             to=[company_attempting_to_reserve.email_one,
                                                 company_attempting_to_reserve.email_two])
                        email.send()
                    else:
                        email = EmailMessage(mail_subject, message, to=[company_attempting_to_reserve.email_one])
                        email.send()
                else:
                    current_site = get_current_site(request)
                    mail_subject = 'Pizza My Mind Registration Confirmation'
                    message = render_to_string('thursdays/confirmation_email.html', {
                        'user': company_attempting_to_reserve,
                        'thursday': scheduled_date,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(company_attempting_to_reserve.pk)).decode(),
                        'token': account_activation_token.make_token(company_attempting_to_reserve),
                        'scheduled_pk': scheduled_date.pk
                    })
                    to_email = os.environ["ADMIN_EMAIL"]
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                    messages.success(request, 'Registration Is Awaiting Confirmation')
                return redirect('/')
        else:
            form = ThursdayForm()
        return render(request, self.template_name, {'thursday_form': form})


class PreviousPizzaMyMindListView(ListView):
    model = Thursday
    template_name = 'thursdays/all_thursdays.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        """
        :param args:
        :param object_list:
        :param kwargs:
        :return: a context dictionary to be accessed in the template
        """
        context = super(PreviousPizzaMyMindListView, self).get_context_data(*args, **kwargs)
        context['all_thursdays'] = Thursday.objects.filter(is_currently_available=False)
        return context


class AboutView(View):
    template_name = 'thursdays/about.html'

    def get(self, request):
        return render(request, self.template_name, {})


class ContactUsView(View):
    template_name = 'thursdays/contact_us.html'

    def get(self, request):
        return render(request, self.template_name, {})


class ArchiveView(LoginRequiredMixin, View):
    template_name = '/'  # homepage

    def post(self, request):
        """
        archive method that sends all of the current PMM dates from the year into the 'archived folder'
        :param request: POST method from HTML
        :return: a redirect to the homepage
        """
        if request.method == 'POST':
            thursday_list = Thursday.objects.filter(is_currently_available=True)
            for thursday in thursday_list.iterator():
                thursday.is_currently_available = False
                thursday.save()
        return redirect(self.template_name)


# ##############################################END CLASS BASED VIEWS##################################################

# ##############################################FUNCTION BASED VIEWS###################################################
def activate(request, uidb64, token, pk):
    """
    Try to convert the uid to a readable text and then query the company that was denied. If it was found, which it
    should be, grab their PMM date from the passed pk, register the company, save the new object, pair the PMM date and
    company together, save the new information. It then sends an email to the company stating their visit was approved.
    It then queries the database for any other companies who attempted to register for the date and sets their
    registration status to False. Redirect to the homepage.
    :param request: POST request from HTML
    :param uidb64: uidb64 encoded string sent from the template representing the model object
    :param token: secure token associated to the company
    :param pk: primary key of the PMM date
    :return: redirection to the homepage
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        approved_company = Company.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Company.DoesNotExist):
        approved_company = None
    if approved_company is not None and account_activation_token.check_token(approved_company, token):
        pmm_date = Thursday.objects.get(pk=pk)
        approved_company.is_registered = True
        approved_company.save()
        pmm_date.assigned_company = approved_company
        pmm_date.scheduled = True
        pmm_date.save()
        approved_company.pmm_date = pmm_date
        approved_company.save()

        current_site = get_current_site(request)

        mail_subject = 'Approved Pizza My Mind Visit'
        message = render_to_string('thursdays/approved_visit.html', {
            'user': approved_company.name,
            'domain': current_site.domain,
            'date': pmm_date
        })
        if approved_company.email_two:
            email = EmailMessage(mail_subject, message, to=[approved_company.email_one, approved_company.email_two])
            email.send()
        else:
            email_one = approved_company.email_one
            email = EmailMessage(mail_subject, message, to=[email_one])
            email.send()

        automatic_denial_list = Company.objects.filter(pmm_date=pmm_date).exclude(id=approved_company.id)
        for denied_company in automatic_denial_list.iterator():
            #     mail_subject = 'Denied Pizza My Mind Visit'
            #     message = render_to_string('thursdays/denied_visit.html', {
            #         'user': denied_company.name,
            #         'domain': current_site.domain,
            #     })
            #     if denied_company.email_two:
            #       email = EmailMessage(mail_subject, message, to=[denied_company.email_one, denied_company.email_two])
            #         email.send()
            #     else:
            #         email = EmailMessage(mail_subject, message, to=[denied_company.email_one])
            #         email.send()
            denied_company.pmm_date = None
            denied_company.save()
        return redirect('/')
    else:
        return HttpResponse('Activation link is invalid!')


def deactivate(request, uidb64, token):
    """
    Try to convert the uid to a readable text and then query the company that was denied.
    If it was found, which is should be, change its registration status to False, delete its pmm_date, and then save the
    newly updated object. Then send an email to the deneid company stating their visit was denied. Redirect to the home-
    page.
    :param request: POST request from HTML
    :param uidb64: uidb64 encoded string sent from the template representing the model object
    :param token: secure token associated to the company
    :return: redirection to the homepage
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        denied_company = Company.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Company.DoesNotExist):
        denied_company = None
    if denied_company is not None and account_activation_token.check_token(denied_company, token):
        denied_company.is_registered = False
        denied_company.pmm_date = None
        denied_company.save()

        current_site = get_current_site(request)
        mail_subject = 'Denied Pizza My Mind Visit'
        message = render_to_string('thursdays/denied_visit.html', {
            'user': denied_company.name,
            'domain': current_site.domain
        })
        if denied_company.email_two:
            email = EmailMessage(mail_subject, message, to=[denied_company.email_one, denied_company.email_two])
            email.send()
        else:
            email = EmailMessage(mail_subject, message, to=[denied_company.email_one])
            email.send()

        return redirect('/')
    else:
        return HttpResponse('Deactivation link is invalid!')


def bound_form(request, pk):
    """
    Render the sign up form and auto-select the PMM date that was selected
    :param request: GET request sent from HTML
    :param pk: primary key associated to the PMM date
    :return: rendering of the thursday_form.html page with the PMM date already selected
    """
    item = Thursday.objects.get(id=pk)
    form = ThursdayForm(initial={'pmm_date': item})
    return render(request, 'thursdays/thursday_form.html', {'thursday_form': form})


# Gets the extra dates from the front-end
def get_extra_dates(request):
    num_extra_days = request.POST.get('num_extra_days')
    days = []
    for i in range(int(num_extra_days)):
        days.append(request.POST.get('date_' + str(i)))

    return days


# Saves a Thursday object to the DB
def save_date(request, date_name, date):
    if date_name is not None:
        form = CreateThursdayForm()
        thursday = form.save(commit=False)
        thursday.date = date
        thursday.assigned_company = None
        thursday.scheduled = False
        thursday.save()


def create_thursdays(request):
    """
    If the form is filled out then get the dynamically created date fields and initialize a form with those,
    then if the form is valid iterate through the extra dates and save them to the DB.
    Finally, save the first date (the one produced by the form class)
    display a message to the user
    :param request:
    :return:
    """
    context = {}
    if request.method == 'POST':
        extra_dates = get_extra_dates(request)
        form = CreateThursdayForm(request.POST, extra=extra_dates)
        if form.is_valid():
            for (date_name, date) in form.extra_dates():
                save_date(request, date_name, date)
            form.save()
            context['message_success'] = "Dates have been successfully created!"
        else:
            context['message_error'] = "An error occurred while trying to create dates."
    else:
        context['form'] = CreateThursdayForm()
    return render(request, 'thursdays/create_thursdays.html', context)
