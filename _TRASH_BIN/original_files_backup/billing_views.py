from django.views.generic import CreateView, DetailView, ListView
from django.urls import reverse_lazy
from .models import Bill
from .forms import BillForm

class BillCreateView(CreateView):
    model = Bill
    form_class = BillForm
    template_name = 'billing/bill_form.html'
    success_url = reverse_lazy('bill-list')

class BillDetailView(DetailView):
    model = Bill
    template_name = 'billing/bill_detail.html'
    context_object_name = 'bill'

class BillListView(ListView):
    model = Bill
    template_name = 'billing/bill_list.html'
    context_object_name = 'bills'
