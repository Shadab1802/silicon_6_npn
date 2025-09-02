from pydantic import BaseModel,Field

class Input(BaseModel):
    DATE: str = Field(...,description="Date of flight (YYYY-MM-DD)")
    AIRLINE: str = Field(...,description="Airline Code like AA, AB etc")
    DEPARTURE_TIME: str = Field(...,description="Times in 24hr format (HH:MM) of leaving origin state")
    ARRIVAL_TIME: str = Field(...,description="Times in 24hr format (HH:MM) of arrival at destination")
    ORIGIN_STATE: str = Field(...,description="State code from where the flight is scheduled to leave")
    DESTINATION_STATE: str = Field(...,description="Destination state code")
    DEPARTURE_DELAY: float = Field(...,ge=0.0,description="Avg departure delay caused by airline")