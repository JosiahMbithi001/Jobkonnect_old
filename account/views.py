from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Employer, Employee, User
import random 
from .forms import RegisterForm, CertificateForm, EmployeeForm, EmployerForm

# Create your views here.
def base(request):
    """
    This is the landing autentication Page 
    """
    return render(request, "account/authenticate.html")

def employer_sign_up(request):
    """Employers View for the SignUp Form"""
  
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        phonenumber = request.POST['phonenumber']
        email = request.POST['email']
        password = request.POST['password']
        location = request.POST['location']
        user_name = f'{firstname}{random.randint(1, 9999)}'

        new_user = User(
            username=user_name,
            password=password,
            role='Employer'
        )
        new_user.save()

        new_employer = Employer(
            userid=new_user,
            firstname=firstname,
            lastname=lastname,
            phonenumber=phonenumber,
            email=email,
            password=password,
            location=location
        )
        new_employer.save()
        return redirect("/")
    else:
        return render(request, 'account/employer.html')


def employee_sign_up(request):
    """Employee signup View"""

    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        phonenumber = request.POST['phonenumber']
        email = request.POST['email']
        password = request.POST['password']
        location = request.POST['location']
        profession = request.POST['profession']
        status = 'active'
        user_name = f'{firstname}{random.randint(1, 9999)}'

        new_user = User(
            username=user_name,
            password=password,
            role="Employee",
            email=email,
            is_active=True,
            is_staff=True,
            is_superuser=False,
            )
        new_user.save()

        new_employee = Employee(
            user=new_user,
            firstname=firstname,
            lastname=lastname,
            phonenumber=phonenumber,
            email=email,
            password=password,
            location=location,
            profession=profession,
            status=status
        )
        new_employee.save()
        return redirect('/')
    else:
        return render(request, 'account/employee.html')
 
        
# def user_login(request):
#     """
#     This Function Logins in an authenticated User
#     """
#     username = request.POST["username"]
#     password = request.POST["password"]
#     username = "joe"
#     password = "123456"
#     user= User.objects.get(username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return redirect("/")
#     else:
#         return render(request, 'account/login.html')
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, ("You were successfully Logged In"))
            return redirect("/employer/post_job")
        else:
            messages.success(request, ("Error Logging In - Please Try Again..."))
            return redirect("/account/login")
       # return redirect("/")
    else:
        return render(request, 'account/login.html')

def user_logout(request):
    """
    Function used to logout user
    """
    logout(request)
    messages.success(request, ("You were successfully Logged Out"))
    return redirect ("login/")


def upload_certificate(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.save()
            return redirect('certificate_list')
    else:
        form = CertificateForm()
    return render(request, 'upload_certificate.html', {'form': form})