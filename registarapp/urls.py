from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", auth_views.LoginView.as_view(template_name='registarapp/login.html'), name="login"),
    path("forgot_password", views.forgotPasswordView, name="forgot_password"),
    path("sign_up", views.signUpView, name="sign_up"),
    path('api/register', views.RegisterUserView.as_view(), name="register"),
    path("dashboard", views.dashboardView, name="dashboard"),
    path("registration_student", views.registrationView, name="registration_student"),
    path("bill_payment", views.billPaymentView, name="bill_payment"),
    path('bill_student/<int:student_id>', views.bill_student_view, name="bill_student"),
    path("create_bill/<int:student_id>", views.create_bill_view, name="create_bill"),
    path('create_bill_common', views.create_bill_common_view, name='create_bill_common'),
    path('create-student', views.create_student_view, name='create_student'),
    path('edit_student/<int:student_id>', views.edit_student_view, name='edit_student')
    
]                                                                                                                                                                                                                       