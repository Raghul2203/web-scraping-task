from django.urls import path
from .views import content, detail
app_name = "scrap"
urlpatterns = [
    path('content', content, name='content' ),
    path('detail/<path:qs>/', detail, name='detail')
]
