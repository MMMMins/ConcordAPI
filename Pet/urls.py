from django.conf.urls.static import static
from django.urls import path

from Concord import settings
from .views import pet_view

urlpatterns = [
    path('test/',pet_view.save_pet_info),
    path('imgload/<regnumber>/', pet_view.imgLoadHTML),
    path('aistart/', pet_view.ai_start)

]

urlpatterns += static(
        settings.MEDIA_URL,
        document_root = settings.MEDIA_ROOT)