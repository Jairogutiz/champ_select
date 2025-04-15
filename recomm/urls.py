from django.urls import path
from . import views

urlpatterns = [
    path('recommendations/<str:session_id>/<str:role>/', views.recommendations, name='recommendations'),
    path('recommendations/<str:session_id>/', views.role_selector, name='role_selector'),
    path('recommendations/', views.recommendations, name='recommendations_post'),
    path('test_cache/<str:session_id>/<str:role>/', views.test_cache, name='test_cache'),
    path('test_cache/<str:session_id>/', views.test_cache, name='test_cache'),
]

