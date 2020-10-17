from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from .models import User
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.forms import ModelForm
from django import forms
from django.shortcuts import redirect, reverse
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from allauth.account.models import EmailAddress
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.generics import ListAPIView
from inventory.api_views import IsStafforAdmin, IsAdmin
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters
from inventory.api_views import StandardResultsSetPagination

##########SERIALIZER##########
class UserSerializer(ModelSerializer):
    edit_url = SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', '_type', 'edit_url']
    def get_edit_url(self, obj):
        return reverse('accounts:user-update', kwargs = {'pk': obj.id})
##########FORM##########
class UserCreationForm(ModelForm):
    password_2 = forms.CharField(required=True, label='Password Confirm')
    class Meta:
        model = User
        fields = ['first_name','last_name','_type','email','password','password_2', 'is_active']

# Create your views here.
class UserCreateView(LoginRequiredMixin, UserPassesTestMixin ,CreateView):
    form_class = UserCreationForm
    template_name = 'account/user_create.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = 'Create New User'
        return context
    
    def test_func(self):
        return self.request.user._type in ['ADMIN']
    def form_valid(self, form):
        if form.is_valid():
            password = make_password(form.cleaned_data['password'])
            form.instance.password = password
            if form.cleaned_data['password'] == form.cleaned_data['password_2']:
                user = form.save()
                EmailAddress.objects.create(user = user, email = form.cleaned_data['email'], verified=True, primary=True)
                messages.success(self.request, f"User successfully Created.")
            else:
                messages.warning(self.request, f"Error: Please Check Your Form.")
        return redirect('/')

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin ,UpdateView):
    form_class = UserCreationForm
    queryset = User.objects.all()
    template_name = 'account/user_create.html'
    def test_func(self):
        return self.request.user._type in ['ADMIN']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = 'Update User'
        return context
    def form_valid(self, form):
        if form.is_valid():
            password = make_password(form.cleaned_data['password'])
            form.instance.password = password
            if form.cleaned_data['password'] == form.cleaned_data['password_2']:
                user = form.save()
                email = EmailAddress.objects.get(user = user)
                email.email = form.cleaned_data['email']
                email.save()
                messages.success(self.request, f"User Updated Successfully.")
            else:
                messages.warning(self.request, f"Error: Please Check Your Form.")
        return redirect('/')


##########API VIEW##########
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    pagination_class = StandardResultsSetPagination
    filterset_fields = {'_type':['exact']}
    search_fields = ['first_name','last_name', 'email']

def userlistview(request):
    return render(request, 'account/user-list.html')