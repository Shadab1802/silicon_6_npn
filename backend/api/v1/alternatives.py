#backend/api/v1/aternatives.py

"""
This route is for responding alternatives for a predicted delay flight.

Uses ExternalAPI(Aviation stack) to fetch scheduled flights from origin state (any airport) to destination state(any airport)

as on free tier of api no parameter passing is allowed. so some processing is made here.(sorted in ascending order of arrival time) 

as user input is in perticular format to maintain uniformality across whole api calling process, some preprocessing is required before calling external api

here we mapped the states to their coresponding airport from states_airport.json and then call api for one-to-one mapping of airport corresponding to each state 

output is : {"total_flights": len(all_flights), "flights": all_flights}

"""
from app.schemas.input_model import Input ## user input module
from fastapi import APIRouter
from app.services.aviation_stack_api import AviationStackAPI
import json

#creating router instance
router = APIRouter()
avi_api = AviationStackAPI()


with open("states_airport.json") as f:
    states_airport = json.load(f)

@router.post("/alternatives")
def alternatives(input: Input):
    origin_state = input.ORIGIN_STATE.upper()
    dest_state = input.DESTINATION_STATE.upper()

    origin_airports = states_airport.get(origin_state)
    dest_airports = states_airport.get(dest_state)

    if not origin_airports or not dest_airports:
        return {"error": "No airports found for the given states."}

    all_flights = []

    # Loop through all combinations of origin × destination airports
    for origin_airport in origin_airports:
        for dest_airport in dest_airports:
            try:
                flights_data = avi_api.get_flights(
                    dep_iata=origin_airport,
                    arr_iata=dest_airport,
                    flight_date=input.DATE,
                    # flight_status="scheduled",
                )
                # Append all flights from this API call
                all_flights.extend(flights_data.get("data", []))
            except Exception as e:
                # Optionally log errors but continue
                print(f"Error fetching flights {origin_airport} → {dest_airport}: {e}")

    # At this point, `all_flights` contains all flights from every airport combination
    # print(avi_api.get_flights(airlines="AA"))
    # Extract HH:MM (first 5 chars after T)
    all_flights["departure_scheduled"] = all_flights["departure_scheduled"].str.split("T").str[1].str[:5]
    all_flights["arrival_scheduled"] = all_flights["arrival_scheduled"].str.split("T").str[1].str[:5]

    # Sort by departure time (24-hour format)
    all_flights = all_flights.sort_values("arrival_scheduled").reset_index(drop=True)    

    return {"total_flights": len(all_flights), "flights": all_flights}

if __name__=='__main__':
    print(alternatives(Input(
        DATE="2025-09-02",
        AIRLINE="AA",
        DEPARTURE_TIME="13:20",
        ARRIVAL_TIME="15:20",
        ORIGIN_STATE="NY",
        DESTINATION_STATE="CT",
        DEPARTURE_DELAY="10",
    )))