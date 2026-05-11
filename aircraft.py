import math
import matplotlib.pyplot as plt
from airport import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# --------------------------------------------------
# CLASS
# --------------------------------------------------

class Aircraft:

    """
    Aircraft class.

    Parameters:
        aircraft_id (str)
        company (str)
        origin (str)
        time_landing (str)

    Returns:
        Aircraft object
    """

    def __init__(self, aircraft_id, company, origin, time_landing):

        self.aircraft_id = aircraft_id
        self.company = company
        self.origin = origin
        self.time_landing = time_landing


# --------------------------------------------------
# LOAD ARRIVALS
# --------------------------------------------------

def LoadArrivals(filename):

    """
    Loads aircraft arrivals from a text file.

    Parameters:
        filename (str)

    Returns:
        list
    """

    aircrafts = []

    try:

        file = open(filename, "r")

    except:

        return []

    file.readline()

    line = file.readline()

    while line != "":

        parts = line.split()

        if len(parts) >= 4:

            aircraft_id = parts[0]

            origin = parts[1]

            time = parts[2]

            company = parts[3]

            aircraft = Aircraft(
                aircraft_id,
                company,
                origin,
                time
            )

            aircrafts.append(aircraft)

        line = file.readline()

    file.close()

    return aircrafts


# --------------------------------------------------
# PLOT ARRIVALS
# --------------------------------------------------

def PlotArrivals(aircrafts):

    """
    Creates a plot of arrivals per hour.

    Parameters:
        aircrafts (list)

    Returns:
        None
    """

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

    """
    Creates a Tkinter plot of arrivals per hour.

    Parameters:
        frame
        aircrafts (list)

    Returns:
        None
    """

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

    i = 0

    while i < len(frame.winfo_children()):

        frame.winfo_children()[i].destroy()

        i += 1

    fig = Figure(figsize=(6, 4))

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

    """
    Saves flights into a text file.

    Parameters:
        aircrafts (list)
        filename (str)

    Returns:
        int
    """

    if len(aircrafts) == 0:

        return -1

    file = open(filename, "w")

    i = 0

    while i < len(aircrafts):

        ac = aircrafts[i]

        line = ac.aircraft_id + " "

        line += ac.origin + " "

        line += ac.time_landing + " "

        line += ac.company

        file.write(line + "\n")

        i += 1

    file.close()

    return 0


# --------------------------------------------------
# PLOT AIRLINES
# --------------------------------------------------

def PlotAirlines(aircrafts):

    """
    Creates a plot with flights per airline.

    Parameters:
        aircrafts (list)

    Returns:
        None
    """

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

    plt.figure(figsize=(12, 6))

    plt.bar(airlines, counts)

    plt.title("Flights per airline")

    plt.xlabel("Airlines")

    plt.ylabel("Flights")

    plt.xticks(rotation=90, fontsize=6)

    plt.tight_layout()

    plt.show()


# --------------------------------------------------
# TKINTER PLOT AIRLINES
# --------------------------------------------------

def PlotAirlinesTk(frame, aircrafts):

    """
    Creates a Tkinter plot with flights per airline.

    Parameters:
        frame
        aircrafts (list)

    Returns:
        None
    """

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

    i = 0

    while i < len(frame.winfo_children()):

        frame.winfo_children()[i].destroy()

        i += 1

    fig = Figure(figsize=(12, 6))

    ax = fig.add_subplot(111)

    ax.bar(airlines, counts)

    ax.set_title("Flights per airline")

    ax.set_xlabel("Airlines")

    ax.set_ylabel("Flights")

    ax.set_xticklabels(
        airlines,
        rotation=90,
        fontsize=6
    )

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame)

    canvas.draw()

    canvas.get_tk_widget().pack()


# --------------------------------------------------
# PLOT FLIGHTS TYPE
# --------------------------------------------------

def PlotFlightsType(aircrafts):

    """
    Creates a plot comparing Schengen
    and Non-Schengen flights.

    Parameters:
        aircrafts (list)

    Returns:
        None
    """

    if len(aircrafts) == 0:

        print("Empty aircraft list")

        return

    airlines = []

    schengen_counts = []

    non_schengen_counts = []

    i = 0

    while i < len(aircrafts):

        aircraft = aircrafts[i]

        airline = aircraft.company

        found = False

        j = 0

        while j < len(airlines) and not found:

            if airlines[j] == airline:

                if aircraft.origin in schengen:

                    schengen_counts[j] += 1

                else:

                    non_schengen_counts[j] += 1

                found = True

            j += 1

        if not found:

            airlines.append(airline)

            if aircraft.origin in schengen:

                schengen_counts.append(1)

                non_schengen_counts.append(0)

            else:

                schengen_counts.append(0)

                non_schengen_counts.append(1)

        i += 1

    plt.figure(figsize=(12, 6))

    plt.bar(
        airlines,
        schengen_counts,
        label="Schengen"
    )

    plt.bar(
        airlines,
        non_schengen_counts,
        bottom=schengen_counts,
        label="Non-Schengen"
    )

    plt.title("Schengen vs Non-Schengen flights")

    plt.xlabel("Airline")

    plt.ylabel("Number of flights")

    plt.xticks(rotation=90, fontsize=6)

    plt.legend()

    plt.tight_layout()

    plt.show()


# --------------------------------------------------
# PLOT MAP
# --------------------------------------------------

def MapFlights(aircrafts):

    """
    Creates a KML file with flight routes.

    Parameters:
        aircrafts (list)

    Returns:
        None
    """

    if len(aircrafts) == 0:

        print("Empty aircraft list")

        return

    file = open("flights.kml", "w")

    file.write("<?xml version='1.0' encoding='UTF-8'?>\n")

    file.write("<kml xmlns='http://www.opengis.net/kml/2.2'>\n")

    file.write("<Document>\n")

    i = 0

    while i < len(aircrafts):

        aircraft = aircrafts[i]

        if aircraft.origin in Airport_coords:

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

        i += 1

    file.write("</Document>\n")

    file.write("</kml>\n")

    file.close()

    print("KML file created: flights.kml")


# --------------------------------------------------
# HAVERSINE
# --------------------------------------------------

def haversine(lat1, lon1, lat2, lon2):

    """
    Calculates distance between two coordinates.

    Parameters:
        lat1 (float)
        lon1 (float)
        lat2 (float)
        lon2 (float)

    Returns:
        float
    """

    dlat = math.radians(lat2 - lat1)

    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) ** 2

    a += math.cos(math.radians(lat1))

    a *= math.cos(math.radians(lat2))

    a *= math.sin(dlon / 2) ** 2

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return 6371 * c


# --------------------------------------------------
# LONG DISTANCE
# --------------------------------------------------

def LongDistanceArrivals(aircrafts, airports):

    """
    Returns aircrafts with flights longer than 2000 km.

    Parameters:
        aircrafts (list)
        airports (list)

    Returns:
        list
    """

    result = []

    i = 0

    while i < len(aircrafts):

        ac = aircrafts[i]

        origin_airport = None

        j = 0

        found = False

        while j < len(airports) and not found:

            if airports[j].ICAO == ac.origin:

                origin_airport = airports[j]

                found = True

            j += 1

        if origin_airport != None:

            distance = haversine(
                origin_airport.latitude,
                origin_airport.longitude,
                41.2974,
                2.0833
            )

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
