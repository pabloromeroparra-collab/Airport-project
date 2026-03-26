from airport import *
import tkinter as tk

airports = []

def load_airports():
    global airports
    airports = LoadAirports("Airports.txt")
    label.config(text="Loaded " + str(len(airports)) + " airports")


def show_airports():
    if len(airports) == 0:
        label.config(text="No airports loaded")
        return

    i = 0
    output = ""

    while i < len(airports):
        SetSchengen(airports[i])
        airport = airports[i]

        line = airport.ICAO + " | " + "{:.4f}".format(airport.latitude) + " " + "{:.4f}".format(airport.longitude)
        line += " | Schengen: " + str(airport.Schengen)

        output = output + line + "\n"

        label.config(text=output)
        window.update()

        i += 1


def add_airport():
    code = entry_code.get()
    latitude = entry_lat.get()
    longitude = entry_lon.get()

    try:
        airport = Airport(code, float(latitude), float(longitude))
        SetSchengen(airport)

        result = AddAirport(airports, airport)

        if result == 0:
            label.config(text="Airport added")
        else:
            label.config(text="Airport already exists")

    except ValueError:
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
    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i += 1

    PlotAirports(airports)
    label.config(text="Plot shown")


def map_airports():
    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i += 1

    MapAirports(airports)
    label.config(text="Map created")


window = tk.Tk()
window.title("Airport Manager")
window.geometry("500x500")

# inputs

tk.Label(window, text="ICAO Code").pack()
entry_code = tk.Entry(window)
entry_code.pack()

tk.Label(window, text="Latitude").pack()
entry_lat = tk.Entry(window)
entry_lat.pack()

tk.Label(window, text="Longitude").pack()
entry_lon = tk.Entry(window)
entry_lon.pack()

# buttons (simple vertical list)

tk.Button(window, text="Load Airports", command=load_airports).pack()
tk.Button(window, text="Show Airports", command=show_airports).pack()
tk.Button(window, text="Add Airport", command=add_airport).pack()
tk.Button(window, text="Remove Airport", command=remove_airport).pack()
tk.Button(window, text="Save Schengen", command=save_schengen).pack()
tk.Button(window, text="Plot Airports", command=plot_airports).pack()
tk.Button(window, text="Map Airports", command=map_airports).pack()

# output label (simple, as you wanted)
label = tk.Label(window, text="")
label.pack()

window.mainloop()
