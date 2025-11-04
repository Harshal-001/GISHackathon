import json

import googlemaps
import os
from dotenv import load_dotenv

load_dotenv()

def calculate_driving_distance( origin_lat, origin_lng, requestType = "police"):
    """
    Calculates the driving distance between two points using Google Maps Distance Matrix API.

    Args:
        api_key (str): Your Google Maps Platform API key.
        origin_lat (float): Latitude of the origin point.
        origin_lng (float): Longitude of the origin point.
        destination_lat (float): Latitude of the destination point.
        destination_lng (float): Longitude of the destination point.

    Returns:
        dict: A dictionary containing distance and duration information,
              or None if the request fails.
    """
    police_names = [
        "Bur Dubai Police Station",
        "Naif Police Station",
        "Al Muraqqabat Police Station",
        "Al Rashidiya Police Station",
        "Al Qusais Police Station",
        "Hatta Police Station",
        "Nad Al Sheba Police Station",
        "Jebel Ali Police Station",
        "Ports Police Station (Port Rashid area)",
        "Al Barsha Police Station",
        "Al Khawaneej Police Station"
    ]

    fire_names = [
        "Al Karama Civil Defence Station",
        "Al Rashidiya Civil Defence Station",
        "Al Qusais Civil Defence Station",
        "Al Mizhar Civil Defence Station",
        "Al Aweer Civil Defence Station",
        "Jumeirah Civil Defence Station",
        "Jebel Ali Civil Defence Station",
        "Nadd Al Shiba (Nad Al Sheba) Civil Defence Station",
        "Al Quoz Civil Defence Station",
        "Al Barsha Civil Defence Station",
        "Al Twar Civil Defence Station",
        "Hatta Civil Defence Station",
        "Expo / Expo City Civil Defence Station",
        "Al Hamriya Civil Defence Station",
        "Al Manara / Umm Suqeim Civil Defence Station"
    ]

    hospital_names = [
        "Rashid Hospital",
        "Latifa Hospital",
        "Al Jalila Children's Hospital",
        "American Hospital Dubai",
        "Mediclinic City Hospital (DHCC)",
        "Mediclinic Parkview Hospital",
        "Mediclinic Welcare Hospital (Al Garhoud)",
        "Medcare Women & Children Hospital (Sheikh Zayed Rd)",
        "Al Zahra Hospital Dubai (Al Barsha)",
        "Saudi German Hospital Dubai (Al Barsha)",
        "NMC Hospital - Deira",
        "NMC Specialist Hospital (DIP area)",
        "Zulekha Hospital Dubai (Al Qusais / Al Nahda area)",
        "Wooridul Spine Hospital (Dubai)",
        "Aster Hospital - Al Qusais"
    ]
    gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_APIKEY"))

    # Format the coordinates for the API request
    origins = f"{origin_lat},{origin_lng}"

    with open('EmergencyCenters.json', 'r') as file:
        obj = json.load(file)
    lst = []
    if (requestType == "police"):
        lst = police_names
    elif (requestType == "fire"):
        lst = fire_names
    else:
        lst = hospital_names

    ans = {}
    for i in lst:
        destinations = f"{obj[requestType][i]['lat']},{obj[requestType][i]['lng']}"
        try:
            # Request distance matrix
            matrix_result = gmaps.distance_matrix(
                origins=origins,
                destinations=destinations,
                mode="driving"
            )

            # Process the result
            if matrix_result['status'] == 'OK' and matrix_result['rows']:
                # The Distance Matrix API returns a matrix.
                # For two points, we expect one row and one element in that row.
                element = matrix_result['rows'][0]['elements'][0]

                if element['status'] == 'OK':
                    distance = element['distance']['text']
                    duration = element['duration']['text']
                    ans[i] = {
                                "distance": distance,
                                "duration": duration
                            }
                else:
                    print(f"Error calculating distance for element: {element['status']}")
                    return None
            else:
                print(f"Error in Distance Matrix request: {matrix_result['status']}")
                return None

        except googlemaps.exceptions.ApiError as e:
            print(f"Google Maps API Error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
    ans_output = json.dumps(ans, indent=4)
    return ans_output


if __name__ == "__main__":
    # --- IMPORTANT ---
    # Replace 'YOUR_API_KEY' with your actual Google Maps Platform API Key.
    # Make sure the Distance Matrix API is enabled in your Google Cloud project.
    # It's recommended to store API keys securely, e.g., using environment variables.
    # For this example, we'll put it directly here, but be cautious in production.
    # api_key = os.environ.get("GOOGLE_MAPS_API_KEY") # Recommended way

    origin_lat = 25.130839852559077
    origin_lng = 55.41718289605346

    print(f"Calculating driving distance from ({origin_lat}, {origin_lng}) to ...")
    distance_info = calculate_driving_distance(
        origin_lat, origin_lng, 'fire'
    )

    if distance_info:
        print("\n--- Distance Matrix Result ---")
        print(distance_info)
    else:
        print("Failed to retrieve distance information.")
