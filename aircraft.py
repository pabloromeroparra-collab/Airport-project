import math
import matplotlib.pyplot as plt
from airport import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# --------------------------------------------------
# CLASS
# --------------------------------------------------

class Aircraft:
    def __init__(self, aircraft_id, company, origin, time_landing):
        self.aircraft_id = aircraft_id
        self.company = company
        self.origin = origin
        self.time_landing = time_landing


# --------------------------------------------------
# LOAD ARRIVALS
# --------------------------------------------------

def LoadArrivals(filename):

    aircrafts = []

    try:
        file = open(filename, "r")
    except:
        return []

    file.readline()  # skip header
    line = file.readline()

    while line != "":

        parts = line.split()

        if len(parts) >= 4:

            aircraft_id = parts[0]
            origin = parts[1]
            time = parts[2]
            company = parts[3]

            aircraft = Aircraft(aircraft_id, company, origin, time)
            aircrafts.append(aircraft)

        line = file.readline()

    file.close()
    return aircrafts


# --------------------------------------------------
# PLOT ARRIVALS (NORMAL)
# --------------------------------------------------

def PlotArrivals(aircrafts):

    if len(aircrafts) == 0:
        print("Empty aircraft list")
        return

    hours = [0] * 24

    i = 0
    while i < len(aircrafts):

        time = aircrafts[i].time_landing
        hour = int(time[0:2])

        hours[hour] += 1
        i += 1

    x = []
    i = 0
    while i < 24:
        x.append(i)
        i += 1

    plt.bar(x, hours)
    plt.xlabel("Hour")
    plt.ylabel("Flights")
    plt.title("Arrivals per hour")
    plt.show()


# --------------------------------------------------
# TKINTER PLOT ARRIVALS
# --------------------------------------------------

def PlotArrivalsTk(frame, aircrafts):

    if len(aircrafts) == 0:
        print("Empty aircraft list")
        return

    hours = [0] * 24

    i = 0
    while i < len(aircrafts):
        time = aircrafts[i].time_landing
        hour = int(time[0:2])
        hours[hour] += 1
        i += 1

    # limpiar frame
    for widget in frame.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(6,4))
    ax = fig.add_subplot(111)

    x = []
    i = 0
    while i < 24:
        x.append(i)
        i += 1

    ax.bar(x, hours)
    ax.set_title("Arrivals per hour")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Flights")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# --------------------------------------------------
# SAVE FLIGHTS
# --------------------------------------------------

def SaveFlights(aircrafts, filename):

    if len(aircrafts) == 0:
        return -1

    file = open(filename, "w")

    i = 0
    while i < len(aircrafts):

        ac = aircrafts[i]
        line = ac.aircraft_id + " " + ac.origin + " " + ac.time_landing + " " + ac.company

        file.write(line + "\n")
        i += 1

    file.close()
    return 0

# --------------------------------------------------
# PLOT AIRLINES
# --------------------------------------------------
def PlotAirlines(aircrafts):

    if len(aircrafts) == 0:
        print("Empty aircraft list")
        return

    airlines = []
    counts = []

    i = 0
    while i < len(aircrafts):

        company = aircrafts[i].company

        found = False
        j = 0

        while j < len(airlines) and not found:
            if airlines[j] == company:
                counts[j] += 1
                found = True
            j += 1

        if not found:
            airlines.append(company)
            counts.append(1)

        i += 1

    plt.bar(airlines, counts)
    plt.title("Flights per airline")
    plt.show()


# --------------------------------------------------
# TKINTER PLOT AIRLINES
# --------------------------------------------------

def PlotAirlinesTk(frame, aircrafts):

    if len(aircrafts) == 0:
        print("Empty aircraft list")
        return

    airlines = []
    counts = []

    i = 0
    while i < len(aircrafts):

        comp = aircrafts[i].company

        found = False
        j = 0

        while j < len(airlines) and not found:
            if airlines[j] == comp:
                counts[j] += 1
                found = True
            j += 1

        if not found:
            airlines.append(comp)
            counts.append(1)

        i += 1

    # limpiar frame
    for widget in frame.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(6,4))
    ax = fig.add_subplot(111)

    ax.bar(airlines, counts)
    ax.set_title("Flights per airline")

    # etiquetas legibles
    ax.set_xticklabels(airlines, rotation=45, ha="right")

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# --------------------------------------------------
# PLOT FLIGHTS TYPE
# --------------------------------------------------
def PlotFlightsType(aircrafts):
    if len(aircrafts)==0:
        print("Empty aircraft list")
        return

    contador_schengen=[]
    contador_no_schengen=[]
    for aircraft in aircrafts:
        airline= aircraft.company
        if airline not in contador_schengen:
            contador_schengen[airline]=0
            contador_no_schengen[airline]=0

        if aircraft.origin in schengen:
            contador_schengen[aircraft.origin]= contador_schengen[aircraft.origin]+1
        else:
            contador_no_schengen[aircraft.origin]= contador_no_schengen[aircraft.origin]+1

    airlines = list(contador_schengen.keys())
    schengen_valores = list(contador_schengen.values())
    no_schengen_valores = list(contador_no_schengen.values())

    plt.bar(airlines, schengen_valores, label="Schengen")
    plt.bar(airlines, no_schengen_valores, bottom=schengen_valores, label="Non-Schengen")
    plt.title("Schengen vs Non-Schengen flights")
    plt.xlabel("Airline")
    plt.ylabel("Number of flights")
    plt.legend()
    plt.show()                                                     # final part Martí

# --------------------------------------------------
# PLOT MAP
# --------------------------------------------------
def MapFlights(aircrafts):
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
# --------------------------------------------------
# HAVERSINE
# --------------------------------------------------

def haversine(lat1, lon1, lat2, lon2):

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon/2)**2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return 6371 * c


# --------------------------------------------------
# LONG DISTANCE
# --------------------------------------------------

def LongDistanceArrivals(aircrafts, airports):

    result = []

    i = 0
    while i < len(aircrafts):

        ac = aircrafts[i]

        origin_coords = None
        j = 0
        found=False
        while j < len(airports) and not found:
            if airports[j].ICAO == ac.origin:
                origin_coords = airports[j].ICAO
                found= True
            j += 1

        if origin_coords != None:

            distance = haversine(origin_coords.latitude,
                                 origin_coords.longitude,
                                 41.2974, 2.0833)

            if distance > 2000:
                result.append(ac)

        i += 1

    return result

# --------------------------------------------------
# TEST SECTION
# --------------------------------------------------

if __name__ == "__main__":

    aircrafts = LoadArrivals("Arrivals.txt")

    print("Loaded:", len(aircrafts), "aircraft")

    PlotArrivals(aircrafts)
    PlotAirlines(aircrafts)
