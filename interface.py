import tkinter as tk
<<<<<<< HEAD
from LEBL import *
=======
from airport import *
from aircraft import *
>>>>>>> d2d42b882792b520f895989799dc6fdedc700ec6

# ---------------- VARIABLES ----------------

airports = []
<<<<<<< HEAD
bcn = None
=======
>>>>>>> d2d42b882792b520f895989799dc6fdedc700ec6
aircrafts = []

# ---------------- FUNCTIONS AIRPORTS ----------------

def load_airports():

    """
    Loads airports from Airports.txt
    and stores them in the airports list.

    Parameters:
        None

    Returns:
        None
    """

    global airports

<<<<<<< HEAD
    airports = LoadAirports("DATA/Airports.txt")
=======
    airports = LoadAirports("Airports.txt")
>>>>>>> d2d42b882792b520f895989799dc6fdedc700ec6

    text_box.delete("1.0", tk.END)

    label.config(text="Loaded " + str(len(airports)) + " airports")


def show_airports():

    """
    Shows all airports in the text box.

    Parameters:
        None

    Returns:
        None
    """

    text_box.delete("1.0", tk.END)

    i = 0

    while i < len(airports):

        SetSchengen(airports[i])

        line = airports[i].ICAO + " | "

        line += "{:.4f}".format(airports[i].latitude) + " "

        line += "{:.4f}".format(airports[i].longitude)

        line += " | Schengen: " + str(airports[i].Schengen)

        text_box.insert(tk.END, line + "\n")

        i = i + 1


def add_airport():

    """
    Adds a new airport to the airports list.

    Parameters:
        None

    Returns:
        None
    """

    code = entry_code.get()

    lat = entry_lat.get()

    lon = entry_lon.get()

    try:

        airport = Airport(code, float(lat), float(lon))

        SetSchengen(airport)

        result = AddAirport(airports, airport)

        if result == 0:

            label.config(text="Airport added")

        else:

            label.config(text="Airport already exists")

    except ValueError:

        label.config(text="Invalid input")


def remove_airport():

    """
    Removes an airport from the airports list.

    Parameters:
        None

    Returns:
        None
    """

    code = entry_code.get()

    result = RemoveAirport(airports, code)

    if result == 0:

        label.config(text="Airport removed")

    else:

        label.config(text="Airport not found")


def save_schengen():
<<<<<<< HEAD
=======

    """
    Saves Schengen airports into a text file.

    Parameters:
        None

    Returns:
        None
    """

    i = 0

    while i < len(airports):

        SetSchengen(airports[i])

        i = i + 1
>>>>>>> d2d42b882792b520f895989799dc6fdedc700ec6

    """
    Saves Schengen airports into a text file.

    Parameters:
        None

    Returns:
        None
    """

    i = 0

    while i < len(airports):

        SetSchengen(airports[i])

        i = i + 1

    result = SaveSchengenAirports(airports, "OUTPUTS/schengen.txt")

    if result == 0:

        label.config(text="Schengen airports saved")

    else:

        label.config(text="Error saving")


def plot_airports():

    """
    Creates a plot with airport positions.

    Parameters:
        None

    Returns:
        None
    """

    if len(airports) == 0:

        label.config(text="Load airports first")

        return

    i = 0

    while i < len(airports):

        SetSchengen(airports[i])

        i = i + 1

    PlotAirportsTk(frame_plot, airports)


def map_airports():

    """
    Opens airports in Google Earth.

    Parameters:
        None

    Returns:
        None
    """

    if len(airports) == 0:

        label.config(text="Load airports first")

        return

    i = 0

    while i < len(airports):

        SetSchengen(airports[i])
<<<<<<< HEAD

        i = i + 1

    MapAirportsTk(frame_plot,airports)

    label.config(
        text="Airport map displayed"
    )
# ---------------- FUNCTIONS AIRCRAFTS ----------------

def load_arrivals():

    """
    Loads aircraft arrivals from Arrivals.txt.

    Parameters:
        None

    Returns:
        None
    """

    global aircrafts

    aircrafts = LoadArrivals("DATA/Arrivals.txt")

    text_box.delete("1.0", tk.END)

    label.config(text="Loaded " + str(len(aircrafts)) + " arrivals")


def show_aircrafts():

    """
    Shows aircraft information in the text box.

    Parameters:
        None

    Returns:
        None
    """

    text_box.delete("1.0", tk.END)

    i = 0

    while i < len(aircrafts):

        ac = aircrafts[i]

        line = ac.aircraft_id + " | "

        line += ac.company + " | "

        line += ac.origin + " | "

        line += ac.time_landing

        text_box.insert(tk.END, line + "\n")

        i = i + 1


