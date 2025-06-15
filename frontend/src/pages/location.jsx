// components/LocationSender.js
import React, { useEffect } from "react";

const LocationSender = () => {
  useEffect(() => {
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(async (position) => {
        const { latitude, longitude } = position.coords;

        // Send to Django backend
        try {
          await fetch("http://localhost:8000/api/location/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              // If you use authentication, include token here
            },
            body: JSON.stringify({ latitude, longitude }),
          });
          console.log("Location sent successfully");
        } catch (err) {
          console.error("Error sending location:", err);
        }
      });
    } else {
      console.log("Geolocation not supported");
    }
  }, []);

  return <div>Getting your location...</div>;
};

export default LocationSender;
