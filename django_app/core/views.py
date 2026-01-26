# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages

from models.user_model import UserModel
from models.progress_model import ProgressModel


def home(request):
    """Simple home page."""
    return render(request, "core/home.html")


def login_view(request):
    """Login page with form."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = UserModel.authenticate(username, password)

        if user:
            request.session["user_id"] = user["username"]
            request.session["username"] = user["username"]
            messages.success(request, f"Logged in as {username}")
            return redirect("progress_view")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")

    return render(request, "core/login.html")


def progress_view(request):
    """Show the logged-in user's progress."""
    user_id = request.session.get("user_id")
    username = request.session.get("username")

    if not user_id:
        messages.error(request, "Please log in first.")
        return redirect("login")

    progress = ProgressModel.load_progress(user_id)
    if not progress:
        progress = ProgressModel.create_progress(user_id)

    context = {
        "username": username,
        "current_mission": progress.get("current_mission", 1),
        "missions_completed": progress.get("missions_completed", []),
    }

    print("SESSION USER_ID:", user_id)
    print("PROGRESS:", progress)

    return render(request, "core/progress.html", context)


def logout_view(request):
    """Log out the current user."""
    request.session.flush()   # important since you are NOT using Django auth users
    logout(request)
    return redirect("home")
