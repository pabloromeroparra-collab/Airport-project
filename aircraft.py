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

            valid = True

            try:

                time_parts = time.split(":")

                if len(time_parts) != 2:

                    valid = False

                else:

                    hour = int(time_parts[0])

                    minute = int(time_parts[1])

                    if hour < 0 or hour > 23:
                        valid = False

                    if minute < 0 or minute > 59:
                        valid = False

            except:

                valid = False

            if valid:
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

        parts = time.split(":")

        hour = int(parts[0])

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

        parts = time.split(":")

        hour = int(parts[0])

        hours[hour] += 1

        i += 1

    widgets = frame.winfo_children()

    i = 0

    while i < len(widgets):
        widgets[i].destroy()

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
def MapFlights(aircrafts, airports):

    ExportFlightsKML(
        aircrafts,
        airports,
        "OUTPUTS/flights.kml"
    )

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

    widgets = frame.winfo_children()

    i = 0

    while i < len(widgets):
        widgets[i].destroy()

        i += 1

    fig = Figure(figsize=(12, 6))

    ax = fig.add_subplot(111)

    ax.bar(airlines, counts)

    ax.set_title("Flights per airline")

    ax.set_xlabel("Airlines")

    ax.set_ylabel("Flights")

    ax.tick_params(
        axis="x",
        labelrotation=90,
        labelsize=6
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

                if IsSchengenAirport(aircraft.origin):

                    schengen_counts[j] += 1

                else:

                    non_schengen_counts[j] += 1

                found = True

            j += 1

        if not found:

            airlines.append(airline)

            if IsSchengenAirport(aircraft.origin):

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

def PlotFlightsTypeTk(frame, aircrafts):

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

        while j < len(airlines) and found == False:

            if airlines[j] == airline:

                if IsSchengenAirport(
                    aircraft.origin
                ):

                    schengen_counts[j] = (
                        schengen_counts[j] + 1
                    )

                else:

                    non_schengen_counts[j] = (
                        non_schengen_counts[j] + 1
                    )

                found = True

            j = j + 1

        if found == False:

            airlines.append(airline)

            if IsSchengenAirport(
                aircraft.origin
            ):

                schengen_counts.append(1)

                non_schengen_counts.append(0)

            else:

                schengen_counts.append(0)

                non_schengen_counts.append(1)

        i = i + 1

    widgets = frame.winfo_children()

    i = 0

    while i < len(widgets):

        widgets[i].destroy()

        i = i + 1

    fig = Figure(figsize=(10, 5))

    ax = fig.add_subplot(111)

    ax.bar(
        airlines,
        schengen_counts,
        label="Schengen"
    )

    ax.bar(
        airlines,
        non_schengen_counts,
        bottom=schengen_counts,
        label="Non-Schengen"
    )

    ax.set_title(
        "Flight Types"
    )

    ax.set_xlabel(
        "Airlines"
    )

    ax.set_ylabel(
        "Flights"
    )

    ax.tick_params(
        axis="x",
        labelrotation=90,
        labelsize=6
    )

    ax.legend()

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(
        fig,
        master=frame
    )

    canvas.draw()

    canvas.get_tk_widget().pack()

def MapFlightsTk(frame,aircrafts,airports):

    coords = AirportCoords(airports)

    widgets = frame.winfo_children()

    i = 0

    while i < len(widgets):

        widgets[i].destroy()

        i = i + 1

    fig = Figure(figsize=(12, 6))

    ax = fig.add_subplot(111)
    ax.set_facecolor("lightblue")

    fig.patch.set_facecolor("white")

    destination_lat = 41.2974

    destination_lon = 2.0833

    i = 0

    while i < len(aircrafts):

        aircraft = aircrafts[i]

        found = False

        keys = list(coords.keys())

        j = 0

        while j < len(keys) and found == False:

            if keys[j] == aircraft.origin:

                found = True

            else:

                j = j + 1

        if found:

            origin = coords[
                aircraft.origin
            ]

            origin_lat = origin[0]

            origin_lon = origin[1]

            ax.plot(
                [origin_lon, destination_lon],
                [origin_lat, destination_lat],
                linewidth=0.5
            )

            ax.plot(
                origin_lon,
                origin_lat,
                marker="o"
            )

            ax.text(
                origin_lon + 1,
                origin_lat + 1,
                aircraft.origin,
                fontsize=6
            )

        i = i + 1

    ax.plot(
        destination_lon,
        destination_lat,
        marker="o",
        color="red",
        markersize=8
    )

    ax.text(
        destination_lon + 1,
        destination_lat + 1,
        "LEBL",
        fontsize=7
    )

    ax.set_xlim(-180, 180)

    ax.set_ylim(-90, 90)

    ax.set_title(
        "Flights to Barcelona"
    )

    ax.set_xlabel(
        "Longitude"
    )

    ax.set_ylabel(
        "Latitude"
    )

    ax.grid(True)

    canvas = FigureCanvasTkAgg(
        fig,
        master=frame
    )

    canvas.draw()

    canvas.get_tk_widget().pack()

# --------------------------------------------------
# TEST SECTION
# --------------------------------------------------

if __name__ == "__main__":

    aircrafts = LoadArrivals("DATA/arrivals.txt")

    print("Loaded:", len(aircrafts), "aircraft")

    PlotArrivals(aircrafts)

    PlotAirlines(aircrafts)