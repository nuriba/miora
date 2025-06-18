import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from try_on.models import TryOnSession
from avatars.models import Avatar

User = get_user_model()

class TryOnConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f'tryon_{self.session_id}'
        self.user = self.scope['user']
        
        if self.user.is_anonymous:
            await self.close()
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        # Send initial connection message
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connected to try-on session',
            'session_id': self.session_id
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'garment_change':
                await self.handle_garment_change(data)
            elif message_type == 'fit_analysis':
                await self.handle_fit_analysis(data)
            elif message_type == 'avatar_update':
                await self.handle_avatar_update(data)
            elif message_type == 'session_save':
                await self.handle_session_save(data)
            else:
                await self.send_error('Unknown message type')
                
        except json.JSONDecodeError:
            await self.send_error('Invalid JSON')
        except Exception as e:
            await self.send_error(f'Error processing message: {str(e)}')

    async def handle_garment_change(self, data):
        garment_id = data.get('garment_id')
        if not garment_id:
            await self.send_error('Missing garment_id')
            return
        
        # Simulate garment processing time
        await asyncio.sleep(0.5)
        
        # Send garment update to all clients in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'garment_update',
                'garment_id': garment_id,
                'status': 'applied',
                'timestamp': self._get_timestamp()
            }
        )

    async def handle_fit_analysis(self, data):
        measurements = data.get('measurements', {})
        
        # Simulate fit analysis processing
        await asyncio.sleep(1.0)
        
        # Mock fit analysis results
        fit_results = {
            'overall_fit': 'good',
            'fit_score': 85,
            'areas': {
                'chest': {'fit': 'perfect', 'score': 95},
                'waist': {'fit': 'loose', 'score': 75},
                'shoulders': {'fit': 'good', 'score': 88},
                'length': {'fit': 'good', 'score': 82}
            },
            'recommendations': [
                'Consider sizing down for a more fitted look',
                'The shoulders fit perfectly',
                'Length is appropriate for your height'
            ]
        }
        
        await self.send(text_data=json.dumps({
            'type': 'fit_analysis_result',
            'results': fit_results,
            'timestamp': self._get_timestamp()
        }))

    async def handle_avatar_update(self, data):
        avatar_data = data.get('avatar_data', {})
        
        # Update avatar in database
        try:
            await self._update_avatar(avatar_data)
            await self.send(text_data=json.dumps({
                'type': 'avatar_updated',
                'status': 'success',
                'timestamp': self._get_timestamp()
            }))
        except Exception as e:
            await self.send_error(f'Failed to update avatar: {str(e)}')

    async def handle_session_save(self, data):
        session_data = data.get('session_data', {})
        
        try:
            await self._save_session(session_data)
            await self.send(text_data=json.dumps({
                'type': 'session_saved',
                'status': 'success',
                'timestamp': self._get_timestamp()
            }))
        except Exception as e:
            await self.send_error(f'Failed to save session: {str(e)}')

    async def garment_update(self, event):
        # Send garment update to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'garment_change_result',
            'garment_id': event['garment_id'],
            'status': event['status'],
            'timestamp': event['timestamp']
        }))

    async def send_error(self, message):
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': message,
            'timestamp': self._get_timestamp()
        }))

    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()

    @database_sync_to_async
    def _update_avatar(self, avatar_data):
        # Update avatar in database
        avatar = Avatar.objects.filter(user=self.user).first()
        if avatar and avatar_data:
            for key, value in avatar_data.items():
                if hasattr(avatar, key):
                    setattr(avatar, key, value)
            avatar.save()

    @database_sync_to_async
    def _save_session(self, session_data):
        # Save try-on session
        session = TryOnSession.objects.filter(id=self.session_id, user=self.user).first()
        if session and session_data:
            for key, value in session_data.items():
                if hasattr(session, key):
                    setattr(session, key, value)
            session.save()

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        
        if self.user.is_anonymous:
            await self.close()
            return
            
        self.room_group_name = f'notifications_{self.user.id}'
        
        # Join notification group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave notification group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def notification_message(self, event):
        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'data': event['data']
        })) 