import matplotlib.pyplot as plt
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

    Parameters:
        filename (str)

    Returns:
        list
    """

    airports = []

    try:

        file = open(filename, "r")

    except:

        return []

    line = file.readline()

    line = file.readline()

    while line != "":

        parts = line.split()

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

        line = file.readline()

    file.close()

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

    written = False

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
        label="Schengen"
    )

    ax.bar(
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

    widgets = frame.winfo_children()

    i = 0

    while i < len(widgets):

        widgets[i].destroy()

        i = i + 1

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

    canvas = FigureCanvasTkAgg(
        fig,
        master=frame
    )

    canvas.draw()

    canvas.get_tk_widget().pack()


# --------------------------------------------------
# AIRPORT COORDINATES
# --------------------------------------------------

def AirportCoords(airports):

    coords = {}

    i = 0

    while i < len(airports):

        airport = airports[i]

        coords[
            airport.ICAO
        ] = (
            airport.latitude,
            airport.longitude
        )

        i = i + 1

    return coords

def MapAirportsTk(frame, airports):

    widgets = frame.winfo_children()

    i = 0

    while i < len(widgets):

        widgets[i].destroy()

        i = i + 1

    fig = Figure(figsize=(10, 5))

    ax = fig.add_subplot(111)
    ax.set_facecolor("lightblue")

    fig.patch.set_facecolor("white")

    i = 0

    while i < len(airports):

        airport = airports[i]

        x = airport.longitude

        y = airport.latitude

        if airport.Schengen:

            color = "blue"

        else:

            color = "red"

        ax.plot(
            x,
            y,
            marker="o",
            color=color
        )

        ax.text(
            x + 1,
            y + 1,
            airport.ICAO,
            fontsize=6
        )

        i = i + 1

    ax.set_xlim(-180, 180)

    ax.set_ylim(-90, 90)

    ax.set_title("Airport Map")

    ax.set_xlabel("Longitude")

    ax.set_ylabel("Latitude")

    ax.grid(True)

    canvas = FigureCanvasTkAgg(
        fig,
        master=frame
    )

    canvas.draw()

    canvas.get_tk_widget().pack()