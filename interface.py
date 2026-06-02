import tkinter as tk
from LEBL import *
from PIL import Image, ImageTk
class RoundedButton(tk.Canvas):

    def __init__(self, parent, text="", command=None, radius=18,
                 bg="#12086F", fg="white", hover_bg="#2A1FA8",
                 width=170, height=30,
                 font=("Arial", 9, "bold"), **kwargs):

        parent_bg = window_color

        try:
            parent_bg = parent.cget("bg")
        except:
            pass

        super().__init__(
            parent,
            width=width,
            height=height,
            bg=parent_bg,
            highlightthickness=0,
            bd=0,
            **kwargs
        )

        self.command = command
        self.radius = radius
        self.bg_color = bg
        self.fg_color = fg
        self.hover_color = hover_bg
        self.text = text
        self.font = font
        self._btn_w = width
        self._btn_h = height
        self._current = bg

        self._draw(bg)

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Configure>", self._on_resize)

    def _draw(self, color):

        self.delete("all")

        w = self._btn_w
        h = self._btn_h
        r = min(self.radius, h / 2, w / 2)

        points = [
            r, 0,
            w - r, 0,
            w, 0,
            w, r,
            w, h - r,
            w, h,
            w - r, h,
            r, h,
            0, h,
            0, h - r,
            0, r,
            0, 0,
        ]

        self.create_polygon(
            points,
            smooth=True,
            fill=color,
            outline=color
        )

        self.create_text(
            w / 2,
            h / 2,
            text=self.text,
            fill=self.fg_color,
            font=self.font
        )

        self._current = color

    def _on_click(self, event):

        if self.command:

            self.command()

    def _on_enter(self, event):

        self._draw(self.hover_color)

    def _on_leave(self, event):

        self._draw(self.bg_color)

    def _on_resize(self, event):

        self._btn_w = event.width
        self._btn_h = event.height
        self._draw(self._current)
# ---------------- VARIABLES ----------------

airports = []
bcn = None
aircrafts = []
current_time_minutes = 600
simulation_running = False
dark_mode = False

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
    if len(airports) == 0:
        show_message(
            text=
            "No airports loaded.\n"
            "Click LOAD AIRPORTS first."
        )

        return

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
        if (
                code == ""
                or lat == ""
                or lon == ""
        ):
            show_message(
                text=
                "Missing information.\n"
                "Enter ICAO, latitude and longitude."
            )

            return

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
    """
        Exports selected airports to a KML file
        and opens it in Google Earth.
        """
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
    """
        Opens the airport selection window
        and plots the chosen airports.
        """
    select_airports_window(
        "plot"
    )


