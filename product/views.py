from django.http import JsonResponse

from product.models import *
from django.views import generic

from django.shortcuts import render

from .forms import OrderForm
from .models import Category, Product
from django.core.paginator import Paginator

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    if category_slug:
        category = Category.objects.get(id=category_slug)
        products = products.filter(category=category)

    paginator = Paginator(products, 10)  # Display 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_data = [
            {
                'category': product.category.name,
                'name': product.name,
                'price': str(product.price),
                'image': product.image.url if product.image else ''
            } for product in page_obj
        ]
        return JsonResponse({'products': product_data})

    return render(request, 'index.html', {'page_obj': page_obj, 'categories': categories})


class CreateOrderView(LoginRequiredMixin, generic.CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'create_order.html'
    success_url = 'order_list'

    def get_initial(self):
        initial = super().get_initial()
        product_id = self.kwargs.get('product_id')
        self.product = get_object_or_404(Product, id=product_id)
        initial['product'] = self.product
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = self.product
        return super().form_valid(form)


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'

    def get_object(self, queryset=None):
        return get_object_or_404(Order, id=self.kwargs['order_id'], user=self.request.user)
