import matplotlib.pyplot as plt
<<<<<<< HEAD
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
=======
import os
import sys

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# --------------------------------------------------
# CLASS
# --------------------------------------------------

class Airport:

    """
    Airport class.

    Parameters:
        ICAO (str)
        latitude (float)
        longitude (float)

    Returns:
        Airport object
    """

    def __init__(self, ICAO, latitude, longitude):

        self.ICAO = ICAO

        self.latitude = float(latitude)

        self.longitude = float(longitude)

        self.Schengen = False


# --------------------------------------------------
# SCHENGEN
# --------------------------------------------------

def IsSchengenAirport(code):

    """
    Checks if an airport belongs
    to the Schengen area.

    Parameters:
        code (str)

    Returns:
        bool
    """

    if code == "":

        return False

    prefix = code[0:2]

    array = [
        'LO', 'EB', 'LK', 'LC', 'EK', 'EE',
        'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
        'BI', 'LI', 'EV', 'EY', 'EL', 'LM',
        'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE',
        'ES', 'LS'
    ]

    found = False

    i = 0

    while i < len(array) and found == False:

        if prefix == array[i]:

            found = True

        else:

            i = i + 1

    return found


def SetSchengen(airport):

    """
    Sets the Schengen attribute
    of an airport.

    Parameters:
        airport (Airport)

    Returns:
        bool
    """

    airport.Schengen = IsSchengenAirport(airport.ICAO)

    return airport.Schengen


# --------------------------------------------------
# PRINT
# --------------------------------------------------

def PrintAirport(airport):

    """
    Prints airport information.

    Parameters:
        airport (Airport)

    Returns:
        None
    """

    print("Code:", airport.ICAO)

    print(
        "Coordinates:",
        airport.latitude,
        ",",
        airport.longitude
    )

    print("Schengen:", airport.Schengen)


# --------------------------------------------------
# LOAD AIRPORTS
# --------------------------------------------------

def LoadAirports(filename):

    """
    Loads airports from a text file.
>>>>>>> d2d42b882792b520f895989799dc6fdedc700ec6

    Parameters:
        filename (str)

    Returns:
        list
    """

<<<<<<< HEAD
    aircrafts = []
=======
    airports = []
>>>>>>> d2d42b882792b520f895989799dc6fdedc700ec6

    try:

        file = open(filename, "r")

    except:

        return []

<<<<<<< HEAD
    file.readline()
=======
    line = file.readline()
>>>>>>> d2d42b882792b520f895989799dc6fdedc700ec6

    line = file.readline()

    while line != "":

        parts = line.split()

<<<<<<< HEAD
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

=======
        if len(parts) >= 3:

            code = parts[0]

            # LATITUDE

            coord_sign = parts[1][0]

            coord = parts[1][1:]

            deg = int(coord[0:2])

            min_ = int(coord[2:4])

            sec = int(coord[4:6])

            latitude = deg + min_ / 60 + sec / 3600

            if coord_sign == 'S':

                latitude = -latitude

            # LONGITUDE

            coord_sign = parts[2][0]

            coord = parts[2][1:]

            deg = int(coord[0:3])

            min_ = int(coord[3:5])

            sec = int(coord[5:7])

            longitude = deg + min_ / 60 + sec / 3600

            if coord_sign == 'W':

                longitude = -longitude

            airport = Airport(
                code,
                latitude,
                longitude
            )

            airports.append(airport)

>>>>>>> d2d42b882792b520f895989799dc6fdedc700ec6
        line = file.readline()

    file.close()

<<<<<<< HEAD
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
=======
    return airports


# --------------------------------------------------
# SAVE SCHENGEN
# --------------------------------------------------

def SaveSchengenAirports(airports, filename):

    """
    Saves Schengen airports into a file.

    Parameters:
        airports (list)
        filename (str)

    Returns:
        int
    """

    if len(airports) == 0:

        return -1

    file = open(filename, "w")

    file.write("CODE LAT LON\n")

    i = 0
>>>>>>> d2d42b882792b520f895989799dc6fdedc700ec6

    written = False

<<<<<<< HEAD
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
=======
    while i < len(airports):

        if airports[i].Schengen:

            latitude = airports[i].latitude

            longitude = airports[i].longitude

            # LATITUDE

            if latitude >= 0:

                lat_dir = "N"

            else:

                lat_dir = "S"

                latitude = -latitude

            lat_deg = int(latitude)

            lat_min = int((latitude - lat_deg) * 60)

            lat_sec = int(
                (
                    ((latitude - lat_deg) * 60)
                    - lat_min
                ) * 60
            )

            lat_text = (
                lat_dir
                + str(lat_deg).zfill(2)
                + str(lat_min).zfill(2)
                + str(lat_sec).zfill(2)
            )

            # LONGITUDE

            if longitude >= 0:

                lon_dir = "E"

            else:

                lon_dir = "W"

                longitude = -longitude

            lon_deg = int(longitude)

            lon_min = int((longitude - lon_deg) * 60)

            lon_sec = int(
                (
                    ((longitude - lon_deg) * 60)
                    - lon_min
                ) * 60
            )

            lon_text = (
                lon_dir
                + str(lon_deg).zfill(3)
                + str(lon_min).zfill(2)
                + str(lon_sec).zfill(2)
            )

            file.write(
                airports[i].ICAO
                + " "
                + lat_text
                + " "
                + lon_text
                + "\n"
            )

            written = True

        i = i + 1

    file.close()

    if written:

        return 0

    else:

        return -1
>>>>>>> d2d42b882792b520f895989799dc6fdedc700ec6

    i = 0