def map_airports():
    """
        Opens the airport selection window
        and exports selected airports to Google Earth.
        """
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
    if len(aircrafts) == 0:

        show_message(
            text="Load flights first"
        )

        return

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
    Opens an airline selection window
    and plots hourly arrival distribution.
    """
    select_aircrafts_window(
        "arrivals"
    )

def plot_airlines():
    """
        Opens an airline selection window
        and plots airline traffic statistics.
        """
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
    """
        Loads the LEBL airport structure from file
        and creates terminals, boarding areas and gates.
        """
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
    """
    Assigns available gates to all loaded aircraft
    according to airline terminal and flight type.
    """

    global bcn

    if bcn == None:
        show_message(
            text=
            "Airport not loaded.\n"
            "Click BUILD AIRPORT first."
        )

        return

    if len(aircrafts) == 0:
        show_message(
            text=
            "No flights loaded.\n"
            "Click LOAD FLIGHTS first."
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
    update_status()


# --------------------------------------------------
# SHOW OCCUPANCY
# --------------------------------------------------

def show_occupancy():
    """
    Displays the occupancy status of all gates
    in the airport structure.
    """

    global bcn

    if bcn == None:

        show_message(
            text=
            "Airport structure missing.\n"
            "Click BUILD AIRPORT first."
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
    """
    Draws a graphical representation
    of current gate occupancy.
    """
    global bcn

    if bcn == None:

        show_message(
            text=
            "Airport structure missing.\n"
            "Click BUILD AIRPORT first."
        )

        return

    PlotGateOccupancyTk(
        frame_plot,
        bcn
    )

def show_gate_assignments():
    """
    Displays which aircraft is assigned
    to each airport gate.
    """
    global bcn

    if bcn == None:

        show_message(
            text="Load and Build airport first"
        )

        return

    lines = ShowGateAssignments(
        bcn
    )
    if len(lines) == 0:
        show_message(
            text="No gate assignments"
        )

        return

    text_box.delete("1.0", tk.END)

    i = 0

    while i < len(lines):

        text_box.insert(
            tk.END,
            lines[i] + "\n"
        )

        i = i + 1

def reset_gates():
    """
    Frees all airport gates and removes
    current aircraft assignments.
    """
    global bcn

    if bcn == None:

        show_message(
            text=
            "Airport structure missing.\n"
            "Click BUILD AIRPORT first."
        )

        return

    ResetGates(bcn)

    show_message(
        text="All gates reset"
    )

def plot_gate_distribution():
    """
    Plots gate distribution across
    terminals and boarding areas.
    """
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
    """
    Opens a window that allows the user
    to select gates and visualize their
    state at a specific simulation time.
    """
    global bcn

    if bcn == None:
        show_message(
            text=
            "Gate Viewer unavailable.\n"
            "Step 1: Click BUILD AIRPORT."
        )

        return

    if len(aircrafts) == 0:
        show_message(
            text=
            "Gate Viewer unavailable.\n"
            "Step 1: Click LOAD FLIGHTS."
        )

        return
    time = entry_hour.get()
    try:

        parts = time.split(":")

        hour = int(parts[0])

        minute = int(parts[1])

        if (
                hour < 0
                or hour > 23
                or minute < 0
                or minute > 59
        ):
            raise ValueError

    except:

        show_message(
            text=
            "Invalid time.\n"
            "Use HH:MM format."
        )

        return



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
    """
    Opens the airline selection window
    and exports flight routes to Google Earth.
    """
    if len(airports) == 0:

        show_message(
            text=
            "Airport database not loaded.\n"
            "Click LOAD AIRPORTS first."
        )

        return

    select_aircrafts_window(
        "map"
    )

def plot_flights_type():
    """
    Opens an airline selection window
    and plots flight type distribution.
    """
    select_aircrafts_window(
        "type"
    )

def show_long_distance():
    """
    Displays flights arriving from airports
    located more than 2000 km away.
    """
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
    """
    Plots airport gate occupancy evolution
    throughout the day.
    """
    global bcn

    if bcn == None:

        show_message(
            text=
            "Airport structure missing.\n"
            "Click BUILD AIRPORT first."
        )

        return

    if len(aircrafts) == 0:
        show_message(
            text=
            "No flights loaded.\n"
            "Click LOAD FLIGHTS first."
        )

        return

    PlotDayOccupancy(
        frame_plot,
        bcn,
        aircrafts
    )
def update_gate_view():
    """
    Updates the graphical gate viewer using
    the current simulation time.
    """
    global bcn

    if bcn == None:

        return

    if len(aircrafts) == 0:

        return

    time_text = (
        GetCurrentTimeText()
    )

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

    PlotGateStateTk(
        frame_plot,
        bcn,
        aircrafts,
        time_text,
        gates
    )

    show_message(
        text="Showing airport at "
             + time_text
    )
    update_status()

def next_hour():
    """
    Advances simulation time by 10 minutes
    and refreshes the gate viewer.
    """
    global current_time_minutes

    current_time_minutes = (
                                   current_time_minutes + 10
                           ) % (24 * 60)

    entry_hour.delete(0, tk.END)

    entry_hour.insert(
        0,
        GetCurrentTimeText()
    )

    update_gate_view()


def previous_hour():
    """
    Moves simulation time back by 10 minutes
    and refreshes the gate viewer.
    """
    global current_time_minutes

    current_time_minutes = (
        current_time_minutes - 10
    ) % (24 * 60)

    entry_hour.delete(0, tk.END)

    entry_hour.insert(
        0,
        GetCurrentTimeText()
    )

    update_gate_view()

def run_simulation():
    """
    Internal loop that updates the simulation
    automatically while it is running.
    """
    global simulation_running

    if simulation_running == False:

        return

    next_hour()

    window.after(
        1000,
        run_simulation
    )
def start_simulation():
    """
    Starts automatic airport simulation
    and aircraft animation.
    """
    global simulation_running

    global bcn

    if bcn == None:

        show_message(
            text="Load and Build airport first"
        )

        return

    if len(aircrafts) == 0:

        show_message(
            text="Load flights first"
        )

        return

    simulation_running = True
    animate_plane()
    show_message(
        text=
        "Simulation started.\n"
        "Airport time will advance every second."
    )

    run_simulation()

def stop_simulation():
    """
    Stops automatic airport simulation.
    """
    global simulation_running

    if simulation_running == False:

        show_message(
            text="Simulation already stopped"
        )

        return

    simulation_running = False

    show_message(
        text="Simulation stopped"
    )

def simulate_day():
    """
    Runs a complete day simulation and
    displays the assignment results.
    """
    global bcn

    if bcn == None:
        show_message(
            text=
            "Airport not loaded.\n"
            "Click BUILD AIRPORT first."
        )

        return

    if len(aircrafts) == 0:
        show_message(
            text=
            "No flights loaded.\n"
            "Click LOAD FLIGHTS first."
        )

        return

    results = SimulateDay(
        bcn,
        aircrafts
    )

    text_box.delete(
        "1.0",
        tk.END
    )

    i = 0

    while i < len(results):

        text_box.insert(
            tk.END,
            results[i] + "\n"
        )

        i = i + 1

def GetCurrentTimeText():
    """
    Converts simulation minutes into HH:MM format.
    """
    global current_time_minutes

    hour = (
        current_time_minutes // 60
    ) % 24

    minute = (
        current_time_minutes % 60
    )

    text = (
        str(hour).zfill(2)
        + ":"
        + str(minute).zfill(2)
    )

    return text
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
    ).pack(pady=2)

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
        pady=1
    )

    tk.Button(
        window_select,
        text="Plot",
        command=plot_selected
    ).pack(
        fill="x",
        padx=10,
        pady=2
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
    ).pack(pady=2)

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
        pady=1
    )

    tk.Button(
        window_select,
        text="Execute",
        command=execute
    ).pack(
        fill="x",
        padx=10,
        pady=2
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
    ).pack(pady=2)

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
        pady=1
    )

    tk.Button(
        window_select,
        text="Execute",
        command=execute
    ).pack(
        fill="x",
        padx=10,
        pady=2
    )

def toggle_theme():
    """
    Switches between light mode and dark mode.
    """
    global dark_mode
    global theme_button


    dark_mode = not dark_mode

    if dark_mode:
        frame_buttons.configure(
            bg="#1E1E1E"
        )
        frame_plot.configure(
            bg="#1E1E1E"
        )
        frame_airports_buttons.configure(bg="#1E1E1E")
        frame_aircrafts_buttons.configure(bg="#1E1E1E")
        frame_simulation_buttons.configure(bg="#1E1E1E")
        frame_visual_buttons.configure(bg="#1E1E1E")
        frame_airports.configure(
            bg="#1E1E1E",
            fg="white"
        )

        frame_aircrafts.configure(
            bg="#1E1E1E",
            fg="white"
        )

        frame_simulation.configure(
            bg="#1E1E1E",
            fg="white"
        )

        frame_visual.configure(
            bg="#1E1E1E",
            fg="white"
        )

        status_label.configure(
            bg="#1E1E1E",
            fg="white"
        )

        frame_footer.configure(
            bg="#1E1E1E"
        )
        theme_button.text = "☀ Day Mode"

        theme_button._draw(theme_button.bg_color)

        window.configure(bg="#1E1E1E")

        frame_main.configure(bg="#1E1E1E")

        frame_bottom.configure(bg="#1E1E1E")

        frame_output.configure(bg="#1E1E1E")

        text_box.configure(
                bg="#2D2D2D",
                fg="white",
                insertbackground="white"
            )

        title_label.configure(
                bg="#1E1E1E",
                fg="white"
            )

        plane_label.configure(
                bg="#1E1E1E",
                fg="#FFD700"
            )

    else:
        frame_buttons.configure(
            bg=window_color
        )
        frame_plot.configure(
            bg="#DCDCDC"
        )
        frame_airports_buttons.configure(bg=window_color)
        frame_aircrafts_buttons.configure(bg=window_color)
        frame_simulation_buttons.configure(bg=window_color)
        frame_visual_buttons.configure(bg=window_color)
        frame_airports.configure(
            bg=window_color,
            fg="black"
        )

        frame_aircrafts.configure(
            bg=window_color,
            fg="black"
        )

        frame_simulation.configure(
            bg=window_color,
            fg="black"
        )

        frame_visual.configure(
            bg=window_color,
            fg="black"
        )

        status_label.configure(
            bg="#DCDCDC",
            fg="black"
        )

        frame_footer.configure(
            bg=window_color
        )
        theme_button.text = "🌙 Night Mode"

        theme_button._draw(theme_button.bg_color)

        window.configure(bg=window_color)

        frame_main.configure(bg=window_color)

        frame_bottom.configure(bg=window_color)

        frame_output.configure(bg=window_color)

        text_box.configure(
                bg="#EAF0FF",
                fg="#12086F",
                insertbackground="#12086F"
            )

        title_label.configure(
                bg=window_color,
                fg="#12086F"
            )

        plane_label.configure(
                bg=window_color,
                fg="#FF6000"
            )

def show_splash():
    """
    Displays the project welcome screen.
    """
    splash = tk.Toplevel()

    splash.title("Welcome")

    splash.geometry("500x300")

    splash.resizable(False, False)

    tk.Label(
        splash,
        text="✈ AIRPORT & AIRCRAFT MANAGER ✈",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        splash,
        text=(
            "Barcelona Airport Simulation System\n\n"
            "Group 13\n\n"
            "Martí Vázquez\n"
            "Pablo Romero\n"
            "Paula Bautista"
        ),
        font=("Arial", 11)
    ).pack()

    tk.Button(
        splash,
        text="Start",
        command=splash.destroy,
        width=15
    ).pack(pady=20)

    splash.grab_set()
# ---------------- WINDOW ----------------

window = tk.Tk()

window_color = "#63C5DA"

window.configure(bg=window_color)

window.title("Airport and Aircraft Manager")

window.geometry("1100x900")


def show_message(text):
    """
    Displays a formatted system message
    in the output panel.
    """
    text_box.delete("1.0", tk.END)

    text_box.insert(
        tk.END,
        "SYSTEM MESSAGE\n\n"
        + text
    )

    text_box.tag_add(
        "message",
        "1.0",
        tk.END
    )

    text_box.tag_config(
        "message",
        foreground="#C00000",
        font=("Arial", 11, "bold")
    )

def update_status():
    """
    Updates the airport status panel with
    occupancy and utilization information.
    """
    global bcn

    global aircrafts


    if bcn == None:

        return

    occupied = 0

    total = 0

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

                gate = area.gates[k]

                total = total + 1

                if gate.occupied == True:

                    occupied = occupied + 1

                k = k + 1

            j = j + 1

        i = i + 1

    free = total - occupied
    utilization = 0

    if total > 0:
        utilization = (
                              occupied * 100
                      ) / total

    text = (
            "TIME: "
            + GetCurrentTimeText()
            + "\n"
    )

    text += (
            "ACTIVE FLIGHTS: "
            + str(len(aircrafts))
            + "\n"
    )

    text += (
        "OCCUPIED GATES: "
        + str(occupied)
        + "\n"
    )

    text += (
            "FREE GATES: "
            + str(free)
            + "\n"
    )

    text += (
            "UTILIZATION: "
            + str(round(utilization, 1))
            + "%"
    )

    try:

        status_label.config(
            text=text
        )

    except:

        return

def show_help(title, message):
    """
    Opens a help window with information
    about a selected functionality.
    """
    help_window = tk.Toplevel()

    help_window.title(title)

    help_window.geometry("350x200")

    label = tk.Label(
        help_window,
        text=message,
        wraplength=300,
        justify="left",
        padx=20,
        pady=20
    )

    label.pack()
def show_statistics():
    """
    Displays airport statistics including
    utilization, gates and airline activity.
    """
    global bcn
    companies = []
    counts = []

    i = 0

    while i < len(aircrafts):

        company = aircrafts[i].company

        if company in companies:

            pos = companies.index(company)

            counts[pos] += 1

        else:

            companies.append(company)

            counts.append(1)

        i += 1

    most_company = ""
    most_count = 0

    i = 0

    while i < len(counts):

        if counts[i] > most_count:
            most_count = counts[i]

            most_company = companies[i]

        i += 1

    if bcn == None:

        show_message(
            text=
            "Airport structure missing.\n"
            "Click BUILD AIRPORT first."
        )

        return

    if len(aircrafts) == 0:

        show_message(
            text=
            "No flights loaded.\n"
            "Click LOAD FLIGHTS first."
        )

        return

    occupied = 0
    total = 0

    i = 0

    while i < len(bcn.terminals):

        terminal = bcn.terminals[i]

        j = 0

        while j < len(terminal.boarding_areas):

            area = terminal.boarding_areas[j]

            k = 0

            while k < len(area.gates):

                total += 1

                if area.gates[k].occupied:

                    occupied += 1

                k += 1

            j += 1

        i += 1

    utilization = 0

    if total > 0:

        utilization = (
            occupied * 100
        ) / total

    text = (
        "AIRPORT REPORT\n\n"
        + "Flights Loaded: "
        + str(len(aircrafts))
        + "\n"
        + "Airports Loaded: "
        + str(len(airports))
        + "\n"
        + "Occupied Gates: "
        + str(occupied)
        + "\n"
        + "Free Gates: "
        + str(total - occupied)
        + "\n"
        + "Utilization: "
        + str(round(utilization, 1))
        + "%"
        + "\n\nMost Used Airline: "
        + most_company
        + "\nFlights: "
        + str(most_count)
    )

    text_box.delete("1.0", tk.END)

    text_box.insert(
        tk.END,
        text
    )
    update_status()

def animate_plane(x=-60):
    """
    Animates the aircraft icon during
    simulation playback.
    """
    global simulation_running

    if not simulation_running:
        return

    plane_animation.place(
        x=x,
        y=820
    )

    plane_animation.lift()

    if x > window.winfo_width():

        x = -60

    window.after(
        20,
        lambda: animate_plane(x + 5)
    )
def show_extras():
    """
    Displays a window describing all extra
    functionalities added to the project.
    """
    window_extras = tk.Toplevel()

    window_extras.title(
        "Extra Functionalities"
    )

    window_extras.geometry(
        "800x600"
    )

    text = tk.Text(
        window_extras,
        wrap="word",
        font=("Arial", 10)
    )

    text.pack(
        fill=tk.BOTH,
        expand=True
    )

    info = """

