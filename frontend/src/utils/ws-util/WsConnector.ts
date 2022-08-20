import type { Socket } from 'socket.io-client';
import { io } from 'socket.io-client';

const root_path = 'ws://localhost:5000'

export default class WSConnector
{
    connection: Socket
    private session: string
    constructor(namespace: string, session: string)
    {
        this.connection = io(root_path + namespace);
        this.session = session;
        this.connection.connect();
        this.connection.emit('connect_ws', {session: this.session});
    }

    emit()
    {
        
    }
}