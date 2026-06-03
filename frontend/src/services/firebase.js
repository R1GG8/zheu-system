import { initializeApp } from "firebase/app";
import { getMessaging, getToken, onMessage } from "firebase/messaging";

const firebaseConfig = {
  apiKey: "AIzaSyC2gA0-CmBWDvIIvCYCpGDc_AGI-lJCoXU",
  authDomain: "zheu-system.firebaseapp.com",
  projectId: "zheu-system",
  storageBucket: "zheu-system.firebasestorage.app",
  messagingSenderId: "687928237913",
  appId: "1:687928237913:web:575faec5d95a555d36f648"
};

const app = initializeApp(firebaseConfig);
const messaging = getMessaging(app);

export const requestNotificationPermission = async () => {
  try {
    const permission = await Notification.requestPermission();
    if (permission === 'granted') {
      const token = await getToken(messaging, { 
        vapidKey: 'BFZs6x7mzYn76fjFsEsZYrFDu8AKC0ZWLK2bHofAha82BdAzDFtfypcE6gXLiJ4wV8xYHIoWqCbph3sL_10CRPo' 
      });
      return token;
    }
  } catch (error) {
    console.error('Ошибка при настройке Push-уведомлений:', error);
  }
  return null;
};

// Обработка уведомлений, когда сайт открыт перед глазами пользователя
onMessage(messaging, (payload) => {
  alert(`🔔 ${payload.notification.title}\n\n${payload.notification.body}`);
});