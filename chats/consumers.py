
from channels.consumer import SyncConsumer
from time import sleep
from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from .models import Chat,Group
import json
class EchoConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print("connection established")
        self.group_name=self.scope['url_route']['kwargs']['group_name']
        async_to_sync(self.channel_layer.group_add)(self.group_name,self.channel_name)
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        #print(event['text'])
        data=json.loads(event['text'])
      #  print(data['msg'])
    
        group=Group.objects.get(name=self.group_name)
    
        if self.scope['user'].is_authenticated:
            chat=Chat(content=data['msg'],group=group)
            chat.save()
            data['user']=self.scope['user'].username
            async_to_sync(self.channel_layer.group_send)(self.group_name,{
                'type':'chat.message',
                'message':json.dumps(data)

            })
        else:
            self.send({
                "type": "websocket.send",
                "text":json.dumps({"msg":"login required"})
            })

    def chat_message(self,event):
        print(event)   
        self.send({
                "type": "websocket.send",
                "text":event['message']
            })

    def websocket_disconnect(self,event):
        print("websocket disconnected")    
        async_to_sync(self.channel_layer.group_discard)(self.group_name,self.channel_name)
        raise StopConsumer()