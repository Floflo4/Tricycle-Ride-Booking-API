def register_get_routes(app, rides):

    # GET all ride bookings
    @app.route("/api/rides", methods=["GET"])
    def get_all_rides():
        return rides, 200

    # GET a specific ride booking
    @app.route("/api/rides/<int:ride_id>", methods=["GET"])
    def get_ride_by_id(ride_id):
        for ride in rides:
            if ride["id"] == ride_id:
                return ride, 200

        return {"error": "Ride booking not found"}, 404
