from django.urls import path
from . import consumers

websocket_urlpatterns=[
    path('ws/sc/<str:group_name>/',consumers.EchoConsumer.as_asgi()),

]
