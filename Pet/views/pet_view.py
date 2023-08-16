import base64
import os
import subprocess
import uuid
from datetime import datetime
from os import path

from PIL import Image
from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from Concord.settings import BASE_DIR
from User.models import User
from Concord import settings
from Pet.models import Pet_info
from Pet.serializer import RegPetSerializers
from User.serializer import UserAndPetSerializers

imageRootDir = 'static/pet_image'


@csrf_exempt
def ai_start(request):
    # JPG 파일 저장
    if request.method == "POST":
        project_directory = settings.BASE_DIR
        '''
            ai부분 실행 부분 삭제
        '''
        data_str = data.decode('utf-8')  # bytes를 문자열로 디코딩
        split_data = data_str.split('\n')  # \n을 기준으로 분리
        other_data = split_data[1].split(',')
        try:
            pet = Pet_info.objects.get(register_number=other_data[0])
            pet_data = {
                "user_id": pet.user_id.user_id,
                "register_number": pet.register_number,
                "pet_date": pet.pet_date,
                "pet_name": pet.pet_name,
                "pet_gender": pet.pet_gender,
                "pet_breed": pet.pet_breed,
                "pet_size": pet.pet_size
            }
            try:
                user = User.objects.get(user_id=pet.user_id.user_id)
                result_data = {
                    "user_id": user.user_id,
                    "user_phone": user.phone,
                    "register_number": pet.register_number,
                    "pet_name": pet.pet_name,
                    "pet_breed": pet.pet_breed,
                    "result": other_data[1] if float(other_data[1]) > float(other_data[2]) else other_data[2]
                }
                return JsonResponse(result_data)
            except User.DoesNotExist:
                return JsonResponse({"ERROR": "User not found"}, status=404)
        except Pet_info.DoesNotExist:
            return JsonResponse({"ERROR": "Pet not found"}, status=404)

@csrf_exempt
def imgLoadHTML(request, regnumber):
    image_path = f'static/pet_image/{regnumber}/{regnumber}_0.jpg'
    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            image_data = f.read()
            return HttpResponse(image_data, content_type='image/jpeg')
    else:
        return HttpResponse(status=404)
    #
    # media_root = settings.MEDIA_ROOT
    # return render(request, "imgfileload.html", {'image_path': f'pet_image/{regnumber}/{regnumber}_0.jpg'})


@csrf_exempt
def save_pet_info(request):
    print("Request Data:", request.POST)
    pet_image_data = request.FILES.get('pet_image')
    print("Received pet image:", pet_image_data)
    if request.method == 'POST':
        serializer = RegPetSerializers(data=request.POST)

        if serializer.is_valid():
            # register_number 값을 "M연월일-uid" 형식으로 생성
            # now = datetime.now()
            # year_month_day = now.strftime("%Y%m%d")
            register_number = request.POST.get('register_number')
            #f"M{year_month_day}-{uuid.uuid4().hex[:8]}"

            # Base64 인코딩된 이미지 데이터를 디코딩하여 Pillow 이미지로 변환
            try:
                pet_image_data = request.FILES.get('pet_image')
                pet_image = Image.open(pet_image_data)
            except Exception as e:
                return JsonResponse({'error': 'Invalid image data.', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            # 폴더체크후 없으면 생성
            if not path.exists(f'{imageRootDir}/{register_number}'):
                os.mkdir(f'{imageRootDir}/{register_number}')

            # 저장할 이미지 파일 경로 설정
            pet_image_path = f'{register_number}/{register_number}_0.jpg'
            print(pet_image_path)
            print(imageRootDir)
            # Pillow 이미지를 파일로 저장
            try:
                pet_image.save(f'{imageRootDir}/{pet_image_path}', format='JPEG')
            except Exception as e:
                return JsonResponse({'error': 'Failed to save image.', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # serializer 데이터에 register_number를 추가하여 모델에 저장
            serializer.validated_data['register_number'] = register_number
            serializer.validated_data['pet_image'] = pet_image_path
            serializer.save()
            return JsonResponse({'message': 'Pet info saved successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
