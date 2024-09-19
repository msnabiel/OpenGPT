// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth"; // Import Firebase Authentication
import { getAnalytics } from "firebase/analytics";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyD1vKhbldgVgypUiYn0EqiT0tInL_RvPFw",
  authDomain: "msnabiel.firebaseapp.com",
  projectId: "msnabiel",
  storageBucket: "msnabiel.appspot.com",
  messagingSenderId: "716212895434",
  appId: "1:716212895434:web:e9a3ee3b15243f900d7e33",
  measurementId: "G-20LVD0Y2V9"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app); // Initialize Firebase Authentication
const analytics = getAnalytics(app);

export { auth }; // Export the auth object for use in other files