
from django.urls import path,include
from .views import personnelsview

urlpatterns = [
    path('choose',personnelsview,name="psnchoose"),

]