EXTRA FUNCTIONALITIES DEVELOPED
==============================

The following features were NOT required in the official versions of the project
and were developed as additional improvements.

----------------------------------------------------
1. Dynamic Gate Viewer
----------------------------------------------------
Visual representation of airport gates.
Shows free, occupied and soon-departing aircraft.

----------------------------------------------------
2. Time Simulation
----------------------------------------------------
Airport status can be visualized at any
moment of the day.

Buttons:
-10 min
+10 min
Start Simulation
Stop Simulation

----------------------------------------------------
3. Dark Mode
----------------------------------------------------
Complete interface theme switching.

----------------------------------------------------
4. Statistics Dashboard
----------------------------------------------------
Displays:

- Flights loaded
- Airports loaded
- Occupied gates
- Free gates
- Utilization percentage
- Most used airline

----------------------------------------------------
5. Interactive Help System
----------------------------------------------------
Every button contains a help icon
with explanations.

----------------------------------------------------
6. Enhanced System Messages
----------------------------------------------------
User-friendly feedback messages.

Examples:

SYSTEM MESSAGE

Airport loaded successfully

SYSTEM MESSAGE

Flights opened in Google Earth

SYSTEM MESSAGE

Simulation started

----------------------------------------------------
7. Dynamic Airport Status Panel
----------------------------------------------------
Real-time monitoring of:

