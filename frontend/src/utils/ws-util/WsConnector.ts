import type { Socket } from 'socket.io-client';
import { io } from 'socket.io-client';

const root_path = 'ws://localhost:5000'

export default class WSConnector
{
    connection: Socket
    constructor(namespace: string)
    {
        this.connection = io(root_path)
        this.connection.on('connect', () => {
            console.log(this.connection);
        })
        this.connection.on('accept_connection', () => {
            console.log("connection accepted");
        })
        console.log('test')
        this.connection.connect();
        this.connection.emit('connect_ws', {session: '1234'})
    }
}