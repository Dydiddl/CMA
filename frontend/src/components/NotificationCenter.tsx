import React, { useEffect, useState } from 'react';
import { 
    Badge, 
    IconButton, 
    Menu, 
    MenuItem, 
    List, 
    ListItem, 
    ListItemText, 
    Typography,
    Box
} from '@mui/material';
import NotificationsIcon from '@mui/icons-material/Notifications';
import { notificationService, Notification } from '../services/notificationService';

interface NotificationCenterProps {
    userId: number;
}

export const NotificationCenter: React.FC<NotificationCenterProps> = ({ userId }) => {
    const [notifications, setNotifications] = useState<Notification[]>([]);
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
    const [ws, setWs] = useState<WebSocket | null>(null);

    useEffect(() => {
        // 초기 알림 로드
        loadNotifications();

        // WebSocket 연결
        const websocket = new WebSocket(`ws://localhost:8000/ws/${userId}`);
        
        websocket.onmessage = (event) => {
            const notification = JSON.parse(event.data);
            setNotifications(prev => [notification, ...prev]);
        };

        websocket.onclose = () => {
            console.log('WebSocket 연결이 종료되었습니다.');
        };

        setWs(websocket);

        return () => {
            websocket.close();
        };
    }, [userId]);

    const loadNotifications = async () => {
        try {
            const data = await notificationService.getNotifications(userId);
            setNotifications(data);
        } catch (error) {
            console.error('알림을 불러오는데 실패했습니다:', error);
        }
    };

    const handleClick = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleNotificationClick = async (notification: Notification) => {
        if (!notification.is_read) {
            try {
                await notificationService.markAsRead(notification.id);
                setNotifications(prev =>
                    prev.map(n =>
                        n.id === notification.id ? { ...n, is_read: true } : n
                    )
                );
            } catch (error) {
                console.error('알림 상태 업데이트에 실패했습니다:', error);
            }
        }
    };

    const unreadCount = notifications.filter(n => !n.is_read).length;

    return (
        <Box>
            <IconButton color="inherit" onClick={handleClick}>
                <Badge badgeContent={unreadCount} color="error">
                    <NotificationsIcon />
                </Badge>
            </IconButton>
            <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleClose}
                PaperProps={{
                    style: {
                        maxHeight: 400,
                        width: 360,
                    },
                }}
            >
                {notifications.length === 0 ? (
                    <MenuItem>
                        <Typography>새로운 알림이 없습니다</Typography>
                    </MenuItem>
                ) : (
                    <List>
                        {notifications.map((notification) => (
                            <ListItem
                                key={notification.id}
                                button
                                onClick={() => handleNotificationClick(notification)}
                                sx={{
                                    backgroundColor: notification.is_read ? 'inherit' : 'action.hover',
                                }}
                            >
                                <ListItemText
                                    primary={notification.title}
                                    secondary={
                                        <>
                                            <Typography component="span" variant="body2" color="text.primary">
                                                {notification.message}
                                            </Typography>
                                            <br />
                                            <Typography component="span" variant="caption" color="text.secondary">
                                                {new Date(notification.created_at).toLocaleString()}
                                            </Typography>
                                        </>
                                    }
                                />
                            </ListItem>
                        ))}
                    </List>
                )}
            </Menu>
        </Box>
    );
}; 