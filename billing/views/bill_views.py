from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
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

class BillStatusUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, pk):
        bill = get_object_or_404(Bill, pk=pk)
        status = request.POST.get('status')
        if status in ['PAID', 'PARTIAL', 'PENDING']:
            bill.payment_status = status
            bill.save()
            messages.success(request, f"Bill #{bill.id} status updated to {status}.")
        return redirect('bill-detail', pk=bill.pk)
