# core/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from models.user_model import UserModel
from models.progress_model import ProgressModel

def home(request):
    """Simple home page."""
    return render(request, "home.html")

def login_view(request):
    """Login page with form."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = UserModel.authenticate(username, password)
        if user:
            # Save user info in session
            request.session["user_id"] = user["id"]
            request.session["username"] = user["username"]
            messages.success(request, f"Logged in as {username}")
            return redirect("progress_view")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login_view")
    return render(request, "login.html")

def progress_view(request):
    """Show the logged-in user's progress."""
    user_id = request.session.get("user_id")
    username = request.session.get("username")

    if not user_id:
        messages.error(request, "Please log in first.")
        return redirect("login_view")

    # Load progress
    progress = ProgressModel.load_progress(user_id)
    if not progress:
        # Create progress if missing
        progress = ProgressModel.create_progress(user_id)

    context = {
        "username": username,
        "current_mission": progress.get("current_mission", 1),
        "missions_completed": progress.get("missions_completed", []),
    }

    return render(request, "progress.html", context)
