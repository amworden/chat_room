import { useState } from 'react';
import { useRouter } from 'next/router';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { createUser } from '@/services/userService';
import { setUserId } from '@/lib/userStorage';

const UserSignupComponent = () => {
    const [username, setUsername] = useState<string>('');
    const [identityColor, setIdentityColor] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);
    const router = useRouter();

    // handle the user signup functionality
    const handleSignup = async () => {
        try {
            setLoading(true);
            const user = await createUser({ username, identity_color: identityColor });
            setUserId(user.id);
            setSuccess('User created successfully!');
            setError(null);
            router.push('/room');
        } catch (err) {
            setError('Failed to create user');
            setSuccess(null);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100 p-4">
            <Card className="w-full max-w-md shadow-lg rounded-lg overflow-hidden">
                <CardHeader className="bg-primary text-primary-foreground p-6">
                    <CardTitle className="text-3xl">Sign Up</CardTitle>
                    <CardDescription className="mt-2">Create your user profile</CardDescription>
                </CardHeader>
                <CardContent className="p-6">
                    {error && <div className="text-red-500 mb-4">{error}</div>}
                    {success && <div className="text-green-500 mb-4">{success}</div>}
                    <div className="mb-6">
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="border border-gray-300 rounded-md p-2 w-full mb-2"
                            placeholder="Username"
                        />
                        <input
                            type="text"
                            value={identityColor}
                            onChange={(e) => setIdentityColor(e.target.value)}
                            className="border border-gray-300 rounded-md p-2 w-full mb-2"
                            placeholder="Hex Color Code"
                        />
                        <button
                            onClick={handleSignup}
                            className="bg-blue-500 text-white px-4 py-2 rounded-md w-full"
                            disabled={loading}
                        >
                            {loading ? 'Signing Up...' : 'Sign Up'}
                        </button>
                    </div>
                </CardContent>
                <CardFooter className="bg-gray-100 p-4">
                    <div className="text-xs text-gray-500">
                        Enter a username and a hex color code for your messages
                    </div>
                </CardFooter>
            </Card>
        </div>
    );
};

export default UserSignupComponent;
