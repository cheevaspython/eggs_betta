from dataclasses import dataclass

        
@dataclass(slots=True, frozen=True)
class SubscribeToRoom():
    """
    """
    room_id: int 
    room_name: str
    room_host: str
    add_message: str = "Вы добавлены в комнату чата" 
    
