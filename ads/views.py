import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Ad
from category.models import Category
from sky_pro_homework28 import settings
from user.models import User


def ads(request):
    return JsonResponse({"status": "ok"}, status=200)


class AdView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by('-price')

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        ad_s = []
        for ad in page_obj:
            user_data = User.objects.get(id=ad.author_id)
            ad_s.append(
                {
                    "id": ad.id,
                    "name": ad.name,
                    "author_id": ad.author_id,
                    "author": user_data.first_name,
                    "price": ad.price,
                    "description": ad.description,
                    "image": str(ad.image),
                    "category": ad.category_id,
                    "is_published": ad.is_published,
                }
            )

        response = {
            "items": ad_s,
            "total": paginator.count,
            "num_pages": paginator.num_pages
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ['name', 'price', 'description', 'is_published', 'author', 'category']

    def post(self, request, *args, **kwargs):
        response = []
        ad_data = json.loads(request.body)
        user_data = User.objects.get(id=ad_data['author_id'])
        cat_data = Category.objects.get(id=ad_data['category_id'])
        ad = Ad.objects.create(
            name=ad_data['name'],
            author=user_data,
            price=ad_data['price'],
            description=ad_data['description'],
            category=cat_data,
            is_published=ad_data['is_published']
        )

        response.append(
            {
                "id": ad.id,
                "name": ad.name,
                "author": ad.author_id,
                "price": ad.price,
                "description": ad.description,
                "image": str(ad.image),
                "category": ad.category_id,
                "is_published": ad.is_published,
            }
        )
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', 'price', 'description', 'is_published', 'image', 'author', 'category']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        response = []
        ad_data = json.loads(request.body)
        user_data = User.objects.get(id=ad_data['author_id'])
        cat_data = Category.objects.get(id=ad_data['category_id'])
        self.object.name = ad_data['name']
        self.object.author = user_data
        self.object.price = ad_data['price']
        self.object.description = ad_data['description']
        self.object.category = cat_data

        self.object.save()

        response.append(
            {
                "id": self.object.id,
                "name": self.object.name,
                "author": self.object.author_id,
                "price": self.object.price,
                "description": self.object.description,
                "image": str(self.object.image),
                "category": self.object.category_id,
                "is_published": self.object.is_published,
            }
        )
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=200)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        response = []
        ad = self.get_object()
        response.append(
            {
                "id": ad.id,
                "name": ad.name,
                "author": ad.author_id,
                "price": ad.price,
                "description": ad.description,
                "image": str(ad.image),
                "category": ad.category_id,
                "is_published": ad.is_published,
            }
        )
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ['name', 'image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES['image']
        self.object.save()
        user_data = User.objects.get(id=self.object.author_id)
        return JsonResponse(
            {
                "id": self.object.id,
                "name": self.object.name,
                "author_id": self.object.author_id,
                "author": user_data.first_name,
                "price": self.object.price,
                "description": self.object.description,
                "image": str(self.object.image),
                "category": self.object.category_id,
                "is_published": self.object.is_published,
            }
        )
