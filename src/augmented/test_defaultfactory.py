from dataclasses import dataclass, field
from typing import List

@dataclass
class ChatClient:
    messages: List[str] = field(default_factory=list)

client1 = ChatClient()
client2 = ChatClient()

client1.messages.append("hello default factory")
print(client1.messages)
print(client2.messages)
