from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='list'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='detail'),
    path('manage/', views.EventManageView.as_view(), name='manage'),
    path('create/', views.EventCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.EventUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='delete'),
]
