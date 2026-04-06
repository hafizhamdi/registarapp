from django.shortcuts import render, redirect, get_object_or_404
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
from datetime import datetime
from django.utils import timezone
from django.http import QueryDict
from django.forms.models import model_to_dict
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
    students = Student.objects.all()
    fulltime_count = Student.objects.filter(student_type='Full-time').count()
    parttime_count = Student.objects.filter(student_type='Part-time').count()

    context = {
        'total_students': len(students),
        'total_fulltime': fulltime_count,
        'total_parttime': parttime_count,
        'page_title': 'Dashboard Overview',
        
    }
    # Django looks in your app's 'templates/' folder automatically
    return render(request, 'registarapp/dashboard/dashboard.html', context)

def registrationView(request):
    # This data can later come from your Database (Models)

    # 1. Get all students (ordered for consistent pagination)
    student_list = Student.objects.all().order_by('-created_date')

    # 2. Apply search filter if search bar is used
    query = request.GET.get('search')
    if query:
        student_list = student_list.filter(full_name__icontains=query) | \
                       student_list.filter(id_number__icontains=query)

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

def bill_student_view(request, student_id):
    # This data can later come from your Database (Models)

    student = get_object_or_404(Student, id=student_id)
    
    bill_list = Bill.objects.filter(student=student).order_by('payment_date')
   
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
    

def billPaymentView(request):
    # This data can later come from your Database (Models)
    bill_list = Bill.objects.select_related('student').order_by('-id')

    # 2. Apply search filter if search bar is used
    query = request.GET.get('search')
    if query:
        bill_list = bill_list.filter(designated_month__icontains=query) | \
                       bill_list.filter(bill_type__icontains=query) | \
                       bill_list.filter(description__icontains=query) | \
                       bill_list.filter(student__full_name__icontains=query)

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
        'bills': page_obj,  # Passing page_obj as 'students' for the loop
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
        dob = request.POST.get('dob')
        id_type = request.POST.get('id_type')
        student_type = request.POST.get('student_type')

        formatted_date = datetime.strptime(dob, '%Y-%m-%d').date()

        current_time = timezone.now()

        # Save to database
        Student.objects.create(
            full_name=full_name,
            id_number=nric,
            id_type=id_type,
            gender=gender,
            age=age,
            dob=formatted_date,
            student_type=student_type,
            created_date=current_time,
        )

        # Add the success message
        messages.success(request, f"Student {request.POST.get('full_name')} registered successfully!")
        
        return redirect('registration_student') # Reload the list

def edit_student_view(request, student_id):
    # Fetch the existing student or return 404
    student = get_object_or_404(Student, id=student_id)


    if request.method == "POST":
        # Since Django doesn't have request.PATCH, we parse the body
        # This works for AJAX calls sending URL-encoded data or JSON
        data = QueryDict(request.body)
        
        # 1. Extraction (Basic Info)
        full_name = data.get('full_name')
        nric = data.get('nric')
        gender = data.get('gender')
        age = data.get('age')
        dob = data.get('dob')
        id_type = data.get('id_type')
        student_type = data.get('student_type')

        # 2. Extraction (Detail Info)
        address_line1 = data.get('address_line1')
        address_line2 = data.get('address_line2')
        postcode = data.get('postcode')
        city = data.get('city')
        state = data.get('state')
        country = data.get('country')
        previous_school = data.get('previous_school')
        
        # 3. Extraction (Family Info)
        total_siblings = data.get('total_siblings')
        number_of_children = data.get('number_of_children')
        parent_name = data.get('parent_name')
        parent_contact = data.get('parent_contact')
        
        # 4. Save to database
        # We use .filter().update() for efficiency, or update attributes and .save()
        Student.objects.filter(id=student_id).update(
            full_name=full_name,
            # id_number=nric,
            id_type=id_type,
            gender=gender,
            age=age,
            dob=dob, # Ensure this is in YYYY-MM-DD format
            student_type=student_type,
            address_line1=address_line1,
            address_line2=address_line2,
            postcode=postcode,
            city=city,
            state=state,
            country=country,
            previous_school=previous_school,
            total_siblings=total_siblings,
            number_of_children=number_of_children,
            parent_name=parent_name,
            parent_contact=parent_contact
        )

        # 5. Success Feedback
        messages.success(request, f"Student {full_name} updated successfully!")
        
        student = get_object_or_404(Student, id=student_id)
        # Note: Redirects often convert PATCH to GET. 
        # For AJAX, you might prefer returning a                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          JsonResponse.
        return render(request,'registarapp/student/edit_student.html',{'student': model_to_dict(student)} )

    return render(request, 'registarapp/student/edit_student.html', {'student': model_to_dict(student)})

