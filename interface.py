from airport import *

airports = []

def load_airports():
    global airports
    airports = LoadAirports("Airports.txt")
    label.config(print("Loaded ", {len(airports)}, " airports"))

def show_airports():
    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        airport = airports[i]
        print(airport.ICAO, " | ", airport.latitude, " ", airport.longitude, " | Schengen: ", airport.Schengen, "\n")
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
            label.config(print("Airport added"))
        else:
            label.config(print("Airport already exists"))

    except ValueError:
        label.config(print("Invalid input"))


def remove_airport():
    code = entry_code.get()
    result = RemoveAirport(airports, code)

    if result == 0:
        label.config(print("Airport removed"))
    else:
        label.config(print("Airport not found"))


def save_schengen():
    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i += 1


result = SaveSchengenAirports(airports, "schengen.txt")

if result == 0:
    print("Saved Schengen airports")
else:
    print("Error saving")


def plot_airports():
    i = 0
    while i<len(airports):
        SetSchengen(airports[i])
        i+=1

    PlotAirports(airports)

def map_airports():
    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i += 1

    MapAirports(airports)


window = tk.Tk()
window.title("Airport Manager")
window.geometry("550x550")

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

# buttons

tk.Button(window, text="Load Airports", command=load_airports).pack(pady=5)
tk.Button(window, text="Show Airports", command=show_airports).pack(pady=5)
tk.Button(window, text="Add Airport", command=add_airport).pack(pady=5)
tk.Button(window, text="Remove Airport", command=remove_airport).pack(pady=5)
tk.Button(window, text="Save Schengen", command=save_schengen).pack(pady=5)
tk.Button(window, text="Plot Airports", command=plot_airports).pack(pady=5)
tk.Button(window, text="Map Airports", command=map_airports).pack(pady=5)

text = tk.Text(window, height=15)
text.pack()

label = tk.Label(window, text="")
label.pack()

window.mainloop()
