# composition version

from datetime import datetime
from typing import Protocol

# Behavior interface (small, focused)
class MessageFormatter:
    def format(self, message: str) -> str:
        now = datetime.now().strftime("%H:%M:%S")
        return f"[{now}] {message}"


# Delivery strategies (very focused responsibilities)
class EmailSender:
    def send(self, to: str, subject: str, body: str) -> bool:
        print(f"EMAIL  →  {to} | Subject: {subject}")
        print(f"       {body}")
        return True


class SMSSender:
    def send(self, to: str, body: str) -> bool:
        print(f"SMS    →  {to}")
        print(f"       {body[:160]}...")  # simulate limit
        return True


class PushSender:
    def send(self, device_token: str, body: str) -> bool:
        print(f"PUSH   →  {device_token[:8]}…")
        print(f"       {body}")
        return True


# The actual notification class — composes behavior
class Notification:
    def __init__(
        self,
        recipient: str,
        message: str,
        sender,                   # any object with .send() method
        formatter=MessageFormatter(),
        subject: str | None = None,
    ):
        self.recipient = recipient
        self.message = message
        self.sender = sender
        self.formatter = formatter
        self.subject = subject or "Notification"
    
    def send(self) -> bool:
        formatted_body = self.formatter.format(self.message)
        
        # Different senders expect different arguments → we adapt here
        if isinstance(self.sender, EmailSender):
            return self.sender.send(self.recipient, self.subject, formatted_body)
        elif isinstance(self.sender, SMSSender):
            return self.sender.send(self.recipient, formatted_body)
        elif isinstance(self.sender, PushSender):
            return self.sender.send(self.recipient, formatted_body)
        else:
            raise ValueError("Unsupported sender type")


# Usage
if __name__ == "__main__":
    formatter = MessageFormatter()
    
    email = Notification(
        recipient="user@company.com",
        message="Your order #4521 has shipped!",
        sender=EmailSender(),
        formatter=formatter,
        subject="Order Update"
    )
    
    sms = Notification(
        recipient="+491701234567",
        message="Your verification code is 918273",
        sender=SMSSender(),
        formatter=formatter
    )
    
    push = Notification(
        recipient="ExponentPushToken[abcd1234]",
        message="You have a new friend request!",
        sender=PushSender(),
        formatter=formatter
    )
    
    email.send()
    sms.send()
    push.send()