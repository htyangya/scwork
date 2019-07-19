from django.urls import path,include
from .views.submit_btn import flow_view
app_name='submit'
urlpatterns = [
    path('flow',flow_view,name='flow'),
]