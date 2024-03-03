import json
import requests
import redis

class NHTSAAPI:
    API_BASE_URL = "https://vpic.nhtsa.dot.gov/api/vehicles"

    def __init__(self):
        pass

    def get_vehicle_types_for_make(self, make):
        url = f"{self.API_BASE_URL}/GetVehicleTypesForMake/{make}?format=json"
        response = requests.get(url)
        data = response.json()
        return data.get("Results", [])

class RedisVehicleStorage:
    def __init__(self, redis_host="localhost", redis_port=6379, redis_db=0):
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

    def insert_vehicle_types(self, key, vehicle_types):
        serialized_data = json.dumps(vehicle_types)
        self.redis_client.set(key, serialized_data)

    def get_vehicle_types(self, key):
        serialized_data = self.redis_client.get(key)
        if serialized_data:
            return json.loads(serialized_data)
        return None


if __name__ == "__main__":
    # Instantiate NHTSAAPI
    nhtsa_api = NHTSAAPI()

    # Specify the make for which you want to get vehicle types (e.g., "merc" for Mercedes)
    make = "merc"
    vehicle_types = nhtsa_api.get_vehicle_types_for_make(make)
    print(f"Vehicle Types for {make}: {vehicle_types}")

    # Instantiate RedisVehicleStorage
    redis_storage = RedisVehicleStorage()

    # Insert vehicle types into Redis
    redis_key = f"vehicle_types_{make}"
    redis_storage.insert_vehicle_types(redis_key, vehicle_types)
    print(f"Vehicle types inserted into Redis with key '{redis_key}'")
    print("_____________________________________________")
    print("_____________________________________________")

    # Retrieve vehicle types from Redis
    retrieved_vehicle_types = redis_storage.get_vehicle_types(redis_key)
    print(f"Retrieved Vehicle Types from Redis: {retrieved_vehicle_types}")
