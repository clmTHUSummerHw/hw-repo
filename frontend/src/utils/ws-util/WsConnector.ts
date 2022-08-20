import type { Socket } from 'socket.io-client';
import { io } from 'socket.io-client';

const root_path = '/api'

export default class WSConnetor
{
    connection: Socket
    constructor(namespace: string)
    {
        this.connection = io(root_path + namespace)
        this.connection.on('connect', () => {
            console.log(this.connection);
        })
    }
}