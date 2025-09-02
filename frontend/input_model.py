from pydantic import BaseModel,Field

class Input(BaseModel):
    DATE: int = Field(...,gt=0,description="Flight Schedule date")
    AIRLINE: str = Field(...,description="Airline Code like AA, AB etc")
    DEPARTURE_TIME: int = Field(...,ge=0,description="Times in minutes of leaving origin state")
    ARRIVAL_TIME: int = Field(...,ge=0,description="Times in minutes of arrival at destination")
    ORIGIN_STATE: str = Field(...,description="State code from where the flight is scheduled to leave")
    DESTINATION_STATE: str = Field(...,description="Destination state code")
    DEPARTURE_DELAY: float = Field(...,ge=0.0,description="Avg departure delay caused by airline")