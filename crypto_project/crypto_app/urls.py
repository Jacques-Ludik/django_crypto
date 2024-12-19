from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api-data/', views.fetch_api_data, name='api-data'),
    path('store-data/', views.store_data, name='store-data'),
    path('retrieve-data/', views.retrieve_data, name='retrieve-data'),
]

urlpatterns += [
    path('', views.index, name='index'),
]
