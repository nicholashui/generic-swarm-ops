import { create } from "zustand";
type Notification = { id: string; title: string; description: string };
export const useNotificationStore = create<{ notifications: Notification[]; push: (notification: Notification) => void; remove: (id: string) => void }>((set) => ({ notifications: [], push: (notification) => set((state) => ({ notifications: [notification, ...state.notifications].slice(0, 5) })), remove: (id) => set((state) => ({ notifications: state.notifications.filter((notification) => notification.id !== id) })) }));
