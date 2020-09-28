from django.shortcuts import render, redirect
from . models import Profile
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, UserDetailUpdateForm
from django.contrib import messages


# Create your views here.

@login_required
def profile(request):
    if request.method=="POST":
        u_form = UserDetailUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account Updated Successfully!')
            return redirect ('profile')
    else:
        u_form = UserDetailUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context={
        'u_form':u_form,
        'p_form':p_form,
        'title':f"{ request.user.first_name }'s Profile",
    }
    return render(request, 'Userprofile/profile.html', context)
