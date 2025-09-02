from pydantic import BaseModel,Field

class Input(BaseModel):
    MONTH: int = Field(...,gt=0,description="Month of the Flight Schedule")
    DAY_OF_WEEK: int = Field(...,gt=0,description="Day of the week of flight schedules, considering monday as 1")
    AIRLINE: str = Field(...,description="Airline Code like AA, AB etc")
    DEPARTURE_TIME: int = Field(...,ge=0,description="Times in minutes of leaving origin state")
    ARRIVAL_TIME: int = Field(...,ge=0,description="Times in minutes of arrival at destination")
    ORIGIN_STATE: str = Field(...,description="State code from where the flight is scheduled to leave")
    DESTINATION_STATE: str = Field(...,description="Destination state code")
    DEPARTURE_DELAY: float = Field(...,ge=0.0,description="Avg departure delay caused by airline")
