import googlemaps
import os
from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

def calculate_driving_distance( origin_lat, origin_lng, destination_lat, destination_lng):
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
    gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_APIKEY"))

    # Format the coordinates for the API request
    origins = f"{origin_lat},{origin_lng}"
    destinations = f"{destination_lat},{destination_lng}"

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
                return {
                    "distance": distance,
                    "duration": duration,
                    "raw_distance_value": element['distance']['value'], # distance in meters
                    "raw_duration_value": element['duration']['value']  # duration in seconds
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

def call_agent():
    agent = create_agent(
        model="claude-sonnet-4-5-20250929",
        tools=[calculate_driving_distance],
        system_prompt="You are a helpful assistant",
    )
