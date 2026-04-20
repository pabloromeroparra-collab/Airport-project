import math

def LoadArrivals(filename):
    aircrafts = []

    try:
        file = open(filename)
        line = file.readline()
        last_arrival=-1
        while line != "":
            parts = line.split()
            if len(parts) >= 4:
                aircraft_code = parts[0]
                origin = parts[1]
                arrival = parts[2]
                airline = parts[3]

                time_parts=arrival.split(":")
                hour=int(time_parts[0])
                minute=int(time_parts[1])
                arrival_time=hour*60+minute


                if last_arrival <= arrival_time:
                    aircraft = Aircrafts(aircraft_code, origin, arrival, airline)
                    aircrafts.append(aircraft)
                    last_arrival = arrival_time
            line = file.readline()
        file.close()
        return aircrafts

    except FileNotFoundError:
        return []


def MapFlights(aircrafts):
    if len(aircrafts) == 0:
        print('Empty aircraft list')
        return

    file = open("flights.txt", "w")
    i = 1
    while i<len(aircrafts[i]):
        aircraft=aircrafts[i]
        coords_origin=Airport_coords[aircraft.origin]
        coords_dest=Airport_coords["LEBL"]
        lat1 = coords_origin[0]
        lon1 = coords_origin[1]

        lat2 = coords_dest[0]
        lon2 = coords_dest[1]

        if aircraft.origin in schengen:
            color = "ff0000ff"
        else:
            color = "ff00ff00"

        file.write("<Placemark>\n")

        file.write("<Style>\n")
        file.write("<LineStyle>\n")
        file.write("<color>" + color + "</color>\n")
        file.write("</LineStyle>\n")
        file.write("</Style>\n")

        file.write("<LineString>\n")
        file.write("<coordinates>\n")

        file.write(str(lon1) + "," + str(lat1) + ",0 ")
        file.write(str(lon2) + "," + str(lat2) + ",0\n")

        file.write("</coordinates>\n")
        file.write("</LineString>\n")

        file.write("</Placemark>\n")

        i = i + 1

    file.write("</Document>\n")
    file.write("</kml>\n")

    file.close()

    print("KML file created: flights.kml")

def haversine(lat1, lon1, lat2, lon2):
    dlat=math.radians(lat2-lat1)
    dlon=math.radians(lon2-lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dlon / 2) * math.sin(dlon / 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = 6371 * c

    return distance

def LongDistanceArrivals(aircrafts):
    aircrafts2000=[]
    if len(aircrafts) == 0:
        print("Empty aircraft list")
        return []

    i = 0
    while i < len(aircrafts):

        aircraft = aircrafts[i]

        coords_origin = Airport_coords[aircraft.origin]
        coords_dest = Airport_coords["LEBL"]

        lat1 = coords_origin[0]
        lon1 = coords_origin[1]

        lat2 = coords_dest[0]
        lon2 = coords_dest[1]

        distance = haversine(lat1, lon1, lat2, lon2)

        if distance > 2000:
            aircrafts2000.append(aircraft)

        i = i + 1

    return aircrafts2000
