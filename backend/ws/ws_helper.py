from typing import Any, Callable, Dict
from flask_socketio import SocketIO


class WsHelper:
    __ws: SocketIO
    namespace: str
    __handlers: Dict[str, Callable[[Any], None]]
    def __init__(self, namespace: str) -> None:
        self.__ws = None
        self.namespace = namespace
        self.__handlers = {}

    def init_ws(self, ws: SocketIO) -> None:
        self.__ws = ws
        for i in self.__handlers:
            self.__ws.on_event(i, self.__handlers[i], self.namespace)

    def on_event(self, event_name: str, handler: Callable[[Any], None]) -> None:
        if self.__ws is None:
            self.__handlers[event_name] = handler
        else:
            self.__ws.on_event(event_name, handler, self.namespace)

    def emit(self, to: str, event_name: str, *args: Any) -> None:
        self.__ws.emit(event_name, args=args, to=to)