import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import useWebSocket from '@/hooks/webSocket';

// handle the alerts component to show alerts for new messages
// not fully implemented yet
const AlertsComponent = ({ roomId }: { roomId: string }) => {
    const { alerts, removeAlert } = useWebSocket(roomId, true);
    const router = useRouter();

    return (
        <div className="fixed bottom-0 right-0 m-4 space-y-2">
            {alerts.map((alert) => (
                <Alert key={alert.id}>
                    <AlertTitle>New Message</AlertTitle>
                    <AlertDescription>
                        {alert.content}
                    </AlertDescription>
                    <button onClick={() => {
                        router.push(`/rooms/${alert.room_id}`);
                        removeAlert(alert.id);
                    }} className="ml-auto text-blue-500">View</button>
                </Alert>
            ))}
        </div>
    );
};

export default AlertsComponent;
