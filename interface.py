import tkinter as tk
from airport import *
from aircraft import *

# ---------------- VARIABLES ----------------

airports = []
aircrafts = []

# ---------------- FUNCIONES AIRPORTS ----------------

def load_airports():
    global airports
    airports = LoadAirports("Airports.txt")
    label.config(text="Loaded " + str(len(airports)) + " airports")

def show_airports():
    text_box.delete("1.0", tk.END)

    i = 0
    while i < len(airports):
        SetSchengen(airports[i])

        line = airports[i].ICAO + " | "
        line += "{:.4f}".format(airports[i].latitude) + " "
        line += "{:.4f}".format(airports[i].longitude)
        line += " | Schengen: " + str(airports[i].Schengen)

        text_box.insert(tk.END, line + "\n")
        i += 1

def add_airport():
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

    except:
        label.config(text="Invalid input")

def remove_airport():
    code = entry_code.get()
    result = RemoveAirport(airports, code)

    if result == 0:
        label.config(text="Airport removed")
    else:
        label.config(text="Airport not found")

def save_schengen():
    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i += 1

    result = SaveSchengenAirports(airports, "schengen.txt")

    if result == 0:
        label.config(text="Schengen airports saved")
    else:
        label.config(text="Error saving")

def plot_airports():
    if len(airports) == 0:
        label.config(text="Load airports first")
        return

    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i += 1

    PlotAirportsTk(frame_plot, airports)

def map_airports():
    if len(airports) == 0:
        label.config(text="Load airports first")
        return

    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i += 1

    MapAirports(airports)
    label.config(text="Map opened (check Google Earth)")

# ---------------- FUNCIONES AIRCRAFTS ----------------

def load_arrivals():
    global aircrafts
    aircrafts = LoadArrivals("Arrivals.txt")
    label.config(text="Loaded " + str(len(aircrafts)) + " arrivals")

def show_aircrafts():
    text_box.delete("1.0", tk.END)

    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]

        line = ac.aircraft_id + " | " + ac.company + " | "
        line += ac.origin + " | " + ac.time_landing

        text_box.insert(tk.END, line + "\n")
        i += 1

def plot_arrivals():
    if len(aircrafts) == 0:
        label.config(text="Load arrivals first")
        return

    PlotArrivalsTk(frame_plot, aircrafts)

def plot_airlines():
    if len(aircrafts) == 0:
        label.config(text="Load arrivals first")
        return

    PlotAirlinesTk(frame_plot, aircrafts)

def save_flights():
    if len(aircrafts) == 0:
        label.config(text="Load arrivals first")
        return

    result = SaveFlights(aircrafts, "flights.txt")

    if result == 0:
        label.config(text="Flights saved")
    else:
        label.config(text="Error saving flights")

# ---------------- VENTANA ----------------

window = tk.Tk()
window.title("Airport Manager V2")
window.geometry("1100x700")

# ---------------- OUTPUT ARRIBA ----------------

frame_top = tk.Frame(window)
frame_top.pack()

text_box = tk.Text(frame_top, height=12, width=130)
text_box.pack()

# ---------------- ZONA CENTRAL ----------------

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

tk.Label(frame_left, text="--- AIRPORTS ---").pack()

tk.Button(frame_left, text="Load Airports", command=load_airports).pack(fill="x")
tk.Button(frame_left, text="Show Airports", command=show_airports).pack(fill="x")
tk.Button(frame_left, text="Add Airport", command=add_airport).pack(fill="x")
tk.Button(frame_left, text="Remove Airport", command=remove_airport).pack(fill="x")
tk.Button(frame_left, text="Save Schengen", command=save_schengen).pack(fill="x")
tk.Button(frame_left, text="Plot Airports", command=plot_airports).pack(fill="x")
tk.Button(frame_left, text="Map Airports", command=map_airports).pack(fill="x")

# ---------------- AIRCRAFTS ----------------

tk.Label(frame_center, text="--- AIRCRAFTS ---").pack()

tk.Button(frame_center, text="Load Arrivals", command=load_arrivals).pack(fill="x")
tk.Button(frame_center, text="Show Aircrafts", command=show_aircrafts).pack(fill="x")
tk.Button(frame_center, text="Plot Arrivals", command=plot_arrivals).pack(fill="x")
tk.Button(frame_center, text="Plot Airlines", command=plot_airlines).pack(fill="x")
tk.Button(frame_center, text="Save Flights", command=save_flights).pack(fill="x")

# ---------------- STATUS ----------------

label = tk.Label(window, text="")
label.pack()

# ---------------- START ----------------

window.mainloop()