from injector import Injector
from typing import Any, Type

class Mediator:
    def __init__(self, injector: Injector):
        self.injector = injector
    
    def send(self, command: Any) -> Any:
        command_name = command.__class__.__name__
        handler_name = command_name.replace("Command", "CommandHandler").replace("Query", "QueryHandler")
        return self._get_handler_type(command_name, handler_name)
    
    def _get_handler_type(self, command_name: Any, handler_name: Any) -> Type[Any]:
        
        handler = self.injector.get(handler_name)
        return handler.handle(command_name)