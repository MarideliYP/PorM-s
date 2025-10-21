from django.urls import path
from .views import Register, Login, logout_view, user_update, User_list, user_delete, User_details, verify_email_view, \
    resend_code_view, update_img

app_name = 'user'


urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('verificar-correo/<str:username>/', verify_email_view, name='verify_email'),
    path('reenviar-codigo/<str:username>/', resend_code_view, name='resend_code'),
    path('list/', User_list.as_view(), name='list'),
    path('<int:pk>/details/', User_details.as_view(), name='details'),
    path('<int:pk>/delete/', user_delete, name='delete'),
    path('<int:pk>/update/', user_update, name='update'),
    path('<int:pk>/updatei/', update_img, name='updatei'),
]

