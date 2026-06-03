importScripts("https://www.gstatic.com/firebasejs/10.14.1/firebase-app-compat.js");
importScripts("https://www.gstatic.com/firebasejs/10.14.1/firebase-messaging-compat.js");

firebase.initializeApp({
  apiKey: "AIzaSyC2gA0-CmBWDvIIvCYCpGDc_AGI-lJCoXU",
  authDomain: "zheu-system.firebaseapp.com",
  projectId: "zheu-system",
  storageBucket: "zheu-system.firebasestorage.app",
  messagingSenderId: "687928237913",
  appId: "1:687928237913:web:575faec5d95a555d36f648"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
  console.log("[SW] Получено фоновое сообщение: ", payload);
  
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: "/favicon.ico" 
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});