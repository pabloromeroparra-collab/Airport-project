from aircraft import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# --------------------------------------------------
# CLASS GATE
# --------------------------------------------------

class Gate:

    def __init__(self, name):

        self.name = name

        self.occupied = False

        self.aircraft = ""


# --------------------------------------------------
# CLASS BOARDING AREA
# --------------------------------------------------

class BoardingArea:

    def __init__(self, name, area_type):

        self.name = name

        self.type = area_type

        self.gates = []


# --------------------------------------------------
# CLASS TERMINAL
# --------------------------------------------------

class Terminal:

    def __init__(self, name):

        self.name = name

        self.boarding_areas = []

        self.airlines = []


# --------------------------------------------------
# CLASS BARCELONA AIRPORT
# --------------------------------------------------

class BarcelonaAP:

    def __init__(self, code):

        self.code = code

        self.terminals = []


# --------------------------------------------------
# SET GATES
# --------------------------------------------------

def SetGates(area, init_gate, end_gate, prefix):

    if end_gate <= init_gate:

        return -1

    area.gates = []

    gate_number = init_gate

    while gate_number <= end_gate:

        gate_name = prefix + str(gate_number)

        gate = Gate(gate_name)

        area.gates.append(gate)

        gate_number = gate_number + 1

    return 0


# --------------------------------------------------
# LOAD AIRLINES
# --------------------------------------------------
def LoadAirlines(terminal, t_name):

    filename = "DATA/" + t_name + "_Airlines.txt"

    try:

        file = open(filename, "r")

    except:

        return -1

    terminal.airlines = []

    line = file.readline()

    while line != "":

        parts = line.split()

        if len(parts) > 0:

            airline = parts[len(parts) - 1]

            terminal.airlines.append(
                airline
            )

        line = file.readline()

    file.close()

    return 0


# --------------------------------------------------
# LOAD AIRPORT STRUCTURE
# --------------------------------------------------

def LoadAirportStructure(filename):

    try:

        file = open(filename, "r")

    except:

        return -1

    first_line = file.readline()

    first_parts = first_line.split()

    airport_code = first_parts[0]

    bcn = BarcelonaAP(airport_code)

    line = file.readline()

    while line != "":

        parts = line.split()


        if len(parts) > 0:

            if parts[0] == "Terminal":

                terminal_name = parts[1]

                terminal = Terminal(
                    terminal_name
                )

                LoadAirlines(
                    terminal,
                    terminal_name
                )

                number_areas = int(parts[2])

                count = 0

                while count < number_areas:

                    line = file.readline()

                    while line != "" and len(line.split()) < 7:
                        line = file.readline()

                    if line == "":
                        break

                    area_parts = line.split()

                    area_name = area_parts[1]

                    area_type = area_parts[2]

                    init_gate = int(
                        area_parts[4]
                    )

                    end_gate = int(
                        area_parts[6]
                    )

                    area = BoardingArea(
                        area_name,
                        area_type
                    )

                    prefix = (
                        terminal_name
                        + area_name
                        + "G"
                    )

                    SetGates(
                        area,
                        init_gate,
                        end_gate,
                        prefix
                    )

                    terminal.boarding_areas.append(
                        area
                    )

                    count = count + 1

                bcn.terminals.append(
                    terminal
                )

        line = file.readline()

    file.close()

    return bcn


# --------------------------------------------------
# GATE OCCUPANCY
# --------------------------------------------------

def GateOccupancy(bcn):

    occupancy = []

    i = 0

    while i < len(bcn.terminals):

        terminal = bcn.terminals[i]

        j = 0

        while j < len(
            terminal.boarding_areas
        ):

            area = terminal.boarding_areas[j]

            k = 0

            while k < len(area.gates):

                gate = area.gates[k]

                line = gate.name + " | "

                line += str(gate.occupied)

                line += " | "

                line += gate.aircraft

                occupancy.append(line)

                k = k + 1

            j = j + 1

        i = i + 1

    return occupancy


# --------------------------------------------------
# IS AIRLINE IN TERMINAL
# --------------------------------------------------
def IsAirlineInTerminal(
    terminal,
    airline
):

    i = 0

    found = False

    while i < len(terminal.airlines) and found == False:

        terminal_airline = (
            terminal.airlines[i]
        ).strip()

        aircraft_airline = (
            airline
        ).strip()

        if terminal_airline == aircraft_airline:

            found = True

        else:

            i = i + 1

    return found
