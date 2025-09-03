# backend/app/tuils/sub_encoder.py

"""
    This is util funtion to basically convert user_input to model_input schema. As Machine input format is not convient to take as input 
    as we are also providing API features , we can't as user to input in modle format as in training model were trained for better acuracy etc.
    Their even time is in minute and our model don't even take date as input but 

"""

from app.schemas import input_model,ml_model_input
from datetime import datetime
def sub_encoder(user_input:input_model) -> ml_model_input:
    """
    Takes user input (input_model), encodes fields needed for the ML model,
    feeds them to the model, and returns a Pydantic ml_model_input object.
    """

    dt = datetime.strptime(user_input.DATE,"%Y-%m-%d")
    dept_time_obj = datetime.strptime(user_input.DEPARTURE_TIME,"%H:%M") 
    arvl_time_obj = datetime.strptime(user_input.ARRIVAL_TIME, "%H:%M")

    return ml_model_input(
        MONTH=dt.month,
        DAY_OF_WEEK=dt.isoweekday(),
        AIRLINE=user_input.AIRLINE,
        DEPARTURE_TIME=(dept_time_obj.hour * 60 + dept_time_obj.minute),
        ARRIVAL_TIME=(arvl_time_obj.hour*60 + arvl_time_obj.minute),
        ORIGIN_STATE=user_input.ORIGIN_STATE,
        DESTINATION_STATE=user_input.DESTINATION_STATE,
        DEPARTURE_DELAY=user_input.DEPARTURE_DELAY,
    )