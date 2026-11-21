from flask import Flask

from get_rides import register_get_routes
from create_ride import register_create_route

app = Flask(__name__)

# Temporary in-memory ride records
rides = [
    {
        "id": 1,
        "passenger_name": "Juan Dela Cruz",
        "pickup_location": "Mabalacat City College",
        "destination": "Dau Terminal",
        "fare": 50.00,
        "status": "Pending"
    }
]

# Register routes from the other Python files
register_get_routes(app, rides)
register_create_route(app, rides)


@app.route("/")
def home():
    return {
        "message": "Tricycle Ride Booking API is running!",
        "endpoints": [
            "GET /api/rides",
            "GET /api/rides/<id>",
            "POST /api/rides"
        ]
    }, 200


if __name__ == "__main__":
    app.run(host=" ", debug=True)
