from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView
from .forms import ItemCreationForm
from .models import Item
from django.http import JsonResponse
from .models import Category
from rest_framework.generics import ListAPIView
from .serializers import CategoryChartSerializer

# Create your views here.
def index(request):
    return render(request, "inventory/item_list.html")

class ItemCreationVIew(CreateView):
    form_class = ItemCreationForm
    template_name = 'inventory/item_creation.html'
    success_url = "../"

class ItemListView(ListView):
    model = Item
    template_name = "inventory/item_list.html"
    context_object_name = 'items'
    paginate_by = 50

class ItemUpdateVIew(UpdateView):
    form_class = ItemCreationForm
    template_name = 'inventory/item_creation.html'
    success_url = "../../"
    queryset = Item.objects.all()

class CategoryNcount(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryChartSerializer
    