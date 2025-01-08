# from django.shortcuts import render,get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import CreateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from . models import Transaction
from . forms import DepositForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from . constants import DEPOSIT
from django.db.models import Sum
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()
@method_decorator(login_required, name='dispatch')
class TransactionCreateViewMixin(CreateView):
    template_name = 'transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('home')


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'account': self.request.user.account})
        return kwargs
    

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })
        return context

class DepositMoneyView(TransactionCreateViewMixin):
    form_class = DepositForm
    title = 'Deposit'


    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial 
    
    def form_valid(self,form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(update_fields=['balance'])
        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
        send_transaction_email(self.request.user, amount, "Deposite Message", "deposit_email.html")
        return super().form_valid(form)
    


@method_decorator(login_required, name='dispatch')
class TransactionReportView(ListView):
    template_name = 'transaction_report.html'
    model = Transaction
    balance = 0 # filter korar pore ba age amar total balance ke show korbe
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
            self.balance = Transaction.objects.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance
       
        return queryset.distinct() # unique queryset hote hobe
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })

        return context
