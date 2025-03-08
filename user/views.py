from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count
import json
from django.contrib import messages

# Home Page
def home(request):
    return render(request, "home.html")

# User Registration
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

# Admin Login
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Hardcoded admin credentials
        if username == "ADMIN" and password == "!@#$":
            request.session["admin_logged_in"] = True  
            return redirect("admin_dashboard")  
        else:
            return render(request, "admin_login.html", {"error": "Invalid credentials"})

    return render(request, "admin_login.html")

# Admin Dashboard
def admin_dashboard(request):
    if not request.session.get("admin_logged_in"):
        return redirect("admin_login")  

    query = request.GET.get("q", "")
    users = CustomUser.objects.all()
    if query:
        users = users.filter(email__icontains=query)

    # Count users per organization
    org_data = (
        CustomUser.objects
        .values("organisation")
        .annotate(user_count=Count("id"))
        .order_by("-user_count")
    )

    # Convert data to JSON-safe format
    org_labels = json.dumps([entry["organisation"] for entry in org_data])  
    org_counts = json.dumps([entry["user_count"] for entry in org_data])

    return render(request, "admin_dashboard.html", {
        "users": users,
        "query": query,
        "org_labels": org_labels,  
        "org_counts": org_counts   
    })

# Admin Logout
def admin_logout(request):
    request.session.flush()  
    return redirect("home")  

# Login View for Users
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_dashboard')  
            else:
                messages.error(request, "Invalid username or password.")  
        else:
            messages.error(request, "Invalid username or password.")  

    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

# User Dashboard
@login_required
def user_dashboard(request):
    return render(request, "user_dashboard.html", {"user": request.user})

@login_required
def update_profile(request):
    user = request.user  
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')  
    else:
        form = CustomUserUpdateForm(instance=user)  
    return render(request, 'update_profile.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)  # Logout user
    return redirect('home')  # Redirect to Home Page ✅
