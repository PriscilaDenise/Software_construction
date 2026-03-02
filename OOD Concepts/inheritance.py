# inheritance version

from abc import ABC, abstractmethod
from datetime import datetime

class Notification(ABC):
    """Base class - defines the interface"""
    
    def __init__(self, recipient: str, message: str):
        self.recipient = recipient
        self.message = message
        self.timestamp = datetime.now()
    
    def format_message(self) -> str:
        return f"[{self.timestamp.strftime('%H:%M:%S')}] {self.message}"
    
    @abstractmethod
    def send(self) -> bool:
        pass


class EmailNotification(Notification):
    """Is-a Notification"""
    
    def __init__(self, recipient: str, message: str, subject: str = "Notification"):
        super().__init__(recipient, message)
        self.subject = subject
    
    def send(self) -> bool:
        formatted = self.format_message()
        print(f"EMAIL  →  {self.recipient} | Subject: {self.subject}")
        print(f"       {formatted}")
        return True


class SMSNotification(Notification):
    """Is-a Notification"""
    
    def send(self) -> bool:
        formatted = self.format_message()
        print(f"SMS    →  {self.recipient}")
        print(f"       {formatted[:160]}...")  # simulate SMS length limit
        return True


# Usage
if __name__ == "__main__":
    email = EmailNotification("user@company.com", "Your order #4521 has shipped!", "Order Update")
    sms   = SMSNotification("+491701234567", "Your verification code is 918273")
    
    email.send()
    sms.send()