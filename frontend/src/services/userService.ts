export const createUser = async (user: { username: string, identity_color: string }) => {
    const response = await fetch('http://localhost:8000/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(user),
    });
    if (!response.ok) {
        throw new Error('Failed to create user');
    }
    return response.json();
};
