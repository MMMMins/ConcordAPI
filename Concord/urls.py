from django.urls import path, include
import Pet
import User

urlpatterns = [
    path('api/pets/', include('Pet.urls')),
    path('api/users/', include('User.urls'))
]
