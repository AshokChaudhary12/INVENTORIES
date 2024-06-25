from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import FormView, TemplateView, UpdateView, DeleteView, ListView
from weasyprint import HTML
from Inventories import settings
from Inventories.settings import SHIPPING
from .forms import UserForm, InventoriesForm, LoginForm, InventoriesTypesForm, InventoryImageFormSet
from .models import Inventories, InventoryImage
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404


class SignUpView(SuccessMessageMixin, FormView):
    form_class = UserForm
    template_name = "Signup.html"
    success_url = reverse_lazy('login')
    success_message = "Signup successful. Please login."

    def form_valid(self, form):
        subject = 'welcome to inventories'
        username = form.cleaned_data.get('username')
        message = f'Hi {username} thank you for registering in Inventories.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [form.data.get('email')]
        send_mail(subject, message, email_from, recipient_list)
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class CustomLoginView(SuccessMessageMixin, LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    success_message = "Login successful."

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)


class Home(TemplateView):
    template_name = "base.html"


class InventoriesView(FormView):
    form_class = InventoriesForm
    template_name = "create_inventory.html"
    success_url = reverse_lazy('desbord')
    success_message = "Inventories created successful."

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = InventoryImageFormSet(self.request.POST, self.request.FILES,
                                                    queryset=InventoryImage.objects.none())
        else:
            data['formset'] = InventoryImageFormSet(queryset=InventoryImage.objects.none())
        return data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['type'] = self.request.user.inventories
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            images = form.data.getlist('images')
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            for image in images:
                if image:
                    inventory_image = InventoryImage.objects.create(image=image)
                    self.object.images.add(inventory_image)
                    self.object.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class GeneratePdfView(View):

    def get(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user_detail = get_object_or_404(Inventories, pk=pk)
        user_price = user_detail.unit_price
        user_quantity = user_detail.quantity
        object_total = user_price * user_quantity
        html_string = render_to_string('pdf_biling.html', {'data': user_detail, "total": object_total, "Shipping": SHIPPING, "totals": object_total + SHIPPING})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{user_detail.name}.pdf"'

        # Generate PDF
        HTML(string=html_string).write_pdf(response)

        return response


class DashboardView(ListView):
    model = Inventories
    template_name = 'deshboard.html'
    context_object_name = 'data'
    queryset = Inventories.objects.filter(is_delete=False)
    paginate_by = 5

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filter = InventoriesFilters(self.request.GET, queryset=queryset)
    #     return self.filter.qs

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['filter'] = self.filter
    #     return context

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        queryset = queryset.filter(user=user)
        search = self.request.GET.get('search')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        paginate_by = self.request.GET.get('paginate_by')
        print("search--", search)
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(inventry_type__name__icontains=search))

        if start_date and end_date:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(purchase_date__range=(start_date, end_date))
            if not self.get_ordering():
                queryset = queryset.order_by("purchase_date")

        # if paginate_by:
        #     queryset = queryset.filter(paginate_by=paginate_by)

        return queryset

    def get_paginate_by(self, queryset):
        if 'paginate_by' in self.request.GET:
            return self.request.GET['paginate_by']
        else:
            return self.paginate_by

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            context["start_date"] = start_date

        if end_date:
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            context["end_date"] = end_date

        context['paginate_by'] = self.get_paginate_by(self.queryset)
        return context


class AddItemViwe(FormView):
    form_class = InventoriesTypesForm
    template_name = "add_item.html"
    success_url = reverse_lazy('inventories')

    def form_valid(self, form):
        instanc = form.save(commit=False)
        instanc.user = self.request.user
        instanc.save()
        return super().form_valid(form)


class EditViwe(UpdateView):
    model = Inventories
    form_class = InventoriesForm

    template_name = 'update.html'
    success_url = reverse_lazy('desbord')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['type'] = self.request.user.inventories
        return kwargs


class InventoriesDeleteView(DeleteView):
    model = Inventories
    success_url = reverse_lazy('desbord')
    template_name = "delete.html"

    def form_valid(self, form):
        success_url = reverse_lazy('desbord')
        self.object.is_delete = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class Logout(LogoutView):
    pass


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = "password_reset_subject.txt"
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('login')


# class InventoryListView(ListView):
#     template_name ='deshboard.html'
#     model = Inventories
#     context_object_name = 'Inventories'
#     filterset_class = InventoriesFilters