def plot_arrivals():

    """
    Creates a plot with aircraft arrivals.

    Parameters:
        None

    Returns:
        None
    """

    if len(aircrafts) == 0:

        label.config(text="Load arrivals first")

        return

    PlotArrivalsTk(frame_plot, aircrafts)


def plot_airlines():

    """
    Creates a plot with airlines information.

    Parameters:
        None

    Returns:
        None
    """

    if len(aircrafts) == 0:

        label.config(text="Load arrivals first")

        return

    PlotAirlinesTk(frame_plot, aircrafts)


def save_flights():

    """
    Saves flights into a text file.

    Parameters:
        None

    Returns:
        None
    """

    if len(aircrafts) == 0:

        label.config(text="Load arrivals first")

        return

    result = SaveFlights(aircrafts, "OUTPUTS/flights.txt")

    if result == 0:

        label.config(text="Flights saved")

    else:

        label.config(text="Error saving flights")


# --------------------------------------------------
# BUILD AIRPORT
# --------------------------------------------------
=======

        i = i + 1

    MapAirports(airports)

    label.config(text="Map opened (check Google Earth)")


# ---------------- FUNCTIONS AIRCRAFTS ----------------

def load_arrivals():

    """
    Loads aircraft arrivals from Arrivals.txt.

    Parameters:
        None

    Returns:
        None
    """

    global aircrafts

    aircrafts = LoadArrivals("Arrivals.txt")

    text_box.delete("1.0", tk.END)

    label.config(text="Loaded " + str(len(aircrafts)) + " arrivals")


def show_aircrafts():

    """
    Shows aircraft information in the text box.

    Parameters:
        None

    Returns:
        None
    """

    text_box.delete("1.0", tk.END)

    i = 0

    while i < len(aircrafts):

        ac = aircrafts[i]

        line = ac.aircraft_id + " | "

        line += ac.company + " | "

        line += ac.origin + " | "

        line += ac.time_landing

        text_box.insert(tk.END, line + "\n")

        i = i + 1


def plot_arrivals():

    """
    Creates a plot with aircraft arrivals.

    Parameters:
        None

    Returns:
        None
    """

    if len(aircrafts) == 0:

        label.config(text="Load arrivals first")

        return

    PlotArrivalsTk(frame_plot, aircrafts)


def plot_airlines():

    """
    Creates a plot with airlines information.

    Parameters:
        None

    Returns:
        None
    """

    if len(aircrafts) == 0:

        label.config(text="Load arrivals first")

        return

    PlotAirlinesTk(frame_plot, aircrafts)


def save_flights():

    """
    Saves flights into a text file.

    Parameters:
        None

    Returns:
        None
    """

    if len(aircrafts) == 0:

        label.config(text="Load arrivals first")

        return

    result = SaveFlights(aircrafts, "flights.txt")

    if result == 0:

        label.config(text="Flights saved")

    else:

        label.config(text="Error saving flights")


# ---------------- WINDOW ----------------
>>>>>>> d2d42b882792b520f895989799dc6fdedc700ec6

def build_airport():

    global bcn

    bcn = LoadAirportStructure(
        "DATA/LEBL.txt"
    )

    if bcn == -1:

        label.config(
            text="Error loading airport"
        )

    else:

        label.config(
            text="Airport structure loaded"
        )


# --------------------------------------------------
# ASSIGN GATES
# --------------------------------------------------
def assign_gates():

    global bcn

    if bcn == None:

        label.config(
            text="Load airport first"
        )

        return

    if len(aircrafts) == 0:

        label.config(
            text="Load arrivals first"
        )

        return

    assigned = 0

    not_assigned = 0

    i = 0

    while i < len(aircrafts):

        result = AssignGate(
            bcn,
            aircrafts[i]
        )

        if result == 0:

            assigned = assigned + 1

        else:

            not_assigned = (
                not_assigned + 1
            )

        i = i + 1

    text = "Assigned: "

    text += str(assigned)

    text += " | No gate: "

    text += str(not_assigned)

    label.config(text=text)


# --------------------------------------------------
# SHOW OCCUPANCY
# --------------------------------------------------

def show_occupancy():

    global bcn

    if bcn == None:

        label.config(
            text="Load airport first"
        )

        return

    occupancy = GateOccupancy(bcn)

    text_box.delete("1.0", tk.END)

    i = 0

    while i < len(occupancy):

        text_box.insert(
            tk.END,
            occupancy[i] + "\n"
        )

        i = i + 1

