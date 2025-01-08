from django.shortcuts import render, redirect

from django.views.generic import FormView
from . forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login,update_session_auth_hash,logout
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from borrowingapp.models import Borrow
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.



class UserRegistrationView(FormView):
    form_class = UserRegistrationForm
    template_name = 'user_registration.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        print(user)
        login(self.request, user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("Form is invalid. Errors:", form.errors)
        return super().form_invalid(form)
  

    

class UserLoginView(LoginView):
    template_name = 'user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
    
@method_decorator(login_required, name='dispatch')
class UserLogoutView(LoginRequiredMixin,LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.get(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('home'))
    

@method_decorator(login_required, name='dispatch')
class UserAccountUpdateView(View):
    template_name = 'edit_profile.html'
    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})
    

@login_required(login_url='login')
def pass_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user,data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile Updated Successefully')
                update_session_auth_hash(request,form.user)
                return redirect('profile')

        else:
            form = PasswordChangeForm(user=request.user)
        return render(request, 'change_pass.html', {'form':form})
    else:
        return redirect('user_login')
    

@method_decorator(login_required, name='dispatch')
class BorrowedBooksView(ListView):
    model = Borrow
    template_name = 'profile.html' 
    context_object_name = 'borrowed_books'

    def get_queryset(self):
        return Borrow.objects.filter(user=self.request.user.account).select_related('book')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


