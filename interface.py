import tkinter as tk
from LEBL import *
from PIL import Image, ImageTk

# ---------------- VARIABLES ----------------

airports = []
bcn = None
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

    airports = LoadAirports("DATA/Airports.txt")

    text_box.delete("1.0", tk.END)

    show_message(text="Loaded " + str(len(airports)) + " airports")


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

            show_message(text="Airport added")

        else:

            show_message(text="Airport already exists")

    except ValueError:

        show_message(text="Invalid input")


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

        show_message(text="Airport removed")

    else:

        show_message(text="Airport not found")


def save_schengen():

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

        show_message(text="Schengen airports saved")

    else:

        show_message(text="Error saving")

def export_kml():

    import os

    if len(airports) == 0:

        show_message(
            text="Load airports first"
        )

        return

    i = 0

    while i < len(airports):

        SetSchengen(airports[i])

        i = i + 1

    result = ExportKML(
        airports,
        "OUTPUTS/airports.kml"
    )

    if result == 0:

        os.startfile(
            os.path.abspath(
                "OUTPUTS/airports.kml"
            )
        )

        show_message(
            text="Opened in Google Earth"
        )

    else:

        show_message(
            text="Error exporting KML"
        )

def plot_airports():

    select_airports_window(
        "plot"
    )


