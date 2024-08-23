from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse

from django.views import View
from .models import User, Course, Category, Tag
from django.contrib.messages import warning, success
from .utils import send_verification_email
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CourseForm


# Create your views here.




class HomePageView(ListView):
    model = Course
   # queryset = Course.objects.filter(language='uz')
    template_name = 'index.html'
    context_object_name = 'courses'
    paginate_by = 3

    def get_queryset(self):
        request = self.request
        language = request.GET.get('language', 'ru')
        return Course.objects.filter(language=language)


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST.get('email')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        phone = request.POST.get('phone')

        if password != password_confirm:
            warning(request, 'Password confirmation is incorrect')
            return redirect(reverse('main:register'))
        if User.objects.filter(username=username).exists():
            warning(request, 'User already registered')
            return redirect(reverse('main:register'))
        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password,
                                        phone=phone, is_active=False)
        send_verification_email(user)
        login(request, user)
        success(request, 'User  registered')
        return redirect(reverse("main:kirish"))


class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html', {"success": True})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            warning(request, 'User does not exist')
            return redirect(reverse('main:kirish'))
        user = User.objects.get(username=username)
        if not user.check_password(password):
            warning(request, 'Password is incorrect')
            return redirect(reverse('main:kirish'))
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('main:home'))
        warning(request, 'Error')
        return redirect(reverse('main:kirish'))


class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_single.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data['tags'] = Tag.objects.all()
        return data


class AddCourseView(View):
    model = Course
    fields = ['title', "created_at", 'description', 'duration', 'price', 'category', 'tags', 'language', 'image']
    template_name = 'course_add.html'
    success_url = '/'

    def get(self, request):
        form = CourseForm()
        return render(request, self.template_name, {'form': form, "button": "Add"})

    def post(self, request):
        form = CourseForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            success(request, 'Course added')
            return redirect(reverse('main:home'))
        else:
            warning(request, 'Error')
            return render(request, self.template_name, {'form': form})


class CategoryCourseView(CreateView):
    model = Category
    fields = ['title']
    template_name = 'category.html'
    success_url = '/'


class UpdateCourseView(View):
    model = Course
    fields = ['title', "created_at", 'description', 'duration', 'price', 'category', 'tags', 'language', 'image']
    template_name = "course_add.html"
    success_url = '/'


    def get(self, request, pk):
        lang = request.COOKIES.get('language')
        if lang == 'en':
            button = 'Updates'

        if lang == 'ru':
            button = 'Обновить'

        if lang == 'uz':
            button = 'Yangilash'


        course = Course.objects.get(pk=pk)
        form = CourseForm(instance=course)

        response = render(request, self.template_name, {'form': form, "button": "Update"})
        response.set_cookie('course', pk)
        return response


    def post(self, request, pk):
        course = Course.objects.all(pk=pk)
        form = CourseForm(request.POST, request.FILES, instance=course)

        if form.is_valid():
            form.save()
            success(request, 'Course added')
            return redirect(reverse('main:home'))
        else:
            warning(request, 'Error')
            return render(request, self.template_name, {'form': form})



    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["button"] = "Update"
        return data