from airport import *
import tkinter as tk

airports = []

# --------------------------------------------------
# FUNCIONES
# --------------------------------------------------

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

        line = airport.ICAO + " | "
        line = line + "{:.4f}".format(airport.latitude) + " "
        line = line + "{:.4f}".format(airport.longitude)
        line = line + " | Schengen: " + str(airport.Schengen)

        output = output + line + "\n"

        i += 1

    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, output)


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
    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i += 1

    PlotAirportsTk(frame_plot, airports)
    label.config(text="Plot displayed in window")


def map_airports():
    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i += 1

    MapAirports(airports)
    label.config(text="Map opened in Google Earth")


# --------------------------------------------------
# VENTANA
# --------------------------------------------------

window = tk.Tk()
window.title("Airport Manager")
window.geometry("700x600")

# --------------------------------------------------
# INPUTS
# --------------------------------------------------

tk.Label(window, text="ICAO Code").pack()
entry_code = tk.Entry(window)
entry_code.pack()

tk.Label(window, text="Latitude").pack()
entry_lat = tk.Entry(window)
entry_lat.pack()

tk.Label(window, text="Longitude").pack()
entry_lon = tk.Entry(window)
entry_lon.pack()

# --------------------------------------------------
# BOTONES
# --------------------------------------------------

tk.Button(window, text="Load Airports", command=load_airports).pack()
tk.Button(window, text="Show Airports", command=show_airports).pack()
tk.Button(window, text="Add Airport", command=add_airport).pack()
tk.Button(window, text="Remove Airport", command=remove_airport).pack()
tk.Button(window, text="Save Schengen", command=save_schengen).pack()
tk.Button(window, text="Plot Airports", command=plot_airports).pack()
tk.Button(window, text="Map Airports", command=map_airports).pack()

# --------------------------------------------------
# OUTPUT TEXTO (MEJOR QUE LABEL)
# --------------------------------------------------

text_box = tk.Text(window, height=10, width=80)
text_box.pack()

# --------------------------------------------------
# FRAME PARA GRÁFICAS
# --------------------------------------------------

frame_plot = tk.Frame(window)
frame_plot.pack()

# --------------------------------------------------
# MENSAJES
# --------------------------------------------------

label = tk.Label(window, text="")
label.pack()

# --------------------------------------------------

window.mainloop()