
from flask import Flask, request, jsonify

app = Flask(__name__)

# Temporary in-memory ride booking records
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

next_id = 2

# Required fields
required_fields = [
    "passenger_name",
    "pickup_location",
    "destination",
    "fare"
]

allowed_statuses = [
    "Pending",
    "Confirmed",
    "Completed",
    "Cancelled"
]


def validate_ride(data):
    if not isinstance(data, dict):
        return False

    for field in required_fields:
        if field not in data:
            return False

        if field != "fare":
            if not isinstance(data[field], str) or not data[field].strip():
                return False

    try:
        fare = float(data["fare"])
        if fare <= 0:
            return False
    except (ValueError, TypeError):
        return False

    if "status" in data:
        if data["status"] not in allowed_statuses:
            return False

    return True


# 1. GET ALL RIDES
@app.route("/api/rides", methods=["GET"])
def get_rides():
    return jsonify(rides), 200


# 2. GET RIDE BY ID
@app.route("/api/rides/<int:ride_id>", methods=["GET"])
def get_ride(ride_id):
    for ride in rides:
        if ride["id"] == ride_id:
            return jsonify(ride), 200

    return jsonify({"error": "Ride booking not found"}), 404


# 3. CREATE A RIDE BOOKING
@app.route("/api/rides", methods=["POST"])
def create_ride():
    global next_id

    data = request.get_json(silent=True)

    if not validate_ride(data):
        return jsonify({
            "error": "Invalid ride booking information"
        }), 400

    new_ride = {
        "id": next_id,
        "passenger_name": data["passenger_name"].strip(),
        "pickup_location": data["pickup_location"].strip(),
        "destination": data["destination"].strip(),
        "fare": float(data["fare"]),
        "status": data.get("status", "Pending")
    }

    rides.append(new_ride)

    next_id += 1

    return jsonify({
        "message": "Ride booked successfully",
        "id": new_ride["id"]
    }), 201


# 4. UPDATE A RIDE BOOKING
@app.route("/api/rides/<int:ride_id>", methods=["PUT"])
def update_ride(ride_id):
    data = request.get_json(silent=True)

    if not validate_ride(data):
        return jsonify({
            "error": "Invalid ride booking information"
        }), 400

    for ride in rides:
        if ride["id"] == ride_id:
            ride["passenger_name"] = data["passenger_name"].strip()
            ride["pickup_location"] = data["pickup_location"].strip()
            ride["destination"] = data["destination"].strip()
            ride["fare"] = float(data["fare"])
            ride["status"] = data.get("status", "Pending")

            return jsonify({
                "message": "Ride booking updated successfully"
            }), 200

    return jsonify({
        "error": "Ride booking not found"
    }), 404


# 5. CANCEL A RIDE BOOKING
@app.route("/api/rides/<int:ride_id>", methods=["DELETE"])
def cancel_ride(ride_id):
    for ride in rides:
        if ride["id"] == ride_id:
            ride["status"] = "Cancelled"

            return jsonify({
                "message": "Ride booking cancelled successfully"
            }), 200

    return jsonify({
        "error": "Ride booking not found"
    }), 404


if __name__ == "__main__":
    app.run(debug=True)
