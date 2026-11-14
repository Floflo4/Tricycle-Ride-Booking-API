from flask import request


def register_create_route(app, rides):

    @app.route("/api/rides", methods=["POST"])
    def create_ride():
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return {
                "error": "Invalid ride booking information"
            }, 400

        required_fields = [
            "passenger_name",
            "pickup_location",
            "destination",
            "fare"
        ]

        for field in required_fields:
            if field not in data:
                return {
                    "error": "Invalid ride booking information"
                }, 400

            if data[field] is None or data[field] == "":
                return {
                    "error": "Invalid ride booking information"
                }, 400

        try:
            fare = float(data["fare"])
        except (TypeError, ValueError):
            return {
                "error": "Invalid ride booking information"
            }, 400

        if fare <= 0:
            return {
                "error": "Invalid ride booking information"
            }, 400

        new_id = max(
            [ride["id"] for ride in rides],
            default=0
        ) + 1

        new_ride = {
            "id": new_id,
            "passenger_name": data["passenger_name"],
            "pickup_location": data["pickup_location"],
            "destination": data["destination"],
            "fare": fare,
            "status": data.get("status", "Pending")
        }

        rides.append(new_ride)

        return {
            "message": "Ride booked successfully",
            "id": new_id
        }, 201