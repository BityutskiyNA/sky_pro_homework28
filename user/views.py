import json

from django.core.paginator import Paginator
from django.http import JsonResponse

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView, ListView

from ads.models import Ad
from sky_pro_homework28 import settings
from user.models import User, Location


class UserView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        user_list = []
        self.object_list = self.object_list.order_by('username')
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        for user in page_obj:
            user_list.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "age": user.age,
                    "location": user.location.name.split(','),
                    "total_ads": Ad.objects.all().filter(pk=user.pk).count(),
                }
            )

        response = {
            "items": user_list,
            "total": paginator.count,
            "num_pages": paginator.num_pages
        }
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'role', 'age', 'locations']

    def post(self, request, *args, **kwargs):
        response = []
        user_data = json.loads(request.body)
        location_data = Location.objects.get(name=", ".join(user_data['locations']))
        user = User.objects.create(
            username=user_data['username'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            role=user_data['role'],
            age=user_data['age'],
            location=location_data
        )

        response.append(
            {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "locations": user.location.name.split(','),
            }
        )
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'password', 'role', 'age', 'location']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        response = []
        user_data = json.loads(request.body)
        self.object.first_name = user_data['first_name']
        self.object.last_name = user_data['last_name']
        self.object.username = user_data['username']
        self.object.password = user_data['password']
        self.object.role = user_data['role']
        self.object.age = user_data['age']
        location_data = Location.objects.get(name=", ".join(user_data['locations']))
        self.object.location = location_data

        self.object.save()

        response.append(
            {
                "id": self.object.id,
                "username": self.object.username,
                "first_name": self.object.first_name,
                "last_name": self.object.last_name,
                "age": self.object.age,
                "locations": self.object.location.name.split(','),
            }
        )
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=200)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        response = []
        user = self.get_object()
        response.append(
            {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "locations": user.location.name.split(','),
                "total_ads": Ad.objects.all().filter(pk=user.pk).count(),
            }
        )

        return JsonResponse(response, safe=False)
