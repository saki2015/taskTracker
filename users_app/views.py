from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomRegisterForm


def register(request):
    if request.method == "POST":
        # register_form = UserCreationForm(request.POST)
        register_form = CustomRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, ("New user account created!"))
            return redirect("register")
        else:
            # Form is invalid, display error messages
            for field, errors in register_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect(
                "register"
            )  # Redirect back to the registration page with error messages
    else:
        # register_form = UserCreationForm()
        register_form = CustomRegisterForm()
        return render(request, "register.html", {"register_form": register_form})
    return HttpResponse("Invalid form data")
