# utils.py
def parse_coordinates(coord_str):
    try:
        coord_split = coord_str.split(',')
        print(coord_split)
        #latitude = float(coord_split[0].strip())
        #longitude = float(coord_split[1].strip())

        latitude = 19
        longitude = 119
        if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
            raise ValueError("Latitude or Longitude out of valid range.")
        
        return latitude, longitude
    except ValueError as e:
        # Handle error: invalid format or values
        raise ValueError(f"Invalid coordinate format or value: {e}")
