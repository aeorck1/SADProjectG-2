from ResourceAllocation import views
from django.urls import path


urlpatterns = [
    path('generate/', view=views, name='generate'),
    path('fetch/<int:id>/', view=views, name='fetch')
]