def plot_occupancy():

    global bcn

    if bcn == None:

        label.config(
            text="Load airport first"
        )

        return

    PlotGateOccupancyTk(
        frame_plot,
        bcn
    )

def show_gate_assignments():

    global bcn

    if bcn == None:

        label.config(
            text="Load airport first"
        )

        return

    lines = ShowGateAssignments(
        bcn
    )

    text_box.delete("1.0", tk.END)

    i = 0

    while i < len(lines):

        text_box.insert(
            tk.END,
            lines[i] + "\n"
        )

        i = i + 1

def reset_gates():

    global bcn

    if bcn == None:

        label.config(
            text="Load airport first"
        )

        return

    ResetGates(bcn)

    label.config(
        text="All gates reset"
    )

def plot_gate_distribution():

    global bcn

    if bcn == None:

        label.config(
            text="Load airport first"
        )

        return

    PlotGateDistributionTk(
        frame_plot,
        bcn
    )

def map_flights():

    if len(aircrafts) == 0:

        label.config(
            text="Load arrivals first"
        )

        return

    if len(airports) == 0:

        label.config(
            text="Load airports first"
        )

        return

    MapFlightsTk(
        frame_plot,
        aircrafts,
        airports
    )

    label.config(
        text="Flights map opened"
    )

def plot_flights_type():

    if len(aircrafts) == 0:

        label.config(
            text="Load arrivals first"
        )

        return

    PlotFlightsTypeTk(frame_plot,aircrafts)
def show_long_distance():

    if len(aircrafts) == 0:

        label.config(
            text="Load arrivals first"
        )

        return

    if len(airports) == 0:

        label.config(
            text="Load airports first"
        )

        return

    result = LongDistanceArrivals(
        aircrafts,
        airports
    )

    text_box.delete("1.0", tk.END)

    i = 0

    while i < len(result):

        aircraft = result[i]

        line = aircraft.aircraft_id

        line += " | "

        line += aircraft.origin

        line += " | "

        line += aircraft.company

        text_box.insert(
            tk.END,
            line + "\n"
        )

        i = i + 1

# ---------------- WINDOW ----------------

window = tk.Tk()

<<<<<<< HEAD
window_color = "#F0F0F0"

window.configure(bg=window_color)

window.title("Airport and Aircraft Manager")

window.geometry("1100x700")

# ---------------- TOP OUTPUT ----------------

frame_top = tk.Frame(window)

frame_top.pack()

scrollbar = tk.Scrollbar(
    frame_top
)

scrollbar.pack(
    side=tk.RIGHT,
    fill=tk.Y
)

text_box = tk.Text(
    frame_top,
    height=12,
    width=130,
    yscrollcommand=scrollbar.set
)

text_box.pack(
    side=tk.LEFT
)

scrollbar.config(
    command=text_box.yview
)
# ---------------- CENTRAL AREA ----------------

frame_middle = tk.Frame(window)

frame_middle.pack()

frame_left = tk.Frame(frame_middle)

frame_left.grid(row=0, column=0, padx=10)

frame_center = tk.Frame(frame_middle)

frame_center.grid(row=0, column=1, padx=10)

frame_plot = tk.Frame(frame_middle)

frame_plot.grid(row=0, column=2, padx=10)

# ---------------- INPUTS ----------------

tk.Label(frame_left, text="ICAO Code").pack()

entry_code = tk.Entry(frame_left)

entry_code.pack()

tk.Label(frame_left, text="Latitude").pack()

entry_lat = tk.Entry(frame_left)

entry_lat.pack()

tk.Label(frame_left, text="Longitude").pack()

entry_lon = tk.Entry(frame_left)

entry_lon.pack()

# ---------------- AIRPORTS ----------------

tk.Label(frame_left, text="--- AIRPORTS ---").pack(pady=5)

tk.Button(
    frame_left,
    text="Load Airports",
    command=load_airports
).pack(fill="x", pady=2)

tk.Button(
    frame_left,
    text="Show Airports",
    command=show_airports
).pack(fill="x", pady=2)

tk.Button(
    frame_left,
    text="Add Airport",
    command=add_airport
).pack(fill="x", pady=2)

tk.Button(
    frame_left,
    text="Remove Airport",
    command=remove_airport
).pack(fill="x", pady=2)

=======
window.title("Airport and Aircraft Manager")

window.geometry("1100x700")

# ---------------- TOP OUTPUT ----------------

