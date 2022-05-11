from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from accounts.forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from posts.models import Post


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in", 'warning')
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'you registered successfully', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {"form": form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in", 'warning')
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                return redirect('home:home')
            messages.error(request, 'invalid username or password', 'warning')
        return render(request, self.template_name, {"form": form})


class UserLogoutView(LoginRequiredMixin, View):
    # for default login url is '/accounts/login/' if you used another option you should write login_url like below:
    # login_url = '/accounts/login/'
    # or add to settings:
    # LOGIN_URL = '/accounts/login/'

    def get(self, request):
        logout(request)
        messages.success(request, 'You logged out successfully', 'success')
        return redirect("home:home")


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        posts = Post.objects.filter(user=user)
        return render(request, self.template_name, {"user": user, "posts": posts})


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')  # because of class variable evaluation we use lazy
    email_template_name = 'accounts/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:reset_password_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
