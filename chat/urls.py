from django.urls import path

from chat.views import SendMessageView, ChatHistoryView

urlpatterns = [
    path('', SendMessageView.as_view(), name='message-send'),
    path('<int:user_id>/', ChatHistoryView.as_view(), name='chat-history'),
]