# --------------------------------------------------
# SEARCH TERMINAL
# --------------------------------------------------

def SearchTerminal(bcn, airline):

    i = 0

    found = False

    terminal = None

    while i < len(bcn.terminals) and found == False:

        if IsAirlineInTerminal(
            bcn.terminals[i],
            airline
        ):

            terminal = bcn.terminals[i]

            found = True

        else:

            i = i + 1

    return terminal


# --------------------------------------------------
# ASSIGN GATE
# --------------------------------------------------

def AssignGate(bcn, aircraft):

    terminal = SearchTerminal(
        bcn,
        aircraft.company
    )

    if terminal == None:

        return -1

    flight_schengen = IsSchengenAirport(
        aircraft.origin
    )

    i = 0

    assigned = False

    while i < len(
        terminal.boarding_areas
    ) and assigned == False:

        area = terminal.boarding_areas[i]

        correct_area = False

        if flight_schengen:

            if area.type == "Schengen":

                correct_area = True

        else:

            if area.type == "non-Schengen":

                correct_area = True

        if correct_area:

            j = 0

            while j < len(area.gates) and assigned == False:

                gate = area.gates[j]

                if gate.occupied == False:
                    gate.occupied = True

                    gate.aircraft = (
                        aircraft.aircraft_id
                    )

                    assigned = True

                j = j + 1

        i = i + 1

    if assigned:

        return 0

    else:

        return -1

# --------------------------------------------------
# PLOT DAY OCCUPANCY
# --------------------------------------------------

def PlotDayOccupancy(
    frame,
    bcn,
    aircrafts
):

    """
    Plots gate occupancy
    during the whole day.

    Parameters:
        frame
        bcn
        aircrafts (list)

    Returns:
        None
    """

    ResetGates(bcn)

    hours = []

    occupied_counts = []

    unassigned_counts = []

    hour = 0

    while hour < 24:

        time_text = (
            str(hour).zfill(2)
            + ":00"
        )

        not_assigned = (
            AssignGatesAtTime(
                bcn,
                aircrafts,
                time_text
            )
        )

        occupied = 0

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

                    if gate.occupied:

                        occupied = (
                            occupied + 1
                        )

                    k = k + 1

                j = j + 1

            i = i + 1

        hours.append(hour)

        occupied_counts.append(
            occupied
        )

        unassigned_counts.append(
            not_assigned
        )

        hour = hour + 1

    widgets = frame.winfo_children()

    i = 0

    while i < len(widgets):

        widgets[i].destroy()

        i = i + 1

    fig = Figure(figsize=(10, 5))

    ax = fig.add_subplot(111)

    ax.plot(
        hours,
        occupied_counts,
        marker="o",
        label="Occupied gates"
    )

    ax.plot(
        hours,
        unassigned_counts,
        marker="o",
        label="Unassigned aircraft"
    )

    ax.set_title(
        "Airport Occupancy During Day"
    )

    ax.set_xlabel(
        "Hour"
    )

    ax.set_ylabel(
        "Aircraft"
    )

    ax.legend()

    ax.grid(True)

    canvas = FigureCanvasTkAgg(
        fig,
        master=frame
    )

    canvas.draw()

    canvas.get_tk_widget().pack()
# --------------------------------------------------
# FREE GATE
# --------------------------------------------------

def FreeGate(bcn, aircraft_id):

    """
    Frees the gate occupied
    by one aircraft.

    Parameters:
        bcn
        aircraft_id (str)

    Returns:
        int
    """

    i = 0

    found = False

    while (
        i < len(bcn.terminals)
        and found == False
    ):

        terminal = bcn.terminals[i]

        j = 0

        while (
            j < len(
                terminal.boarding_areas
            )
            and found == False
        ):

            area = terminal.boarding_areas[j]

            k = 0

            while (
                k < len(area.gates)
                and found == False
            ):

                gate = area.gates[k]

                if (
                    gate.aircraft
                    ==
                    aircraft_id
                ):

                    gate.occupied = False

                    gate.aircraft = ""

                    found = True

                k = k + 1

            j = j + 1

        i = i + 1

    if found:

        return 0

    else:

        return -1

