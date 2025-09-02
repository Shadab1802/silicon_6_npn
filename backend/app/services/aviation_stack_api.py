import requests
from dotenv import load_dotenv
import os

load_dotenv() 
class AviationStackAPI:
    BASE_URL = "https://api.aviationstack.com/v1/"

    def __init__(self):
        # Get API key from .env; assign None if not found
        self.api_key = os.getenv("AVIATIONSTACK_API_KEY", None)

    def get_flights(self, **kwargs):
        """
        Fetch flights from AviationStack API.

        Only includes parameters that are not None.
        Example parameters: airline_iata, flight_date, dep_iata, arr_iata, dep_time_from, dep_time_to
        """
        params = {"access_key": self.api_key}

        # Include only non-None parameters
        params.update({k: v for k, v in kwargs.items() if v is not None})

        url = f"{self.BASE_URL}flights"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e} (status {e.response.status_code})")
            raise
    
        return response.json()