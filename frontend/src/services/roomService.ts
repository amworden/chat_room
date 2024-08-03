export const getChatRooms = async () => {
    const response = await fetch('http://localhost:8000/rooms');
    if (!response.ok) {
        throw new Error('Failed to fetch chat rooms');
    }
    return response.json();
};

export const createChatRoom = async (name: any) => {
    const response = await fetch('http://localhost:8000/rooms', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name }),
    });
    if (!response.ok) {
        throw new Error('Failed to create chat room');
    }
    return response.json();
};

export const deleteChatRoom = async (id: any) => {
    const response = await fetch(`http://localhost:8000/rooms/${id}`, {
        method: 'DELETE',
    });
    if (!response.ok) {
        throw new Error('Failed to delete chat room');
    }
    return response.json();
};

export const joinRoom = async (roomId: any, userId: any) => {
    const response = await fetch(`http://localhost:8000/rooms/${roomId}/join?user_id=${userId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    });
    if (!response.ok) {
        throw new Error('Failed to join room');
    }
    return response.json();
};


export const leaveRoom = async (roomId: any, userId: any) => {
    const response = await fetch(`http://localhost:8000/rooms/${roomId}/leave`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: userId }),
    });
    if (!response.ok) {
        throw new Error('Failed to leave room');
    }
    return response.json();
};
