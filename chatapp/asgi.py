"""
ASGI config for chatapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""


import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
import chats.routing
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'channel.settings')
application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  # Just HTTP for now. (We can add other protocols later.)
  'websocket':AuthMiddlewareStack( URLRouter(   #authmiddlewarestack is used to acess authmiddleware, sessionmiddleware,
                                                #cookiemiddleware ->ex if u need user in ur channel
    chats.routing.websocket_urlpatterns
  ))
})