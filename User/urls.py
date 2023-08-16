from django.urls import path

from .views import user_view

urlpatterns = [
    path('signup/', user_view.user_sign_up), # 회원가입
    path('login/', user_view.user_login),
    path('<user_id>/', user_view.user_id_check), # 아이디 중복체크
    path('pets/info/<user_id>/', user_view.get_user_and_pet),
]

