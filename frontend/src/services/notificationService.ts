import axios from 'axios';

const API_URL = 'http://localhost:8000';

export interface Notification {
    id: number;
    title: string;
    message: string;
    type: 'info' | 'warning' | 'error' | 'success';
    is_read: boolean;
    created_at: string;
    user_id: number;
}

export interface NotificationCreate {
    title: string;
    message: string;
    type: 'info' | 'warning' | 'error' | 'success';
    user_id: number;
}

class NotificationService {
    async getNotifications(userId: number): Promise<Notification[]> {
        const response = await axios.get(`${API_URL}/notifications/${userId}`);
        return response.data;
    }

    async markAsRead(notificationId: number): Promise<void> {
        await axios.put(`${API_URL}/notifications/${notificationId}/read`);
    }

    async createNotification(notification: NotificationCreate): Promise<Notification> {
        const response = await axios.post(`${API_URL}/notifications/`, notification);
        return response.data;
    }
}

export const notificationService = new NotificationService(); 