import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { getChatRooms, createChatRoom, joinRoom, leaveRoom } from '@/services/roomService';
import { getUserId } from '@/lib/userStorage';
import useWebSocket from '@/hooks/webSocket';

// handle the room landing page and the room creation functionality
const RoomComponent = () => {
    const [rooms, setRooms] = useState<any[]>([]);
    const [newRoomName, setNewRoomName] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const router = useRouter();
    const userId = getUserId();
    const { alerts, removeAlert } = useWebSocket(null, true);

    // router.push('/signup') if userId is not set
    useEffect(() => {
        if (!userId) {
            router.push('/signup');
            return;
        }
        fetchRooms();
    }, [userId]);

    // fetch rooms from the server
    const fetchRooms = async () => {
        try {
            setLoading(true);
            const roomsData = await getChatRooms();
            setRooms(roomsData);
        } catch (err) {
            setError('Failed to fetch rooms');
        } finally {
            setLoading(false);
        }
    };

    // method to handle the join and leave room functionality
    const handleJoinLeaveRoom = async (roomId: number, isMember: boolean) => {
        try {
            setLoading(true);
            if (isMember) {
                await leaveRoom(roomId, userId);
            } else {
                await joinRoom(roomId, userId);
            }
            fetchRooms();
        } catch (err) {
            setError(`Failed to ${isMember ? 'leave' : 'join'} room`);
        } finally {
            setLoading(false);
        }
    };

    // method to handle creating a new room
    const handleCreateRoom = async () => {
        try {
            setLoading(true);
            await createChatRoom(newRoomName);
            setNewRoomName('');
            fetchRooms();
        } catch (err) {
            setError('Failed to create room');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100 p-4">
            <Card className="w-full max-w-4xl shadow-lg rounded-lg overflow-hidden">
                <CardHeader className="bg-primary text-primary-foreground p-6">
                    <CardTitle className="text-3xl">Chat Rooms</CardTitle>
                    <CardDescription className="mt-2">Manage your chat rooms and view their details!</CardDescription>
                </CardHeader>
                <CardContent className="p-6">
                    {error && <div className="text-red-500 mb-4">{error}</div>}
                    <div className="mb-6">
                        <input
                            type="text"
                            value={newRoomName}
                            onChange={(e) => setNewRoomName(e.target.value)}
                            className="border border-gray-300 rounded-md p-2 mr-2"
                            placeholder="New Room Name"
                        />
                        <button
                            onClick={handleCreateRoom}
                            className="bg-blue-500 text-white px-4 py-2 rounded-md"
                            disabled={loading}
                        >
                            {loading ? 'Creating...' : 'Create Room'}
                        </button>
                    </div>
                    <table className="w-full">
                        <thead>
                        <tr>
                            <th className="text-left">Name</th>
                            <th className="text-left">Status</th>
                            <th className="text-right">
                                <span className="sr-only">Actions</span>
                            </th>
                        </tr>
                        </thead>
                        <tbody>
                        {rooms.map((room) => {
                            // check if the user is a member of the room
                            const isMember = room.members.some((member: any) => member.id === userId);
                            return (
                                <tr key={room.id}>
                                    <td className="font-medium">
                                        <Link href={`/rooms/${room.id}`}>
                                            <span className="text-blue-500 hover:underline cursor-pointer">
                                                {room.name}
                                            </span>
                                        </Link>
                                    </td>
                                    <td>
                                        <span
                                            className={`px-2 py-1 rounded-full ${
                                                // change the color based on the user membership status
                                                isMember ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                                            }`}
                                        >
                                            {isMember ? 'Leave' : 'Join'}
                                        </span>
                                    </td>
                                    <td className="text-right">
                                        <button
                                            onClick={() => handleJoinLeaveRoom(room.id, isMember)}
                                            className={`px-3 py-1 rounded-md ml-2 ${
                                                isMember ? 'bg-red-500 text-white' : 'bg-green-500 text-white'
                                            }`}
                                            disabled={loading}
                                        >
                                            {loading ? 'Processing...' : isMember ? 'Leave' : 'Join'}
                                        </button>
                                    </td>
                                </tr>
                            );
                        })}
                        </tbody>
                    </table>
                </CardContent>
                <CardFooter className="bg-gray-100 p-4">
                    <div className="text-xs text-gray-500">
                        Showing <strong>{rooms.length}</strong> rooms
                    </div>
                </CardFooter>
            </Card>

            {alerts.map((alert) => (
                // display the alert message not quite fully implemented
                <Alert key={alert.id} className="fixed bottom-4 right-4 bg-white p-4 rounded shadow-lg">
                    <AlertTitle>New Message</AlertTitle>
                    <AlertDescription>
                        {alert.content} - <Link href={`/rooms/${alert.room_id}`}><span className="text-blue-500 hover:underline cursor-pointer">Go to room</span></Link>
                    </AlertDescription>
                    <button onClick={() => removeAlert(alert.id)}>Close</button>
                </Alert>
            ))}
        </div>
    );
};

export default RoomComponent;