def create_bill_view(request, student_id):
    # Fetch the existing student or return 404
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        # Capture form data
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        month = request.POST.get('month')
        year = request.POST.get('year')
        payment_status = request.POST.get('payment_status')
        current_time = timezone.now()
        # created_date = current_time.strftime('%Y-%m-%d %H:%M:%S')
        payment_date = None
        if payment_status == "Paid":
            payment_date = current_time

        # Save to database
        Bill.objects.create(
            student=student,
            bill_type=bill_type,
            bill_amount=amount,
            designated_month=month,
            designated_year=year,
            payment_method=payment_method,
            payment_status=payment_status,
            payment_date=payment_date,
        )

        # Add the success message
        messages.success(request, f"Student {student.full_name}'s bill added successfully!")
        
        context = {}
        
    return render(request, 'registarapp/bill_payment/bill_payment.html', context)


def create_bill_common_view(request):
    # Fetch the existing student or return 404
    # student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        # Capture form data
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        name = request.POST.get('name')
        bill_type = request.POST.get('bill_type')
        payment_method = request.POST.get('payment_method')
        month = request.POST.get('month')
        year = request.POST.get('year')
        payment_status = request.POST.get('payment_status')
        current_time = timezone.now()
        # created_date = current_time.strftime('%Y-%m-%d %H:%M:%S')
        payment_date = None
        if payment_status == "Paid":
            payment_date = current_time

        student_list = Student.objects.all().order_by('-created_date')

        if name:
            # Filter by the provided name
            student_list = Student.objects.filter(full_name__icontains=name)
        else:
            # Explicitly set to an empty QuerySet if name is None or ""
            student_list = Student.objects.none()
            
        # Save to database
        new_bill = Bill.objects.create(
            student=student_list.first(),
            description=description,
            bill_type=bill_type,
            bill_amount=amount,
            designated_month=month,
            designated_year=year,
            payment_method=payment_method,
            payment_status=payment_status,
            payment_date=payment_date
        )

        # Add the success message
        messages.success(request, f"New Bill {new_bill.id} created")
 
    return redirect('bill_payment');
        
    # return render(request, 'registarapp/bill_payment/bill_payment.html', context)

class RegisterUserView(generics.CreateAPIView):
    User = get_user_model()
    users = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

def receipt_view(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    context = {
        "logo_url": "/static/img/logo.png",
        "company_name": "My Company Sdn Bhd",
        "company_address": "Kuala Lumpur, Malaysia",
        "customer_name": "John Doe",
        "customer_email": "john@email.com",
        "customer_phone": "0123456789",
        "receipt_no": "RCPT-0001",
        "date": "2026-03-29",
        "time": "14:30",
        "payment_method": "Online Transfer",
        "items": [
            {"name": "Course A", "description": "Django Training", "quantity": 1, "price": 100, "total": 100},
            {"name": "Course B", "description": "API Training", "quantity": 2, "price": 50, "total": 100},
        ],
        "grand_total": 200,
        "description": "Thank you for your payment."
    }
    return redirect('receipt', context)

