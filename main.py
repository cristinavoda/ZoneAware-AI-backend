from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
from math import radians, sin, cos, sqrt, atan2


from math import radians, sin, cos, sqrt, atan2

def calculate_distance(p1, p2):
    """
    Calcula distancia en metros entre dos puntos lat/lon
    usando fórmula Haversine
    """
    if p1["lat"] is None or p2["lat"] is None:
        return 0

    R = 6371000  

    lat1 = radians(p1["lat"])
    lon1 = radians(p1["lon"])
    lat2 = radians(p2["lat"])
    lon2 = radians(p2["lon"])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))  



load_dotenv(dotenv_path=".env/.env")

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

if not RAPIDAPI_KEY:
    raise ValueError("RAPIDAPI_KEY no está definida")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "network-as-code.p.rapidapi.com"
}


@app.get("/geofencing-list")
def get_geofencing():
    url = "https://network-as-code.p.rapidapi.com/retrieveGeofencingSubscriptionList"
    response = requests.get(url, headers=HEADERS)
    return response.json()

@app.get("/device-location/{phone_number}")
def get_device_location(phone_number: str):
    url = "https://network-as-code.p.rapidapi.com/device-location"
    params = {"phoneNumber": phone_number}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

drones = [
   {"id": "DRONE-01", "status": "ACTIVE", "lat": 0.0, "lon": 0.0},
    {"id": "DRONE-02", "status": "ACTIVE", "lat": 0.0, "lon": 0.0},
    {"id": "DRONE-03", "status": "STANDBY", "lat": 0.0, "lon": 0.0}, 
]




def evaluate_proximity():
    alerts = []

    for i in range(len(drones)):
        for j in range(i + 1, len(drones)):
            distance = calculate_distance(drones[i], drones[j])

            if distance < 50:  
                alerts.append({
                    "drone1": drones[i]["id"],
                    "drone2": drones[j]["id"],
                    "distance": distance
                })

    return alerts
GEOFENCE_CENTER = {"lat": 41.3874, "lon": 2.1686}  
GEOFENCE_RADIUS = 300  
def check_geofence(drone):
    distance = calculate_distance(drone, GEOFENCE_CENTER)
    return distance < GEOFENCE_RADIUS
