from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

from contacts.models import Contact

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    return redirect('index')

def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if __validatePassword(request, password, password2) and __validateUsername(request, username) and __validateEmail(request, email):
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            # Login after register
            # auth.login(request, user)
            # messages.success(request, 'You are now logged in')
            # return redirect('index')

            user.save()
            messages.success(request, 'You are now registered and can log in')
            return redirect('login')
        else:
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }

    return render(request, 'accounts/dashboard.html', context)


# Validations
def __validatePassword(request, password1, password2):
    if password1 == password2:
        return True
    else:
        messages.error(request, 'Passwords do not match')
        return False

def __validateUsername(request, username):
    if User.objects.filter(username=username).exists():
        messages.error(request, 'That username is taken')
        return False
    else:
        return True

def __validateEmail(request, email):
    if User.objects.filter(email=email).exists():
        messages.error(request, 'That email is taken')
        return False
    else:
        return True