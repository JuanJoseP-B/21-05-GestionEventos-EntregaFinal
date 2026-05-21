from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from django.views import View

from .forms import LoginForm, ProfileUpdateForm, RegisterForm


class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = LoginForm(request)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'Has cerrado sesión correctamente.')
        return redirect('users:login')


class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido a Antigravity, {user.first_name or user.username}!')
            return redirect('home')
        return render(request, self.template_name, {'form': form})


class ProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        profile_form = ProfileUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {
            'profile_form': profile_form,
            'password_form': password_form,
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')

        if 'update_profile' in request.POST:
            profile_form = ProfileUpdateForm(request.POST, instance=request.user)
            password_form = PasswordChangeForm(request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Perfil actualizado correctamente.')
                return redirect('users:profile')
        elif 'change_password' in request.POST:
            profile_form = ProfileUpdateForm(instance=request.user)
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Contraseña actualizada correctamente.')
                return redirect('users:profile')
        else:
            profile_form = ProfileUpdateForm(instance=request.user)
            password_form = PasswordChangeForm(request.user)

        return render(request, self.template_name, {
            'profile_form': profile_form,
            'password_form': password_form,
        })
