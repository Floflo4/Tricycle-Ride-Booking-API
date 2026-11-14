from flask import request


def register_manage_routes(app, rides):

    # PUT: Update an existing ride
    @app.route("/api/rides/<int:ride_id>", methods=["PUT"])
    def update_ride(ride_id):
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return {
                "error": "Invalid ride booking information"
            }, 400

        required_fields = [
            "passenger_name",
            "pickup_location",
            "destination",
            "fare",
            "status"
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

        for ride in rides:
            if ride["id"] == ride_id:
                ride["passenger_name"] = data["passenger_name"]
                ride["pickup_location"] = data["pickup_location"]
                ride["destination"] = data["destination"]
                ride["fare"] = fare
                ride["status"] = data["status"]

                return {
                    "message": "Ride booking updated successfully"
                }, 200

        return {
            "error": "Ride booking not found"
        }, 404

    # DELETE: Cancel a ride booking
    @app.route("/api/rides/<int:ride_id>", methods=["DELETE"])
    def cancel_ride(ride_id):
        for ride in rides:
            if ride["id"] == ride_id:
                ride["status"] = "Cancelled"

                return {
                    "message": "Ride booking cancelled successfully"
                }, 200

        return {
            "error": "Ride booking not found"
        }, 404