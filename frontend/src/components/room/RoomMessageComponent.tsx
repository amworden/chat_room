import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import useWebSocket from '@/hooks/webSocket';

// handle the room messages page and the message sending functionality
const RoomMessagesComponent = () => {
    const router = useRouter();
    const { roomId } = router.query;
    const { messages, sendMessage } = useWebSocket(roomId as string);
    const [newMessage, setNewMessage] = useState('');

    const handleSendMessage = () => {
        sendMessage(newMessage);
        setNewMessage('');
    };

    // get the text color based on the hex color
    const getTextColor = (hexColor: string) => {
        const isValidHex = /^#[0-9A-F]{6}$/i.test(hexColor);
        return isValidHex ? hexColor : '#D2042D';
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100 p-4">
            <Card className="w-full max-w-4xl shadow-lg rounded-lg overflow-hidden">
                <CardHeader className="bg-primary text-primary-foreground p-6">
                    <CardTitle className="text-3xl">Room {roomId} Messages</CardTitle>
                    <CardDescription className="mt-2">View and send messages in this room!</CardDescription>
                </CardHeader>
                <CardContent className="p-6">
                    <div className="mb-6">
                        <input
                            type="text"
                            value={newMessage}
                            onChange={(e) => setNewMessage(e.target.value)}
                            className="border border-gray-300 rounded-md p-2 mr-2"
                            placeholder="New Message"
                        />
                        <button
                            onClick={handleSendMessage}
                            className="bg-blue-500 text-white px-4 py-2 rounded-md"
                        >
                            Send Message
                        </button>
                    </div>
                    <ul className="space-y-4">
                        {messages.map((message) => (
                            <li key={message.id} className="bg-white p-4 rounded-md shadow-sm">
                                <p className="text-sm" style={{ color: getTextColor(message.user?.identity_color || '#D2042D') }}>
                                    {message.content}
                                </p>
                                <p className="text-xs text-gray-500">
                                    {message.user ? `User ${message.user.username}` : 'Unknown User'} - {new Date(message.timestamp).toLocaleString()}
                                </p>
                            </li>
                        ))}
                    </ul>
                </CardContent>
                <CardFooter className="bg-gray-100 p-4">
                    <div className="text-xs text-gray-500">
                        Showing <strong>{messages.length}</strong> messages
                    </div>
                </CardFooter>
            </Card>
        </div>
    );
};

export default RoomMessagesComponent;
