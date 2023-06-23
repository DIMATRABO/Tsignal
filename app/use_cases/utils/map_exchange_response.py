from datetime import datetime



def map_data(order , response ):
        if not response is None:
            order.response  =  str(response) 
            if "id" in response:
                order.execution_id = response['id'] 
            else:
                order.execution_id = None
            
            if "status" in response:
                order.status = response['status'] 
            else:
                order.status = 'failed'

            if "average" in response:
                order.execution_price = response['average'] 
            else:
                order.execution_price = None

            if "datetime" in response:
                order.execution_date = datetime.now() if response['datetime'] == None else datetime.strptime(response["datetime"], "%Y-%m-%dT%H:%M:%S.%fZ")
            else:
                 order.execution_date = datetime.now()

        return order