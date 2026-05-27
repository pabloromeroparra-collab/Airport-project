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
def update_gate_view():

    global current_hour

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

    global current_time_minutes

    current_time_minutes = (
        current_time_minutes + 30
    ) % (24 * 60)

    entry_hour.delete(0, tk.END)

    entry_hour.insert(
        0,
        GetCurrentTimeText()
    )

    update_gate_view()


def previous_hour():

    global current_time_minutes

    current_time_minutes = (
        current_time_minutes - 30
    ) % (24 * 60)

    entry_hour.delete(0, tk.END)

    entry_hour.insert(
        0,
        GetCurrentTimeText()
    )

    update_gate_view()

def run_simulation():

    global simulation_running

    if simulation_running == False:

        return

    next_hour()

    window.after(
        1000,
        run_simulation
    )
def start_simulation():

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

    show_message(
        text="Simulation started"
    )

    run_simulation()

def stop_simulation():

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

# ---------------- WINDOW ----------------

window = tk.Tk()

window_color = "#63C5DA"

window.configure(bg=window_color)

window.title("Airport and Aircraft Manager")

window.geometry("1100x900")


def show_message(text):

    text_box.delete("1.0", tk.END)

    text_box.insert(tk.END,text.upper())

    text_box.tag_add(
        "red",
        "1.0",
        tk.END
    )

    text_box.tag_config("red",foreground="red",font=("Arial", 12, "bold"))
def update_status():

    global bcn

    global aircrafts

    global current_hour

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

    text = (
        "TIME: "
        + GetCurrentTimeText()
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
    )

    try:

        status_label.config(
            text=text
        )

    except:

        return

def show_help(title, message):

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

frame_buttons = tk.Frame(frame_bottom)

frame_buttons.pack(
    side=tk.LEFT,
    fill=tk.Y,
    expand=False,
    padx=10,
    pady=10
)

frame_buttons.config(
    width=240
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
    text="Previous Hour",
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
        "Moves simulation one hour backwards."
    )
).grid(row=4, column=1)

RoundedButton(
    frame_simulation_buttons,
    text="Next Hour",
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
        "Moves simulation one hour forward."
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
        "Starts automatic hour-by-hour airport simulation."
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
    text="G13: Martí Vázquez, Pablo Romero, Paula Bautista",
    font=("Garamond", 12, "bold"),
    fg="#FF6000",
    bg=window_color
)

plane_label.pack()

# ---------------- START ----------------

window.mainloop()