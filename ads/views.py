import json

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ads.models import Ad, Categori


def ads(request):
    return JsonResponse({"status": "ok"}, status=200)

@csrf_exempt
def get_all_ad(request):
    response = []
    if request.method == "GET":
        ad_list = Ad.objects.all()
        for ad in ad_list:
            response.append(
                {
                    "id": ad.id,
                    "name": ad.name,
                    "author": ad.author,
                    "price": ad.price,
                    "description": ad.description,
                    "address": ad.address,
                    "is_published": ad.is_published,
                }
            )
        return JsonResponse(response, safe=False)
    elif request.method == "POST":
        ad_data = json.loads(request.body)

        ad = Ad()
        ad.name = ad_data['name']
        ad.author = ad_data['author']
        ad.price = ad_data['price']
        ad.description = ad_data['description']
        ad.address = ad_data['address']
        ad.is_published = ad_data['is_published']

        ad.save()
        response.append(
            {
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published,
            }
        )
        return JsonResponse(response, safe=False)

def get_ad(request,ad_id):
    response = []
    if request.method == "GET":
        ad = get_object_or_404(Ad, id=ad_id)
        response.append(
                {
                    "id": ad.id,
                    "name": ad.name,
                    "author": ad.author,
                    "price": ad.price,
                    "description": ad.description,
                    "address": ad.address,
                    "is_published": ad.is_published,
                }
            )
        return JsonResponse(response, safe=False)


@csrf_exempt
def get_all_cat(request):
    response = []
    if request.method == "GET":
        cat_list = Categori.objects.all()
        for cat in cat_list:
            response.append(
                {
                    "id": cat.id,
                    "name": cat.name,
                }
            )
        return JsonResponse(response, safe=False)
    elif request.method == "POST":
        cat_data = json.loads(request.body)

        cat = Categori()
        cat.name = cat_data['name']
        cat.save()
        response = [{
            "id": cat.id,
            "name": cat.name,
        }]
        return JsonResponse(response, safe=False)


def get_cat(request,cat_id):
    if request.method == "GET":
        cat = get_object_or_404(Categori, id=cat_id)
        response = []
        response.append(
            {
                "id": cat.id,
                "name": cat.name,
            }
        )
    return JsonResponse(response, safe=False)