def map_airports():

    select_airports_window(
        "map"
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

    arrivals = LoadArrivals(
        "DATA/Arrivals.txt"
    )

    departures = LoadDepartures(
        "DATA/Departures.txt"
    )

    aircrafts = MergeMovements(
        arrivals,
        departures
    )

    text_box.delete("1.0", tk.END)

    show_message(
        text="Loaded merged flights: "
             + str(len(aircrafts))
    )


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

    select_aircrafts_window(
        "arrivals"
    )

def plot_airlines():

    select_aircrafts_window(
        "airlines"
    )


def save_flights():

    """
    Saves flights into a text file.

    Parameters:
        None

    Returns:
        None
    """

    if len(aircrafts) == 0:

        show_message(text="Load arrivals first")

        return

    result = SaveFlights(aircrafts, "OUTPUTS/flights.txt")

    if result == 0:

        show_message(text="Flights saved")

    else:

        show_message(text="Error saving flights")


# --------------------------------------------------
# BUILD AIRPORT
# --------------------------------------------------

def build_airport():

    global bcn

    bcn = LoadAirportStructure(
        "DATA/LEBL.txt"
    )

    if bcn == -1:

        show_message(
            text="Error loading airport"
        )

    else:

        show_message(
            text="Airport structure loaded"
        )


# --------------------------------------------------
# ASSIGN GATES
# --------------------------------------------------
def assign_gates():

    global bcn

    if bcn == None:

        show_message(
            text="Load airport first"
        )

        return

    if len(aircrafts) == 0:

        show_message(
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

    show_message(text=text)


# --------------------------------------------------
# SHOW OCCUPANCY
# --------------------------------------------------

def show_occupancy():

    global bcn

    if bcn == None:

        show_message(
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

        show_message(
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

        show_message(
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

        show_message(
            text="Load airport first"
        )

        return

    ResetGates(bcn)

    show_message(
        text="All gates reset"
    )

def plot_gate_distribution():

    global bcn

    if bcn == None:

        show_message(
            text="Load airport first"
        )

        return

    PlotGateDistributionTk(
        frame_plot,
        bcn
    )
def gate_state_window():

    global bcn

    if bcn == None:

        show_message(
            text="Load airport first"
        )

        return

    if len(aircrafts) == 0:

        show_message(
            text="Load flights first"
        )

        return

    time = entry_hour.get()

    gates = []

    i = 0

    while i < len(bcn.terminals):

        terminal = bcn.terminals[i]

        j = 0

        while j < len(
            terminal.boarding_areas
        ):

            area = (
                terminal.boarding_areas[j]
            )

            k = 0

            while k < len(area.gates):

                gates.append(
                    area.gates[k].name
                )

                k = k + 1

            j = j + 1

        i = i + 1

    window_select = tk.Toplevel()

    window_select.title(
        "Select Gates"
    )

    window_select.geometry(
        "300x500"
    )

    listbox = tk.Listbox(
        window_select,
        selectmode=tk.MULTIPLE
    )

    listbox.pack(
        fill=tk.BOTH,
        expand=True,
        padx=10,
        pady=10
    )

    i = 0

    while i < len(gates):

        listbox.insert(
            tk.END,
            gates[i]
        )

        i = i + 1

    def select_all():

        listbox.select_set(
            0,
            tk.END
        )

    def draw_gates():

        selected = (
            listbox.curselection()
        )

        selected_gates = []

        i = 0

        while i < len(selected):

            selected_gates.append(
                gates[selected[i]]
            )

            i = i + 1

        PlotGateStateTk(
            frame_plot,
            bcn,
            aircrafts,
            time,
            selected_gates
        )

        window_select.destroy()

    tk.Button(
        window_select,
        text="Select All",
        command=select_all
    ).pack(fill="x")

    tk.Button(
        window_select,
        text="Draw Gates",
        command=draw_gates
    ).pack(fill="x")

def map_flights():

    if len(airports) == 0:

        show_message(
            text="Load airports first"
        )

        return

    select_aircrafts_window(
        "map"
    )

def plot_flights_type():

    select_aircrafts_window(
        "type"
    )

def show_long_distance():

    if len(aircrafts) == 0:

        show_message(
            text="Load arrivals first"
        )

        return

    if len(airports) == 0:

        show_message(
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
def plot_day_occupancy():

    global bcn

    if bcn == None:

        show_message(
            text="Load airport first"
        )

        return

    if len(aircrafts) == 0:

        show_message(
            text="Load aircrafts first"
        )

        return

    PlotDayOccupancy(
        frame_plot,
        bcn,
        aircrafts
    )
# ---------------- SELECTION WINDOWS ----------------

def select_airlines_window():

    """
    Opens a window to select airlines
    for plotting.
    """

    if len(aircrafts) == 0:

        show_message(
            text="Load arrivals first"
        )

        return

    companies = []

    i = 0

    while i < len(aircrafts):

        company = aircrafts[i].company

        if company not in companies:

            companies.append(company)

        i = i + 1

    companies.sort()

    window_select = tk.Toplevel()

    window_select.title(
        "Select Airlines"
    )

    window_select.geometry(
        "300x400"
    )

    tk.Label(
        window_select,
        text="Choose airlines"
    ).pack(pady=5)

    listbox = tk.Listbox(
        window_select,
        selectmode=tk.MULTIPLE
    )

    listbox.pack(
        fill=tk.BOTH,
        expand=True,
        padx=10,
        pady=10
    )

    i = 0

    while i < len(companies):

        listbox.insert(
            tk.END,
            companies[i]
        )

        i = i + 1

    def select_all():

        listbox.select_set(
            0,
            tk.END
        )

    def plot_selected():

        selected = listbox.curselection()

        filtered = []

        if len(selected) == 0:

            show_message(
                text="No airlines selected"
            )

            return

        i = 0

        while i < len(aircrafts):

            ac = aircrafts[i]

            j = 0

            while j < len(selected):

                airline = companies[
                    selected[j]
                ]

                if ac.company == airline:

                    filtered.append(ac)

                j = j + 1

            i = i + 1

        PlotAirlinesTk(
            frame_plot,
            filtered
        )

        window_select.destroy()

    tk.Button(
        window_select,
        text="Select All",
        command=select_all
    ).pack(
        fill="x",
        padx=10,
        pady=2
    )

    tk.Button(
        window_select,
        text="Plot",
        command=plot_selected
    ).pack(
        fill="x",
        padx=10,
        pady=5
    )


# ---------------- SELECTION WINDOWS ----------------

def select_airports_window(mode):

    """
    Select airports for plots or maps.
    """

    import os

    if len(airports) == 0:

        show_message(
            text="Load airports first"
        )

        return

    codes = []

    i = 0

    while i < len(airports):

        codes.append(
            airports[i].ICAO
        )

        i = i + 1

    codes.sort()

    window_select = tk.Toplevel()

    window_select.title(
        "Select Airports"
    )

    window_select.geometry(
        "300x400"
    )

    tk.Label(
        window_select,
        text="Choose airports"
    ).pack(pady=5)

    listbox = tk.Listbox(
        window_select,
        selectmode=tk.MULTIPLE
    )

    listbox.pack(
        fill=tk.BOTH,
        expand=True,
        padx=10,
        pady=10
    )

    i = 0

    while i < len(codes):

        listbox.insert(
            tk.END,
            codes[i]
        )

        i = i + 1

    def select_all():

        listbox.select_set(
            0,
            tk.END
        )

    def execute():

        selected = listbox.curselection()

        filtered = []

        if len(selected) == 0:

            show_message(
                text="No airports selected"
            )

            return

        i = 0

        while i < len(airports):

            airport = airports[i]

            j = 0

            while j < len(selected):

                code = codes[
                    selected[j]
                ]

                if airport.ICAO == code:

                    filtered.append(
                        airport
                    )

                j = j + 1

            i = i + 1

        if mode == "plot":

            PlotAirportsTk(
                frame_plot,
                filtered
            )

        elif mode == "map":

            result = ExportKML(
                filtered,
                "OUTPUTS/airports.kml"
            )

            if result == 0:

                os.startfile(
                    os.path.abspath(
                        "OUTPUTS/airports.kml"
                    )
                )

                show_message(
                    text="Opened in Google Earth"
                )

        window_select.destroy()

    tk.Button(
        window_select,
        text="Select All",
        command=select_all
    ).pack(
        fill="x",
        padx=10,
        pady=2
    )

    tk.Button(
        window_select,
        text="Execute",
        command=execute
    ).pack(
        fill="x",
        padx=10,
        pady=5
    )


def select_aircrafts_window(mode):

    """
    Select aircrafts / airlines
    for plots or maps.
    """

    import os

    if len(aircrafts) == 0:

        show_message(
            text="Load arrivals first"
        )

        return

    companies = []

    i = 0

    while i < len(aircrafts):

        company = aircrafts[i].company

        if company not in companies:

            companies.append(company)

        i = i + 1

    companies.sort()

    window_select = tk.Toplevel()

    window_select.title(
        "Select Airlines"
    )

    window_select.geometry(
        "300x400"
    )

    tk.Label(
        window_select,
        text="Choose airlines"
    ).pack(pady=5)

    listbox = tk.Listbox(
        window_select,
        selectmode=tk.MULTIPLE
    )

    listbox.pack(
        fill=tk.BOTH,
        expand=True,
        padx=10,
        pady=10
    )

    i = 0

    while i < len(companies):

        listbox.insert(
            tk.END,
            companies[i]
        )

        i = i + 1

    def select_all():

        listbox.select_set(
            0,
            tk.END
        )

    def execute():

        selected = listbox.curselection()

        filtered = []

        if len(selected) == 0:

            show_message(
                text="No airlines selected"
            )

            return

        i = 0

        while i < len(aircrafts):

            ac = aircrafts[i]

            j = 0

            while j < len(selected):

                airline = companies[
                    selected[j]
                ]

                if ac.company == airline:

                    filtered.append(ac)

                j = j + 1

            i = i + 1

        if mode == "arrivals":

            PlotArrivalsTk(
                frame_plot,
                filtered
            )

        elif mode == "airlines":

            PlotAirlinesTk(
                frame_plot,
                filtered
            )


        elif mode == "map":

            result = ExportFlightsKML(

                filtered,

                airports,

                "OUTPUTS/flights.kml"

            )

            if result == 0:
                os.startfile(

                    os.path.abspath(

                        "OUTPUTS/flights.kml"

                    )

                )

                show_message(

                    text="Flights opened in Google Earth"

                )


        elif mode == "type":

            PlotFlightsTypeTk(

                frame_plot,

                filtered

            )

        window_select.destroy()

    tk.Button(
        window_select,
        text="Select All",
        command=select_all
    ).pack(
        fill="x",
        padx=10,
        pady=2
    )

    tk.Button(
        window_select,
        text="Execute",
        command=execute
    ).pack(
        fill="x",
        padx=10,
        pady=5
    )

# ---------------- WINDOW ----------------

window = tk.Tk()

window_color = "#63C5DA"

window.configure(bg=window_color)

window.title("Airport and Aircraft Manager")

window.geometry("1100x700")

# ---------------- TOP OUTPUT ----------------

from PIL import Image, ImageTk

frame_top = tk.Frame(window)

frame_top.pack()

# -------- PLANE IMAGE --------

try:

    plane_image = Image.open(
        "LOGO.png"
    )

    plane_image = plane_image.resize((200, 200))

    plane_photo = ImageTk.PhotoImage(
        plane_image
    )

    plane_label = tk.Label(
        frame_top,
        image=plane_photo,
        bg=window_color
    )

    plane_label.pack(
        side=tk.LEFT,
        padx=10
    )

except:

    pass

# -------- TEXT AREA --------

scrollbar = tk.Scrollbar(
    frame_top,
    bg=window_color
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

def show_message(text):

    text_box.delete("1.0", tk.END)

    text_box.insert(tk.END,text.upper())

    text_box.tag_add(
        "red",
        "1.0",
        tk.END
    )

    text_box.tag_config("red",foreground="red",font=("Arial", 12, "bold"))

# ---------------- BOTTOM AREA ----------------

frame_bottom = tk.Frame(window)

frame_bottom.configure(bg=window_color)

frame_bottom.pack(fill=tk.BOTH,expand=True)

# LEFT = BUTTONS

frame_buttons = tk.Frame(frame_bottom)

frame_buttons.pack(side=tk.LEFT,fill=tk.Y,padx=10,pady=10)

# RIGHT = PLOTS

frame_plot = tk.Frame(frame_bottom)

frame_plot.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True,padx=10,pady=10)

# SUBDIVISION OF BUTTONS

frame_left = tk.Frame(frame_buttons)


frame_left.pack(side=tk.LEFT,padx=10)

frame_center = tk.Frame(frame_buttons)

frame_center.pack(
    side=tk.LEFT,
    padx=10
)

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

tk.Label(
    frame_left,
    text="Hour (HH:MM)"
).pack()

entry_hour = tk.Entry(
    frame_left
)

entry_hour.pack()

entry_hour.insert(
    0,
    "10:00"
)

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
        text="Day Occupancy",
        command=plot_day_occupancy
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
    text="Gate Viewer",
    command=gate_state_window
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

# ---------------- FOOTER ----------------

frame_footer = tk.Frame(
    window,
    bg=window_color
)

frame_footer.pack(
    side=tk.BOTTOM,
    fill=tk.X,
    pady=10
)

title_label = tk.Label(
    frame_footer,
    text="✈ AIRPORT & AIRCRAFT MANAGER ✈",
    font=("Exo", 12, "bold"),
    fg="#12086F",
    bg=window_color
)

title_label.pack()

plane_label = tk.Label(
    frame_footer,
    text="G13: Martí Vázquez, Pablo Romero, Paula Bautista",
    font=("Garamond", 12, "bold"),
    fg="#FF6000",
    bg=window_color
)

plane_label.pack()

# ---------------- START ----------------

window.mainloop()