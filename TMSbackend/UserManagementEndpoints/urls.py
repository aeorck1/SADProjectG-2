from django.urls import path
from UserManagementEndpoints import views

app_name = 'UserManagementEndpoints'
urlpatterns = [
    path('create/', view=views.CreateUserView.as_view(), name='create'),
    path('createmanager/', view=views.CreateManagerView.as_view(), name='createmanager'),
    path('authenticate/', view=views.AuthTokenView.as_view(), name='authenticate'),
    path('me/', view=views.ManageUserView.as_view(), name='me'),
]