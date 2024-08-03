import { useEffect, useState } from 'react';
import axios from 'axios';
import { getUserId } from '@/lib/userStorage';

// custom hook to handle the WebSocket connection
const useWebSocket = (roomId: string | null, showAlerts = true) => {
    const [messages, setMessages] = useState<any[]>([]);
    const [alerts, setAlerts] = useState<any[]>([]);
    const [socket, setSocket] = useState<WebSocket | null>(null);

    useEffect(() => {
        if (roomId) {
            const fetchInitialMessages = async () => {
                try {
                    // fetch initial messages for the room
                    const response = await axios.get(`http://localhost:8000/messages/room/${roomId}`);
                    setMessages(response.data);
                } catch (error) {
                    console.error('Failed to fetch initial messages', error);
                }
            };

            fetchInitialMessages();

            const ws = new WebSocket(`ws://localhost:8000/ws/${roomId}`);
            // set the WebSocket connection
            setSocket(ws);

            ws.onopen = () => {
                console.log('Connected to WebSocket');
            };

            ws.onclose = () => {
                console.log('Disconnected from WebSocket');
            };

            ws.onmessage = (event) => {
                // parse the incoming message
                const parsedMessage = JSON.parse(event.data);
                // update the messages state with the new message
                setMessages((prevMessages) => [...prevMessages, parsedMessage]);

                // show alerts for new messages
                if (showAlerts) {
                    setAlerts((prevAlerts) => [
                        ...prevAlerts,
                        {
                            content: `${parsedMessage.user.username}: ${parsedMessage.content}`,
                            room_id: parsedMessage.room_id,
                            id: Date.now(),
                        },
                    ]);
                }
            };

            return () => {
                ws.close();
            };
        }
    }, [roomId, showAlerts]);

    // method to send a message to the WebSocket server
    const sendMessage = (content: string) => {
        if (socket) {
            const message = {
                room_id: roomId ? parseInt(roomId) : null,
                user_id: getUserId(),
                content,
            };
            console.log('Sending message', message);
            socket.send(JSON.stringify(message));
        }
    };

    // method to remove an alert from the alerts state
    const removeAlert = (id: number) => {
        setAlerts((prevAlerts) => prevAlerts.filter((alert) => alert.id !== id));
    };

    return { messages, sendMessage, alerts, removeAlert };
};

export default useWebSocket;
