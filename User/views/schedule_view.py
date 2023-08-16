from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from ..models import Schedule
from ..serializer import ScheduleSerializers



@csrf_exempt
def schedule(request, diary_date, user_id):
    if request.method == 'GET':
        try:
            schedule = Schedule.objects.get(diary_date=diary_date, user_id=user_id)
            if schedule.image_pass:
                return JsonResponse({'diary_date': schedule.diary_date, 'image_pass': schedule.image_pass, 'etc':schedule.etc}, status=200)
            else:
                return JsonResponse({'diary_date': schedule.diary_date, 'image_pass': 'no data', 'etc':schedule.etc}, status=200)
        except Schedule.DoesNotExist:
            return JsonResponse({'error': 'data not found.'}, status=404)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ScheduleSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

