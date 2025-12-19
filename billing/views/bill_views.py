from django.views.generic import CreateView, DetailView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from billing.models import Bill
from billing.forms import BillForm

class BillCreateView(CreateView):
    model = Bill
    form_class = BillForm
    template_name = 'billing/bill_form.html'
    success_url = reverse_lazy('bill-list')

class BillDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Bill
    template_name = 'billing/bill_detail.html'
    context_object_name = 'bill'

    def test_func(self):
        bill = self.get_object()
        user = self.request.user
        if user.is_staff:
            return True
        return hasattr(user, 'patient') and bill.patient == user.patient

class BillListView(ListView):
    model = Bill
    template_name = 'billing/bill_list.html'
    context_object_name = 'bills'
