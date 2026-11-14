import requests

BASE_URL = "http://127.0.0.1:5000/api/rides"

results = []


def show_result(operation, response):
    print(f"\n{operation}")
    print("Status Code:", response.status_code)

    try:
        print("Response:", response.json())
    except ValueError:
        print("Response:", response.text)

    results.append(
        (operation, response.status_code)
    )


def main():
    print("====================================")
    print(" TRICYCLE RIDE BOOKING API CONSUMER")
    print("====================================")

    # 1. GET all rides
    try:
        response = requests.get(BASE_URL, timeout=5)
        show_result("GET ALL RIDES", response)

        # 2. GET ride by ID
        response = requests.get(
            f"{BASE_URL}/1",
            timeout=5
        )
        show_result("GET RIDE BY ID", response)

        # 3. POST: Create a new ride
        new_ride = {
            "passenger_name": "Maria Santos",
            "pickup_location": "Mabalacat City College",
            "destination": "Dau Terminal",
            "fare": 50.00,
            "status": "Pending"
        }

        response = requests.post(
            BASE_URL,
            json=new_ride,
            timeout=5
        )
        show_result("CREATE NEW RIDE", response)

        # Get the new ride ID from the response
        new_ride_id = None

        if response.status_code == 201:
            new_ride_id = response.json().get("id")

        if new_ride_id is not None:

            # 4. PUT: Update the newly created ride
            updated_ride = {
                "passenger_name": "Maria Santos",
                "pickup_location": "Mabalacat City College",
                "destination": "Clark Freeport Zone",
                "fare": 100.00,
                "status": "Confirmed"
            }

            response = requests.put(
                f"{BASE_URL}/{new_ride_id}",
                json=updated_ride,
                timeout=5
            )
            show_result("UPDATE RIDE", response)

            # 5. DELETE: Cancel the ride
            response = requests.delete(
                f"{BASE_URL}/{new_ride_id}",
                timeout=5
            )
            show_result("CANCEL RIDE", response)

        else:
            print("\nSkipping PUT and DELETE because ride creation failed.")

        # 6. Error handling: Request a nonexistent ride
        response = requests.get(
            f"{BASE_URL}/99999",
            timeout=5
        )
        show_result("TEST ERROR: NONEXISTENT RIDE", response)

    except requests.exceptions.ConnectionError:
        print("\nERROR: Cannot connect to the API.")
        print("Make sure app.py is running first.")

    except requests.exceptions.Timeout:
        print("\nERROR: The API request timed out.")

    except requests.exceptions.RequestException as error:
        print("\nREQUEST ERROR:", error)

    # Summary report
    print("\n====================================")
    print("           SUMMARY REPORT")
    print("====================================")

    successful = 0
    failed = 0

    for operation, status_code in results:
        passed = 200 <= status_code < 300

        if passed or (
            operation == "TEST ERROR: NONEXISTENT RIDE"
            and status_code == 404
        ):
            successful += 1
            status = "PASS"
        else:
            failed += 1
            status = "FAIL"

        print(f"{operation}: {status} ({status_code})")

    print("------------------------------------")
    print("Successful tests:", successful)
    print("Failed tests:", failed)
    print("Total tests:", len(results))
    print("====================================")


if __name__ == "__main__":
    main()