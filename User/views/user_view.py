import base64
from django.contrib.auth import authenticate
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from Concord import settings
from Pet.serializer import PetSerializers
from ..models import User
from ..serializer import UserSerializers, UserAndPetSerializers
from Pet.models import Pet_info




@csrf_exempt
def get_user_and_pet(request, user_id):
    if request.method == "GET":
        try:
            user = User.objects.get(user_id=user_id)  # Assuming user is authenticated
            pets = Pet_info.objects.filter(user_id=user_id)

            user_serializer = UserAndPetSerializers(user)
            pets_data = []
            for pet in pets:

                # # Convert the image to base64
                # if pet.pet_image:
                #     with open(pet.pet_image.path, 'rb') as img_file:
                #         image_data = base64.b64encode(img_file.read()).decode('utf-8')
                #         print(image_data)

                pet_serializer = PetSerializers(pet)
                pets_data.append(pet_serializer.data)

            response_data = {
                'user': user_serializer.data,
                'pets': pets_data,
            }
            return JsonResponse(response_data, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        password = data.get('password')
        result = authenticate(request, user_id=user_id, password=password)
        if result:
            return JsonResponse({'code': '0001'}, status=200)
        else:
            user = User.objects.get(user_id=user_id)
            try:
                return JsonResponse({'code': '0002'}, status=401)
            except User.DoesNotExist:
                return JsonResponse({'code': '0003'}, status=401)


@csrf_exempt
def user_id_check(request, user_id):
    if request.method == 'GET':
        try:
            user = User.objects.get(user_id=user_id)
            return JsonResponse({'id': user.user_id}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)


@csrf_exempt
def user_sign_up(request):
    if request.method == 'GET':
        query_set = User.objects.all()
        serializer = UserSerializers(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

