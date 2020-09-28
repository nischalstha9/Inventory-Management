from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def view_404(request, *args, **kwargs):
    return render(request,'partial/404.html',{'title':'Oops! Page Not Found!!'}, status=404)