# --------------------------------------------------
# ASSIGN GATES AT TIME
# --------------------------------------------------

def AssignGatesAtTime(
    bcn,
    aircrafts,
    time
):

    """
    Assigns gates dynamically
    during one hour period.

    Parameters:
        bcn
        aircrafts (list)
        time (str)

    Returns:
        int
    """

    not_assigned = 0

    start_hour = int(
        time.split(":")[0]
    )

    end_hour = start_hour + 1

    # --------------------------------
    # FREE DEPARTED AIRCRAFT
    # --------------------------------

    i = 0

    while i < len(aircrafts):

        aircraft = aircrafts[i]

        if aircraft.time_departure != "":

            dep_hour = int(
                aircraft.time_departure.split(":")[0]
            )

            if dep_hour < end_hour:

                FreeGate(
                    bcn,
                    aircraft.aircraft_id
                )

        i = i + 1

    # --------------------------------
    # ASSIGN NEW ARRIVALS
    # --------------------------------

    i = 0

    while i < len(aircrafts):

        aircraft = aircrafts[i]

        if aircraft.time_landing != "":

            arr_hour = int(
                aircraft.time_landing.split(":")[0]
            )

            inside_period = False

            if (
                arr_hour >= start_hour
                and
                arr_hour < end_hour
            ):

                inside_period = True

            if inside_period:

                result = AssignGate(
                    bcn,
                    aircraft
                )

                if result != 0:

                    not_assigned = (
                        not_assigned + 1
                    )

        i = i + 1

    return not_assigned
# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    bcn = LoadAirportStructure(
        "DATA/LEBL.txt"
    )

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

    i = 0

    while i < len(aircrafts):

        AssignGate(
            bcn,
            aircrafts[i]
        )

        i = i + 1

    occupancy = GateOccupancy(bcn)

    i = 0

    while i < len(occupancy):

        print(occupancy[i])

        i = i + 1
    FreeGate(
        bcn,
        aircrafts[0].aircraft_id
    )

    print(
        "Gate freed"
    )
    ResetGates(bcn)

    not_assigned = AssignGatesAtTime(
        bcn,
        aircrafts,
        "10:00"
    )

    print(
        "Not assigned:",
        not_assigned
    )

    occupancy = GateOccupancy(
        bcn
    )

    i = 0

    while i < len(occupancy):
        print(occupancy[i])

        i = i + 1

# --------------------------------------------------
# PLOT GATE OCCUPANCY TK
# --------------------------------------------------

def PlotGateOccupancyTk(frame, bcn):

    occupied = 0

    free = 0

    i = 0

    while i < len(bcn.terminals):

        terminal = bcn.terminals[i]

        j = 0

        while j < len(
            terminal.boarding_areas
        ):

            area = terminal.boarding_areas[j]

            k = 0

            while k < len(area.gates):

                gate = area.gates[k]

                if gate.occupied:

                    occupied = occupied + 1

                else:

                    free = free + 1

                k = k + 1

            j = j + 1

        i = i + 1

    widgets = frame.winfo_children()

    i = 0

    while i < len(widgets):

        widgets[i].destroy()

        i = i + 1

    fig = Figure(figsize=(5, 4))

    ax = fig.add_subplot(111)

    labels = [
        "Occupied",
        "Free"
    ]

    values = [
        occupied,
        free
    ]

    ax.bar(labels, values)

    ax.set_title(
        "Gate Occupancy"
    )

    ax.set_ylabel(
        "Number of gates"
    )

    canvas = FigureCanvasTkAgg(
        fig,
        master=frame
    )

    canvas.draw()

    canvas.get_tk_widget().pack()

# --------------------------------------------------
# SHOW GATE ASSIGNMENTS
# --------------------------------------------------

def ShowGateAssignments(bcn):

    lines = []

    i = 0

    while i < len(bcn.terminals):

        terminal = bcn.terminals[i]

        j = 0

        while j < len(
            terminal.boarding_areas
        ):

            area = terminal.boarding_areas[j]

            k = 0

            while k < len(area.gates):

                gate = area.gates[k]

                if gate.occupied:

                    line = gate.aircraft

                    line += " -> "

                    line += gate.name

                    lines.append(line)

                k = k + 1

            j = j + 1

        i = i + 1

    return lines

