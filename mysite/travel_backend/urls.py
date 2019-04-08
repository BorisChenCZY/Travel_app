from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('account/', views.account_info, name='accountInfo'),
    path('info/', views.info_page, name='accountInfo'),
    path('info/delete_article', views.delete_article, name="deleteArticle"),
    path('info/<str:article>', views.info_page, name='accountInfo'),
    path('account/change_password', views.change_password, name="changePassword"),
    path('appointment/change_info', view = views.appointment_change, name='appointmentInfo'),
    path('appointment/<str:filter>', view = views.appointment_info, name='appointmentInfo'),
    path('appointment/', view = views.appointment_info, name='appointmentInfo'),
    path('login/', auth_views.LoginView.as_view(template_name="login/login.html"), name='login'),

    # path("/info/public/<str:rest>", lambda request, rest: redirect('/static/public/' + rest)),
    path('wx/article_list', view = views.wx_article_list, name="wx_article_list"),
    path('wx/article/<str:idx>', view = views.wx_get_article, name="wx_get_article"),
    path('wx/comment/', view = views.wx_comment, name="wx_get_article"),

]