<<<<<<< HEAD
    while i < len(widgets):

        widgets[i].destroy()

        i = i + 1

    fig = Figure(figsize=(10, 5))

    ax = fig.add_subplot(111)

    ax.bar(
        airlines,
        schengen_counts,
=======
# --------------------------------------------------
# ADD / REMOVE
# --------------------------------------------------

def AddAirport(airports, airport):

    """
    Adds an airport to the list.

    Parameters:
        airports (list)
        airport (Airport)

    Returns:
        int
    """

    i = 0

    found = False

    while i < len(airports) and found == False:

        if airports[i].ICAO == airport.ICAO:

            found = True

        else:

            i = i + 1

    if found == False:

        airports.append(airport)

        return 0

    else:

        return -1


def RemoveAirport(airports, code):

    """
    Removes an airport from the list.

    Parameters:
        airports (list)
        code (str)

    Returns:
        int
    """

    i = 0

    found = False

    while i < len(airports) and found == False:

        if airports[i].ICAO == code:

            found = True

        else:

            i = i + 1

    if found:

        airports[i:i + 1] = []

        return 0

    else:

        return -1


# --------------------------------------------------
# PLOT AIRPORTS
# --------------------------------------------------

def PlotAirports(airports):

    """
    Creates a plot with Schengen
    and Non-Schengen airports.

    Parameters:
        airports (list)

    Returns:
        None
    """

    contador_schengen = 0

    contador_no_schengen = 0

    i = 0

    while i < len(airports):

        if airports[i].Schengen:

            contador_schengen = (
                contador_schengen + 1
            )

        else:

            contador_no_schengen = (
                contador_no_schengen + 1
            )

        i = i + 1

    fig, ax = plt.subplots()

    ax.bar(
        "Airports",
        contador_schengen,
>>>>>>> d2d42b882792b520f895989799dc6fdedc700ec6
        label="Schengen"
    )

    ax.bar(
<<<<<<< HEAD
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
=======
        "Airports",
        contador_no_schengen,
        bottom=contador_schengen,
        label="No Schengen"
    )

    ax.set_ylabel("Count")

    ax.set_title("Schengen Airports")

    ax.legend()

    plt.show()


# --------------------------------------------------
# PLOT AIRPORTS TKINTER
# --------------------------------------------------

def PlotAirportsTk(frame, airports):

    """
    Creates a Tkinter plot with
    Schengen and Non-Schengen airports.

    Parameters:
        frame
        airports (list)

    Returns:
        None
    """

    contador_schengen = 0

    contador_no_schengen = 0

    i = 0

    while i < len(airports):

        if airports[i].Schengen:

            contador_schengen = (
                contador_schengen + 1
            )

        else:

            contador_no_schengen = (
                contador_no_schengen + 1
            )

        i = i + 1
>>>>>>> d2d42b882792b520f895989799dc6fdedc700ec6

    widgets = frame.winfo_children()

    i = 0

    while i < len(widgets):

        widgets[i].destroy()

        i = i + 1

<<<<<<< HEAD
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
=======
    fig = Figure(figsize=(5, 4))

    ax = fig.add_subplot(111)

    ax.bar(
        ["Airports"],
        [contador_schengen],
        label="Schengen"
    )

    ax.bar(
        ["Airports"],
        [contador_no_schengen],
        bottom=[contador_schengen],
        label="No Schengen"
    )

    ax.set_ylabel("Count")

    ax.set_title("Schengen Airports")

    ax.legend()
>>>>>>> d2d42b882792b520f895989799dc6fdedc700ec6

    canvas = FigureCanvasTkAgg(
        fig,
        master=frame
    )

    canvas.draw()

    canvas.get_tk_widget().pack()

<<<<<<< HEAD
# --------------------------------------------------
# TEST SECTION
# --------------------------------------------------

if __name__ == "__main__":

    aircrafts = LoadArrivals("DATA/arrivals.txt")

    print("Loaded:", len(aircrafts), "aircraft")

    PlotArrivals(aircrafts)

    PlotAirlines(aircrafts)
=======

# --------------------------------------------------
# OPEN FILE
# --------------------------------------------------

def open_file(filename):

    """
    Opens a file with the default application.

    Parameters:
        filename (str)

    Returns:
        None
    """

    if sys.platform == "win32":

        os.startfile(filename)

    else:

        os.system("xdg-open " + filename)


# --------------------------------------------------
# MAP AIRPORTS
# --------------------------------------------------

def MapAirports(airports):

    """
    Creates a KML map with airports.

    Parameters:
        airports (list)

    Returns:
        None
    """

    filename = "airports.kml"

    file = open(filename, "w")

    file.write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
    )

    file.write(
        '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
    )

    file.write('<Document>\n')

    file.write('<Style id="schengen">\n')

    file.write(
        '<IconStyle><color>ff00ff00</color></IconStyle>\n'
    )

    file.write('</Style>\n')

    file.write('<Style id="noschengen">\n')

    file.write(
        '<IconStyle><color>ff0000ff</color></IconStyle>\n'
    )

    file.write('</Style>\n')

    i = 0

    while i < len(airports):

        if airports[i].Schengen:

            style = "#schengen"

        else:

            style = "#noschengen"

        file.write('<Placemark>\n')

        file.write(
            '<name>'
            + airports[i].ICAO
            + '</name>\n'
        )

        file.write(
            '<styleUrl>'
            + style
            + '</styleUrl>\n'
        )

        file.write('<Point>\n')

        file.write('<coordinates>\n')

        file.write(
            str(airports[i].longitude)
            + ","
            + str(airports[i].latitude)
            + "\n"
        )

        file.write('</coordinates>\n')

        file.write('</Point>\n')

        file.write('</Placemark>\n')

        i = i + 1

    file.write('</Document>\n')

    file.write('</kml>\n')

    file.close()

    open_file(filename)
>>>>>>> d2d42b882792b520f895989799dc6fdedc700ec6
