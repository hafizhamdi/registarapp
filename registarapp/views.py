from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm, ForgotPasswodForm
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Student, Bill
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    return render(request, "registarapp/index.html", {})

def main(request):
    return render(request, "registarapp/main.html", {})

def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'], 
                                password=form.cleaned_data['password'])
            if user:
                # login(request, user)
                return redirect('index')
            else:
                # Add the error message here
                messages.error(request, "Invalid email or password. Please try again.")
        else:
             messages.error(request, "Invalid form submission.")
    else:
        form = LoginForm()
    return render(request, 'registarapp/login.html', {'form': form})

def forgotPasswordView(request):
    if request.method == 'POST':
        form = ForgotPasswodForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['username'])
            if user:
                # login(request, user)
                return redirect('index')
    else:
        form = ForgotPasswodForm()
    return render(request, 'registarapp/forgot_password.html', {'form': form})

def signUpView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = UserSerializer.create(form.cleaned_data)
                                
            if user:
                # login(request, user)
                print("User created")
                return redirect('index')
            else:
                print("Something wrong, user not created")
    else:
        form = SignUpForm()
    return render(request, 'registarapp/sign_up.html', {'form': form})

def dashboardView(request):
    # This data can later come from your Database (Models)
    context = {
        'total_students': 1240,
        'page_title': 'Dashboard Overview',
    }
    # Django looks in your app's 'templates/' folder automatically
    return render(request, 'registarapp/dashboard/dashboard.html', context)

def registrationView(request):
    # This data can later come from your Database (Models)

    # 1. Get all students (ordered for consistent pagination)
    student_list = Student.objects.all().order_by('full_name')

    # 2. Apply search filter if search bar is used
    query = request.GET.get('search')
    if query:
        student_list = student_list.filter(full_name__icontains=query) | \
                       student_list.filter(nric__icontains=query)

    # 3. Initialize Paginator (e.g., 10 students per page)
    paginator = Paginator(student_list, 10) 
    
    # 4. Get current page number from request
    page_number = request.GET.get('page')
    
    # 5. Get the specific page object
    # get_page() handles invalid or out-of-range page numbers automatically
    page_obj = paginator.get_page(page_number)
    # context = {
    #     'students': [
    #         {
    #             'full_name' : 'ABU KASIM',
    #             'nric': '900129016139',
    #             'age': 12,
    #             'gender': 'M',
    #             'type': 'Full time'
    #         },
    #         {
    #             'full_name' : 'MALIK MARWAN',
    #             'nric': '900129016139',
    #             'age': 12,
    #             'gender': 'M',
    #             'type': 'Full time'
    #         }
    #     ],
    #     'page_title': 'Student Registration',
    # }

    context = {
        'page_obj': page_obj,
        'students': page_obj,  # Passing page_obj as 'students' for the loop
    }
    # Django looks in your app's 'templates/' folder automatically
    return render(request, 'registarapp/student/registration_student.html', context)

def billPaymentView(request):
    # This data can later come from your Database (Models)

    # 1. Get all students (ordered for consistent pagination)
    bill_list = Bill.objects.all().order_by('payment_date')

    # 2. Apply search filter if search bar is used
    query = request.GET.get('search')
    if query:
        bill_list = bill_list.filter(full_name__icontains=query) | \
                       bill_list.filter(nric__icontains=query)

    # 3. Initialize Paginator (e.g., 10 students per page)
    paginator = Paginator(bill_list, 10) 
    
    # 4. Get current page number from request
    page_number = request.GET.get('page')
    
    # 5. Get the specific page object
    # get_page() handles invalid or out-of-range page numbers automatically
    page_obj = paginator.get_page(page_number)

    # context = {
    #     'students': [
    #         {
    #             'full_name' : 'ABU KASIM',
    #             'nric': '900129016139',
    #             'amount': 200.0,
    #             'description': 'YURAN TAHUNAN',
    #             'payment_at': '2025-02-18 02:11 AM',
    #             'payment_type': 'Cash'
    #         },
    #         {
    #             'full_name' : 'SALEH MAT YOM',
    #             'nric': '900129016139',
    #             'amount': 200.0,
    #             'description': 'YURAN TAHUNAN',
    #             'payment_at': '2025-02-18 02:11 AM',
    #             'payment_type': 'FPX'
    #         },
    #     ],
    #     'page_title': 'Student Registration',
    # }

    context = {
        'page_obj': page_obj,
        'students': page_obj,  # Passing page_obj as 'students' for the loop
    }
    # Django looks in your app's 'templates/' folder automatically
    return render(request, 'registarapp/bill_payment/bill_payment.html', context)

def create_student_view(request):
    if request.method == "POST":
        # Capture form data
        full_name = request.POST.get('full_name')
        nric = request.POST.get('nric')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        student_type = request.POST.get('student_type')

        # Save to database
        Student.objects.create(
            full_name=full_name,
            id_number=nric,
            gender=gender,
            age=age,
            student_type=student_type
        )

        # Add the success message
        messages.success(request, f"Student {request.POST.get('full_name')} registered successfully!")
        
        return redirect('registration_student') # Reload the list

class RegisterUserView(generics.CreateAPIView):
    User = get_user_model()
    users = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

