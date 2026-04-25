from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import LawyerRegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect("contracts:dashboard")

    if request.method == "POST":
        form = LawyerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse_lazy("contracts:dashboard"))
    else:
        form = LawyerRegisterForm()

    return render(request, "accounts/register.html", {"form": form})
