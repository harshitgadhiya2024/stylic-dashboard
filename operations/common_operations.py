import uuid
from datetime import datetime

class commonOperation():


    def __init__(self):
        pass

    # get current utc timestamp
    def get_timestamp(self):
        try:
            current_datetime = datetime.utcnow()
            formatted_datetime = current_datetime.strftime("%m-%d-%Y %H:%M:%S")

            return formatted_datetime

        except Exception as e:
            print(f"{datetime.utcnow()}: Error when get timestamp: {e}")

    # generate unique id
    def generate_unique_id(self):
        try:
            unique_id = str(uuid.uuid4())
            return unique_id

        except Exception as e:
            print(f"{datetime.utcnow()}: Error in generating unique id: {e}")