- Current simulation time
- Active flights
- Occupied gates
- Free gates
- Utilization percentage

----------------------------------------------------
8. Advanced Gate Occupancy Visualization
----------------------------------------------------
Graphical airport structure with terminals,
boarding areas and gates.

----------------------------------------------------
9. Night Aircraft Support
----------------------------------------------------
Automatic assignment of aircraft already
present at the airport before the start
of the day.

----------------------------------------------------
10. Airport Splash Screen
----------------------------------------------------
Welcome screen with project information.

----------------------------------------------------
11. Airline Selection Windows
----------------------------------------------------
Interactive airline filtering before
plots and maps.

"""
    text.insert(
        tk.END,
        info
    )

    text.config(
        state="disabled"
    )
# ---------------- MAIN AREA ----------------

frame_main = tk.Frame(
    window,
    bg=window_color
)

frame_main.pack(
    fill=tk.BOTH,
    expand=True
)

# ---------------- OUTPUT PANEL ----------------

frame_output = tk.Frame(
    frame_main,
    bg=window_color
)

frame_output.pack(
    side=tk.LEFT,
    fill=tk.Y,
    padx=10,
    pady=10
)

scrollbar = tk.Scrollbar(
    frame_output
)

scrollbar.pack(
    side=tk.RIGHT,
    fill=tk.Y
)

text_box = tk.Text(
    frame_output,
    width=35,
    height=35,
    yscrollcommand=scrollbar.set,
    bg="#EAF0FF",
    fg="#12086F",
    insertbackground="#12086F"
)

text_box.pack(
    side=tk.LEFT,
    fill=tk.Y
)

scrollbar.config(
    command=text_box.yview
)
# ---------------- BOTTOM AREA ----------------

frame_bottom = tk.Frame(
    frame_main,
    bg=window_color
)

frame_bottom.configure(bg=window_color)

frame_bottom.pack(fill=tk.BOTH,expand=True)

# LEFT = BUTTONS

# --------------------------------
# SCROLLABLE BUTTON PANEL
# --------------------------------

buttons_container = tk.Frame(
    frame_bottom
)

buttons_container.pack(
    side=tk.LEFT,
    fill=tk.Y,
    padx=10,
    pady=10
)

buttons_canvas = tk.Canvas(
    buttons_container,
    width=360,
    highlightthickness=0
)

buttons_scrollbar = tk.Scrollbar(
    buttons_container,
    orient="vertical",
    command=buttons_canvas.yview
)

frame_buttons = tk.Frame(
    buttons_canvas
)

frame_buttons.bind(
    "<Configure>",
    lambda e:
    buttons_canvas.configure(
        scrollregion=
        buttons_canvas.bbox("all")
    )
)

buttons_canvas.create_window(
    (0, 0),
    window=frame_buttons,
    anchor="nw"
)

buttons_canvas.configure(
    yscrollcommand=
    buttons_scrollbar.set
)

buttons_canvas.pack(
    side="left",
    fill="y",
    expand=False
)

buttons_scrollbar.pack(
    side="right",
    fill="y"
)

# ----------------------------
# MOUSE WHEEL
# ----------------------------

def _on_mousewheel(event):
    """
    Enables mouse wheel scrolling
    in the button panel.
    """
    buttons_canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )

buttons_canvas.bind_all(
    "<MouseWheel>",
    _on_mousewheel
)

# ----------------------------
# BUTTON GROUPS
# ----------------------------

frame_airports = tk.LabelFrame(
    frame_buttons,
    text="AIRPORTS",
    padx=5,
    pady=2
)
# RIGHT = PLOTS

frame_plot = tk.Frame(frame_bottom)

frame_plot.pack(
    side=tk.RIGHT,
    fill=tk.BOTH,
    expand=True,
    padx=10,
    pady=10)

status_label = tk.Label(
    frame_plot,
    text="AIRPORT STATUS",
    font=("Arial", 11, "bold"),
    justify="left"
)

status_label.pack(
    anchor="w",
    pady=5
)

# ---------------- BUTTON GROUPS ----------------

frame_airports = tk.LabelFrame(
    frame_buttons,
    text="AIRPORTS",
    padx=5,
    pady=2
)

frame_airports.pack(
    fill="x",
    pady=2
)
frame_airports_buttons = tk.Frame(
    frame_airports
)

frame_airports_buttons.pack()

frame_aircrafts = tk.LabelFrame(
    frame_buttons,
    text="AIRCRAFTS",
    padx=5,
    pady=2
)
frame_aircrafts.pack(
    fill="x",
    pady=2
)
frame_aircrafts_buttons = tk.Frame(
    frame_aircrafts
)

frame_aircrafts_buttons.pack()

frame_simulation = tk.LabelFrame(
    frame_buttons,
    text="SIMULATION",
    padx=5,
    pady=2
)

frame_simulation.pack(
    fill="x",
    pady=2
)
frame_simulation_buttons = tk.Frame(
    frame_simulation
)

frame_simulation_buttons.pack()
frame_visual = tk.LabelFrame(
    frame_buttons,
    text="VISUALIZATION",
    padx=5,
    pady=2
)

frame_visual.pack(
    fill="x",
    pady=2
)
frame_visual_buttons = tk.Frame(
    frame_visual
)

frame_visual_buttons.pack()

theme_button = RoundedButton(
    frame_visual_buttons,
    text="🌙 Night Mode",
    command=toggle_theme,
    width=195,
    height=26,
    radius=12
)
RoundedButton(
    frame_visual_buttons,
    text="⭐ Extras",
    command=show_extras,
    bg="#FFD700",
    hover_bg="#E6C200",
    fg="black",
    width=195,
    height=26,
    radius=12
).grid(
    row=3,
    column=0,
    columnspan=2,
    padx=1,
    pady=5
)

theme_button.grid(
    row=2,
    column=0,
    columnspan=2,
    padx=1,
    pady=5
)
# ---------------- INPUTS ----------------

tk.Label(frame_airports, text="ICAO Code").pack()

entry_code = tk.Entry(frame_airports)

entry_code.pack()

tk.Label(frame_airports, text="Latitude").pack()

entry_lat = tk.Entry(frame_airports)

entry_lat.pack()

tk.Label(frame_airports, text="Longitude").pack()

entry_lon = tk.Entry(frame_airports)

entry_lon.pack()

tk.Label(
    frame_airports,
    text="Hour (HH:MM)"
).pack()

entry_hour = tk.Entry(
    frame_airports
)

entry_hour.pack()

entry_hour.insert(
    0,
    "10:00"
)
# ---------------- AIRPORTS ----------------

RoundedButton(
    frame_airports_buttons,
    text="Load Airports",
    command=load_airports,
    width=95,
    height=26,
    radius=12
).grid(row=0, column=0, padx=1, pady=1)

tk.Button(
    frame_airports_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Load Airports",
        "Loads airport ICAO codes and coordinates from Airports.txt."
    )
).grid(row=0, column=1)

RoundedButton(
    frame_airports_buttons,
    text="Show Airports",
    command=show_airports,
    width=95,
    height=26,
    radius=12
).grid(row=0, column=2, padx=1, pady=1)

tk.Button(
    frame_airports_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Show Airports",
        "Displays all loaded airports and Schengen status."
    )
).grid(row=0, column=3)

RoundedButton(
    frame_airports_buttons,
    text="Add Airport",
    command=add_airport,
    width=95,
    height=26,
    radius=12
).grid(row=1, column=0, padx=1, pady=1)

tk.Button(
    frame_airports_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Add Airport",
        "Adds a new airport manually using ICAO and coordinates."
    )
).grid(row=1, column=1)

RoundedButton(
    frame_airports_buttons,
    text="Remove Airport",
    command=remove_airport,
    width=95,
    height=26,
    radius=12
).grid(row=1, column=2, padx=1, pady=1)

tk.Button(
    frame_airports_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,

    command=lambda:
    show_help(
        "Remove Airport",
        "Deletes an airport from the current airport list."
    )
).grid(row=1, column=3)

RoundedButton(
    frame_airports_buttons,
    text="Save Schengen",
    command=save_schengen,
    width=95,
    height=26,
    radius=12
).grid(row=2, column=0, padx=1, pady=1)

tk.Button(
    frame_airports_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Save Schengen",
        "Exports Schengen airports into a text file."
    )
).grid(row=2, column=1)

RoundedButton(
    frame_airports_buttons,
    text="Plot Airports",
    command=plot_airports,
    width=95,
    height=26,
    radius=12
).grid(row=2, column=2, padx=1, pady=1)

tk.Button(
    frame_airports_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Plot Airports",
        "Plots selected airports on a graph."
    )
).grid(row=2, column=3)

RoundedButton(
    frame_airports_buttons,
    text="Map Airports",
    command=map_airports,
    width=95,
    height=26,
    radius=12
).grid(row=3, column=0, padx=1, pady=1)

tk.Button(
    frame_airports_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Map Airports",
        "Exports selected airports to Google Earth."
    )
).grid(row=3, column=1)

# ---------------- AIRCRAFTS ----------------

RoundedButton(
    frame_aircrafts_buttons,
    text="Load Flights",
    command=load_arrivals,
    width=95,
    height=26,
    radius=12
).grid(row=0, column=0, padx=1, pady=1)

tk.Button(
    frame_aircrafts_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Load Flights",
        "Loads arrivals and departures and merges them into daily aircraft movements."
    )
).grid(row=0, column=1)

RoundedButton(
    frame_aircrafts_buttons,
    text="Show Aircrafts",
    command=show_aircrafts,
    width=95,
    height=26,
    radius=12
).grid(row=0, column=2, padx=1, pady=1)

tk.Button(
    frame_aircrafts_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Show Aircrafts",
        "Displays all loaded aircraft information."
    )
).grid(row=0, column=3)

RoundedButton(
    frame_aircrafts_buttons,
    text="Plot Arrivals",
    command=plot_arrivals,
    width=95,
    height=26,
    radius=12
).grid(row=1, column=0, padx=1, pady=1)

tk.Button(
    frame_aircrafts_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Plot Arrivals",
        "Plots hourly arrival distribution."
    )
).grid(row=1, column=1)

RoundedButton(
    frame_aircrafts_buttons,
    text="Plot Airlines",
    command=plot_airlines,
    width=95,
    height=26,
    radius=12
).grid(row=1, column=2, padx=1, pady=1)

tk.Button(
    frame_aircrafts_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Plot Airlines",
        "Shows airline distribution statistics."
    )
).grid(row=1, column=3)

RoundedButton(
    frame_aircrafts_buttons,
    text="Save Flights",
    command=save_flights,
    width=95,
    height=26,
    radius=12
).grid(row=2, column=0, padx=1, pady=1)

tk.Button(
    frame_aircrafts_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Save Flights",
        "Exports flights into a text file."
    )
).grid(row=2, column=1)
# ---------------- SIMULATION ----------------

RoundedButton(
    frame_simulation_buttons,
    text="Build Airport",
    command=build_airport,
    width=95,
    height=26,
    radius=12
).grid(
    row=0,
    column=0,
    padx=1,
    pady=1
)

tk.Button(
    frame_simulation_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Build Airport",
        "Loads the LEBL airport structure and gates."
    )
).grid(row=0, column=1)

RoundedButton(
    frame_simulation_buttons,
    text="Assign Gates",
    command=assign_gates,
    width=95,
    height=26,
    radius=12
).grid(row=0, column=2, padx=1, pady=1)

tk.Button(
    frame_simulation_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Assign Gates",
        "Assigns aircraft to available airport gates."
    )
).grid(row=0, column=3)

RoundedButton(
    frame_simulation_buttons,
    text="Show Occupancy",
    command=show_occupancy,
    width=95,
    height=26,
    radius=12
).grid(row=1, column=0, padx=1, pady=1)

tk.Button(
    frame_simulation_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Show Occupancy",
        "Displays occupied and free gates."
    )
).grid(row=1, column=1)

RoundedButton(
    frame_simulation_buttons,
    text="Plot Occupancy",
    command=plot_occupancy,
    width=95,
    height=26,
    radius=12
).grid(row=1, column=2, padx=1, pady=1)

tk.Button(
    frame_simulation_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Plot Occupancy",
        "Plots current airport gate occupancy."
    )
).grid(row=1, column=3)

RoundedButton(
    frame_simulation_buttons,
    text="Day Occupancy",
    command=plot_day_occupancy,
    width=95,
    height=26,
    radius=12
).grid(row=2, column=0, padx=1, pady=1)

tk.Button(
    frame_simulation_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Day Occupancy",
        "Plots airport occupancy evolution during the day."
    )
).grid(row=2, column=1)

RoundedButton(
    frame_simulation_buttons,
    text="Simulate Day",
    command=simulate_day,
    width=95,
    height=26,
    radius=12
).grid(row=2, column=2, padx=1, pady=1)

tk.Button(
    frame_simulation_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Simulate Day",
        "Runs the full airport daily simulation."
    )
).grid(row=2, column=3)

RoundedButton(
    frame_simulation_buttons,
    text="Gate Viewer",
    command=gate_state_window,
    width=95,
    height=26,
    radius=12
).grid(row=3, column=0, padx=1, pady=1)

tk.Button(
    frame_simulation_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Gate Viewer",
        "Displays selected airport gates dynamically."
    )
).grid(row=3, column=1)

RoundedButton(
    frame_simulation_buttons,
    text="Reset Gates",
    command=reset_gates,
    width=95,
    height=26,
    radius=12
).grid(row=3, column=2, padx=1, pady=1)

tk.Button(
    frame_simulation_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Reset Gates",
        "Frees all airport gates."
    )
).grid(row=3, column=3)

RoundedButton(
    frame_simulation_buttons,
    text="-10 min",
    command=previous_hour,
    width=95,
    height=26,
    radius=12
).grid(row=4, column=0, padx=1, pady=1)

tk.Button(
    frame_simulation_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Previous Hour",
        "Moves simulation 10 minutes backwards."
    )
).grid(row=4, column=1)

RoundedButton(
    frame_simulation_buttons,
    text="+10 min",
    command=next_hour,
    width=95,
    height=26,
    radius=12
).grid(row=4, column=2, padx=1, pady=1)

tk.Button(
    frame_simulation_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Next Hour",
        "Moves simulation 10 minutes forward."
    )
).grid(row=4, column=3)

RoundedButton(
    frame_simulation_buttons,
    text="▶ Start Sim",
    command=start_simulation,
    width=95,
    height=26,
    radius=12
).grid(row=5, column=0, padx=1, pady=1)

tk.Button(
    frame_simulation_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Start Simulation",
        "Starts automatic 10-minute airport simulation."
    )
).grid(row=5, column=1)

RoundedButton(
    frame_simulation_buttons,
    text="⏹ Stop Sim",
    command=stop_simulation,
    width=95,
    height=26,
    radius=12
).grid(row=5, column=2, padx=1, pady=1)

tk.Button(
    frame_simulation_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Stop Simulation",
        "Stops automatic simulation playback."
    )
).grid(row=5, column=3)

RoundedButton(
    frame_simulation_buttons,
    text="Gate Assignments",
    command=show_gate_assignments,
    width=95,
    height=26,
    radius=12
).grid(row=6, column=0, padx=1, pady=1)

tk.Button(
    frame_simulation_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Gate Assignments",
        "Displays aircraft assigned to each gate."
    )
).grid(row=6, column=1)
RoundedButton(
    frame_simulation_buttons,
    text="📊 Statistics",
    command=show_statistics,
    width=95,
    height=26,
    radius=12
).grid(
    row=6,
    column=2,
    padx=1,
    pady=1
)
tk.Button(
    frame_simulation_buttons,
    text="ⓘ",
    bg="white",
    fg="black",
    width=2,
    command=lambda:
    show_help(
        "Statistics",
        "Displays airport utilization and gate statistics."
    )
).grid(
    row=6,
    column=3
)
# ---------------- VISUALIZATION ----------------

RoundedButton(
    frame_visual_buttons,
    text="Map Flights",
    command=map_flights,
    width=95,
    height=26,
    radius=12
).grid(row=0, column=0, padx=1, pady=1)

tk.Button(
    frame_visual_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Map Flights",
        "Exports selected flights into Google Earth."
    )
).grid(row=0, column=1)

RoundedButton(
    frame_visual_buttons,
    text="Flights Type",
    command=plot_flights_type,
    width=95,
    height=26,
    radius=12
).grid(row=0, column=2, padx=1, pady=1)

tk.Button(
    frame_visual_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Flights Type",
        "Plots the distribution of flight types."
    )
).grid(row=0, column=3)

RoundedButton(
    frame_visual_buttons,
    text="Long Distance",
    command=show_long_distance,
    width=95,
    height=26,
    radius=12
).grid(row=1, column=0, padx=1, pady=1)

tk.Button(
    frame_visual_buttons,
    text="ⓘ",
bg="white",
fg="black",
    width=2,
    command=lambda:
    show_help(
        "Long Distance",
        "Displays long-distance arrivals."
    )
).grid(row=1, column=1)
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
    text=(
        "Barcelona Airport Simulation System\n\n"
        "Group 13\n\n"
        "Martí Vázquez\n"
        "Pablo Romero\n"
        "Paula Bautista"
    ),
    font=("Garamond", 12, "bold"),
    fg="#FF6000",
    bg=window_color
)
plane_img = Image.open(
    "DATA/plane.png"
)

plane_img = plane_img.resize(
    (50, 50)
)

plane_photo = ImageTk.PhotoImage(
    plane_img
)

plane_animation = tk.Label(
    window,
    image=plane_photo,
    bg=window_color
)

plane_animation.image = plane_photo

plane_animation.place(
    x=-60,
    y=820
)

plane_animation.lift()
plane_label.pack()

# ---------------- START ----------------

window.after(
    100,
    show_splash
)

window.mainloop()