frame_top = tk.Frame(window)

frame_top.pack()

text_box = tk.Text(frame_top, height=12, width=130)

text_box.pack()

# ---------------- CENTRAL AREA ----------------

frame_middle = tk.Frame(window)

frame_middle.pack()

frame_left = tk.Frame(frame_middle)

frame_left.grid(row=0, column=0, padx=10)

frame_center = tk.Frame(frame_middle)

frame_center.grid(row=0, column=1, padx=10)

frame_plot = tk.Frame(frame_middle)

frame_plot.grid(row=0, column=2, padx=10)

# ---------------- INPUTS ----------------

tk.Label(frame_left, text="ICAO Code").pack()

entry_code = tk.Entry(frame_left)

entry_code.pack()

tk.Label(frame_left, text="Latitude").pack()

entry_lat = tk.Entry(frame_left)

entry_lat.pack()

tk.Label(frame_left, text="Longitude").pack()

entry_lon = tk.Entry(frame_left)

entry_lon.pack()

# ---------------- AIRPORTS ----------------

tk.Label(frame_left, text="--- AIRPORTS ---").pack(pady=5)

tk.Button(
    frame_left,
    text="Load Airports",
    command=load_airports
).pack(fill="x", pady=2)

tk.Button(
    frame_left,
    text="Show Airports",
    command=show_airports
).pack(fill="x", pady=2)

tk.Button(
    frame_left,
    text="Add Airport",
    command=add_airport
).pack(fill="x", pady=2)

tk.Button(
    frame_left,
    text="Remove Airport",
    command=remove_airport
).pack(fill="x", pady=2)

>>>>>>> d2d42b882792b520f895989799dc6fdedc700ec6
tk.Button(
    frame_left,
    text="Save Schengen",
    command=save_schengen
).pack(fill="x", pady=2)

tk.Button(
    frame_left,
    text="Plot Airports",
    command=plot_airports
).pack(fill="x", pady=2)

tk.Button(
    frame_left,
    text="Map Airports",
    command=map_airports
).pack(fill="x", pady=2)

# ---------------- AIRCRAFTS ----------------

tk.Label(frame_center, text="--- AIRCRAFTS ---").pack(pady=5)

tk.Button(
    frame_center,
    text="Load Arrivals",
    command=load_arrivals
).pack(fill="x", pady=2)

tk.Button(
    frame_center,
    text="Show Aircrafts",
    command=show_aircrafts
).pack(fill="x", pady=2)

tk.Button(
    frame_center,
    text="Plot Arrivals",
    command=plot_arrivals
).pack(fill="x", pady=2)

tk.Button(
    frame_center,
    text="Plot Airlines",
    command=plot_airlines
).pack(fill="x", pady=2)

tk.Button(
    frame_center,
    text="Save Flights",
    command=save_flights
).pack(fill="x", pady=2)

<<<<<<< HEAD
tk.Button(
    frame_center,
    text="Build Airport",
    command=build_airport
).pack(fill="x", pady=2)

tk.Button(
    frame_center,
    text="Assign Gates",
    command=assign_gates
).pack(fill="x", pady=2)

tk.Button(
    frame_center,
    text="Show Occupancy",
    command=show_occupancy
).pack(fill="x", pady=2)

tk.Button(
    frame_center,
    text="Plot Occupancy",
    command=plot_occupancy
).pack(fill="x", pady=2)

tk.Button(
    frame_center,
    text="Show Gate Assignments",
    command=show_gate_assignments
).pack(fill="x", pady=2)

tk.Button(
    frame_center,
    text="Reset Gates",
    command=reset_gates
).pack(fill="x", pady=2)

tk.Button(
    frame_center,
    text="Gate Distribution",
    command=plot_gate_distribution
).pack(fill="x", pady=2)

tk.Button(
    frame_center,
    text="Map Flights",
    command=map_flights
).pack(fill="x", pady=2)

tk.Button(
    frame_center,
    text="Flights Type",
    command=plot_flights_type
).pack(fill="x", pady=2)

tk.Button(
    frame_center,
    text="Long Distance",
    command=show_long_distance
).pack(fill="x", pady=2)

=======
>>>>>>> d2d42b882792b520f895989799dc6fdedc700ec6
# ---------------- STATUS ----------------

label = tk.Label(window, text="")

label.pack(pady=10)
<<<<<<< HEAD

# ---------------- START ----------------

window.mainloop()

=======

# ---------------- START ----------------

window.mainloop()
>>>>>>> d2d42b882792b520f895989799dc6fdedc700ec6
