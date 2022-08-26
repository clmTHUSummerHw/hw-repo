from typing import Any, Callable, Dict
from flask_socketio import SocketIO

from ws.connect_ws import connect_ws
from ws.disconnect_ws import disconnect_ws


# 用于连接Websocket的类
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
        self.__ws.on('connect_ws', connect_ws, self.namespace)
        self.__ws.on('disconnect_ws', disconnect_ws, self.namespace)
        for i in self.__handlers:
            self.__ws.on_event(i, self.__handlers[i], self.namespace)

    def on_event(self, event_name: str, handler: Callable[[Any], None]) -> None:
        if self.__ws is None:
            self.__handlers[event_name] = handler
        else:
            self.__ws.on_event(event_name, handler, self.namespace)

    # 把事件发送给指定用户。event_name：事件名称，args：事件参数
    def emit(self, session: str, event_name: str, *args: Any) -> None:
        self.__ws.emit(event_name, args=args, to=session)