# --------------------------------------------------
# RESET GATES
# --------------------------------------------------

def ResetGates(bcn):

    i = 0

    while i < len(bcn.terminals):

        terminal = bcn.terminals[i]

        j = 0

        while j < len(
            terminal.boarding_areas
        ):

            area = terminal.boarding_areas[j]

            k = 0

            while k < len(area.gates):

                gate = area.gates[k]

                gate.occupied = False

                gate.aircraft = ""

                k = k + 1

            j = j + 1

        i = i + 1

# --------------------------------------------------
# PLOT GATE DISTRIBUTION
# --------------------------------------------------

def PlotGateDistributionTk(
    frame,
    bcn
):

    widgets = frame.winfo_children()

    i = 0

    while i < len(widgets):

        widgets[i].destroy()

        i = i + 1

    fig = Figure(figsize=(10, 6))

    ax = fig.add_subplot(111)

    y = 0

    i = 0

    while i < len(bcn.terminals):

        terminal = bcn.terminals[i]

        j = 0

        while j < len(
            terminal.boarding_areas
        ):

            area = terminal.boarding_areas[j]

            k = 0

            while k < len(area.gates):

                gate = area.gates[k]

                x = k

                if gate.occupied:

                    color = "red"

                else:

                    color = "green"

                rect = plt.Rectangle(
                    (x, y),
                    1,
                    1,
                    color=color
                )

                ax.add_patch(rect)

                ax.text(
                    x + 0.5,
                    y + 0.5,
                    gate.name,
                    ha="center",
                    va="center",
                    fontsize=6
                )

                k = k + 1

            label = (
                terminal.name
                + "-"
                + area.name
            )

            ax.text(
                -2,
                y + 0.5,
                label,
                fontsize=10
            )

            y = y + 2

            j = j + 1

        i = i + 1

    ax.set_xlim(0, 20)

    ax.set_ylim(0, y)

    ax.set_aspect("equal")

    ax.axis("off")

    ax.set_title(
        "Gate Distribution"
    )

    canvas = FigureCanvasTkAgg(
        fig,
        master=frame
    )

    canvas.draw()

    canvas.get_tk_widget().pack()

# --------------------------------------------------
# GATES VIEWER
# --------------------------------------------------

def PlotGateStateTk(
    frame,
    bcn,
    aircrafts,
    time,
    selected_gates
):

    """
    Draws selected gates
    with occupancy colors.

    Parameters:
        frame
        bcn
        aircrafts
        time
        selected_gates

    Returns:
        None
    """

    ResetGates(bcn)

    AssignGatesAtTime(
        bcn,
        aircrafts,
        time
    )

    widgets = frame.winfo_children()

    i = 0

    while i < len(widgets):

        widgets[i].destroy()

        i = i + 1

    fig = Figure(figsize=(12, 6))

    ax = fig.add_subplot(111)

    fig.patch.set_facecolor("white")

    ax.set_facecolor("#f0f0f0")

    gate_count = 0

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

                if gate.name in selected_gates:

                    col = gate_count % 8

                    row = gate_count // 8

                    x = col * 2

                    y = -row * 2

                    if gate.occupied:

                        color = "red"

                    else:

                        color = "limegreen"

                    rect = plt.Rectangle(
                        (x, y),
                        1.5,
                        1.2,
                        facecolor=color,
                        edgecolor="black"
                    )

                    ax.add_patch(rect)

                    text = gate.name

                    if gate.aircraft != "":
                        text += "\n"

                        text += gate.aircraft

                    ax.text(
                        x + 0.75,
                        y + 0.6,
                        text,
                        ha="center",
                        va="center",
                        fontsize=7,
                        color="black"
                    )

                    gate_count = (
                            gate_count + 1
                    )

                k = k + 1

            j = j + 1

        i = i + 1

    ax.set_title(
        "Gate Occupancy at "
        + time
    )
    ax.set_xlim(-1, 16)

    rows = (
                   gate_count // 8
           ) + 1

    ax.set_ylim(
        -rows * 2,
        2
    )
    ax.axis("off")

    canvas = FigureCanvasTkAgg(
        fig,
        master=frame
    )

    canvas.draw()

    canvas.get_tk_widget().pack()