from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

from .forms import LoginForm, UserRegisterForm, UserEditForm, ProfileEditForm, CustomUserRegistrationForm
from .models import Profile


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('<h2>Tizimga kirildi')
                else:
                    return HttpResponse('<h2>Bu foydalanuvhi active holatda emas')
            else:
                return HttpResponse('<h2>Username yoki parol xato')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            login(request, new_user)
            context = {
                'new_user': new_user
            }
            return redirect('user_profile')
    else:
        user_form = UserRegisterForm()
    return render(request, 'profile/register.html', {"form": user_form})


class SignUpView(CreateView):
    form_class = CustomUserRegistrationForm
    success_url = reverse_lazy('user_profile')
    template_name = 'profile/register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(
            user=self.object,
            date_of_birthday=form.cleaned_data.get('date_of_birthday'),
            user_profile_photo=form.cleaned_data.get('user_profile_photo'),
        )
        return response


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'profile/user_edit.html', context)


class ProfileEditView(LoginRequiredMixin, View):
    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'profile/user_edit.html', context)


@login_required
def user_profile(request):
    user = request.user
    if Profile.objects.filter(user=user).exists():
        context = {
            'user': user,
            'profile': Profile.objects.get(user=request.user)
        }
    else:
        context = {
            'user': user
        }
    return render(request, 'profile/user_profile.html', context)


def admin_list_display(request):
    return render(request, 'profile/admin_page.html', {"admins_list": User.objects.filter(is_superuser=True)})


def user_base(request):
    return render(request, 'base/user_base.html')


class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session['password_changed'] = True
        return response


class CustomPasswordChangeDoneView(PasswordChangeDoneView):

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('password_changed', False):
            raise Http404("Parol hali o'zgartirilmagan.")

        del request.session['password_changed']
        return super().dispatch(request, *args, **kwargs)
