import math
import matplotlib.pyplot as plt

class Aircraft:                                                         # inici clase
    def __init__(self, aircraft_id, company, origin, time_landing):
        self.aircraft_id = str(aircraft_id)

        if len(company) == 3:
            self.company = company.upper()
        else:
            self.company = "?"

        if len(origin) == 4:
            self.origin = origin.upper()
        else:
            self.origin = "?"

        if len(time_landing) == 5 and time_landing[2] == ":":
            hh = time_landing[0:2]
            mm = time_landing[3:5]

            if hh.isdigit() and mm.isdigit():
                h = int(hh)
                m = int(mm)

                if 0 <= h <= 23 and 0 <= m <= 59:
                    self.time_landing = time_landing
                else:
                    self.time_landing = "00:00"
            else:
                self.time_landing = "00:00"
        else:
            self.time_landing = "00:00"

    def __str__(self):
        return f"{self.aircraft_id} {self.company} {self.origin} {self.time_landing}"      # final clase


def LoadArrivals(filename):                       # aqui comença part paula
    aircrafts = []

    try:
        file = open(filename)
        line = file.readline()
        last_arrival = -1
        while line != "":
            parts = line.split()
            if len(parts) >= 4:
                aircraft_code = parts[0]
                origin = parts[1]
                arrival = parts[2]
                airline = parts[3]

                time_parts = arrival.split(":")
                hour = int(time_parts[0])
                minute = int(time_parts[1])
                arrival_time = hour * 60 + minute

                if last_arrival <= arrival_time:
                    aircraft = Aircrafts(aircraft_code, origin, arrival, airline)
                    aircrafts.append(aircraft)
                    last_arrival = arrival_time
            line = file.readline()
        file.close()
        return aircrafts

    except FileNotFoundError:
        return []



def PlotAirlines(aircrafts):                     # inici part Martí
    if len(aircrafts) == 0:
        print("Error, empty aircraft list")
        return
    airlines=[]
    for aircraft.company in aircrafts:
        if aircraft in airlines:
            airlines[aircraft.company]  =  airlines[aircraft.company]+1
        else:
            airlines[aircraft.company] = 1

    plt.bar(airlines.keys(), airlines.values())         #grafica
    plt.title("Flights per airline")
    plt.xlabel("Airline")
    plt.ylabel("Number of flights")
    plt.show()

def PlotFlightsType(aircrafts):
    if len(aircrafts)==0:
        print("Empty aircraft list")
        return

    cont_shengen=[]
    cont_no_schengen=[]
    for aircraft in aircrafts:
        airline= aircraft.company
        if airline not in cont_shengen:
            cont_schengen[airline]=0
            cont_no_schengen[airline]=0

        if aircraft.origin in schengen:
            cont_shengen[aircraft.origin]= cont_shengen[aircraft.origin]+1
        else:
            cont_no_schengen[aircraft.origin]= cont_no_schengen[aircraft.origin]+1

    airlines = list(schengen_counts.keys())
    schengen_values = list(schengen_counts.values())
    non_schengen_values = list(non_schengen_counts.values())

    plt.bar(airlines, schengen_values, label="Schengen")
    plt.bar(airlines, non_schengen_values, bottom=schengen_values, label="Non-Schengen")
    plt.title("Schengen vs Non-Schengen flights")
    plt.xlabel("Airline")
    plt.ylabel("Number of flights")
    plt.legend()
    plt.show()                                                     # final part Martí



def MapFlights(aircrafts):                       #part Paula
    if len(aircrafts) == 0:
        print('Empty aircraft list')
        return

    file = open("flights.txt", "w")
    i = 1
    while i < len(aircrafts[i]):
        aircraft = aircrafts[i]
        coords_origin = Airport_coords[aircraft.origin]
        coords_dest = Airport_coords["LEBL"]
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
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dlon / 2) * math.sin(dlon / 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = 6371 * c

    return distance


def LongDistanceArrivals(aircrafts):
    aircrafts2000 = []
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

    return aircrafts2000                                  # fins aqui arriba part paula

#inici part pablo

def SaveFlights(aircrafts, filename):
    if not aircrafts:
        print("Error: aircraft list is empty.")
        return -1

    try:
        with open(filename, "w") as f:
            for ac in aircrafts:
                fields = [
                    ac.flight_number or "-",
                    ac.origin or "-",
                    ac.destination or "-",
                    ac.arrival_time or "-",
                    ac.airline or "-",
                    ac.status or "-",
                ]
                f.write(",".join(str(v) for v in fields) + "\n")
        return 0

    except OSError as e:
        print(f"Error: could not write to '{filename}': {e}")
        return -1

def PlotArrivals(aircrafts):
    if not aircrafts:
        print("Error: no aircraft data to display.")
        return

    hours = [ac.arrival_time.hour if hasattr(ac.arrival_time, 'hour') else int(ac.arrival_time) for ac in aircrafts]

    hour_counts = Counter(hours)
    x = list(range(24))
    y = [hour_counts.get(h, 0) for h in x]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(x, y, color="steelblue", edgecolor="white", width=0.8)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Number of landings")
    ax.set_title("Aircraft landing frequency")
    ax.set_xticks(x)
    ax.set_xticklabels([f"{h:02d}:00" for h in x], rotation=45, ha="right")
    ax.yaxis.get_major_locator().set_params(integer=True)
    plt.tight_layout()
    plt.show()