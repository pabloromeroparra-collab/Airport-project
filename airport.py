import matplotlib.pyplot as plt
import os
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Airport:
    def __init__(self, ICAO, latitude, longitude):
        self.ICAO = ICAO
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.Schengen = False


# --------------------------------------------------
# SCHENGEN
# --------------------------------------------------

def IsSchengenAirport(code):
    if code == "":
        return False

    prefix = code[0:2]

    array = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG',
             'EH', 'LH', 'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP',
             'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']

    found = False
    i = 0

    while i < len(array) and found == False:
        if prefix == array[i]:
            found = True
        else:
            i = i + 1

    return found


def SetSchengen(airport):
    airport.Schengen = IsSchengenAirport(airport.ICAO)
    return airport.Schengen


# --------------------------------------------------
# PRINT
# --------------------------------------------------

def PrintAirport(airport):
    print("Code:", airport.ICAO)
    print("Coordinates:", airport.latitude, ",", airport.longitude)
    print("Schengen:", airport.Schengen)


# --------------------------------------------------
# LOAD AIRPORTS
# --------------------------------------------------

def LoadAirports(filename):
    airports = []

    try:
        file = open(filename, "r")
    except:
        return []

    # saltar cabecera
    line = file.readline()

    line = file.readline()

    while line != "":
        parts = line.split()

        if len(parts) >= 3:

            code = parts[0]

            # LATITUD
            coord_sign = parts[1][0]
            coord = parts[1][1:]

            deg = int(coord[0:2])
            min_ = int(coord[2:4])
            sec = int(coord[4:6])

            latitude = deg + min_ / 60 + sec / 3600

            if coord_sign == 'S':
                latitude = -latitude

            # LONGITUD
            coord_sign = parts[2][0]
            coord = parts[2][1:]

            deg = int(coord[0:3])
            min_ = int(coord[3:5])
            sec = int(coord[5:7])

            longitude = deg + min_ / 60 + sec / 3600

            if coord_sign == 'W':
                longitude = -longitude

            airport = Airport(code, latitude, longitude)
            airports.append(airport)

        line = file.readline()

    file.close()
    return airports


# --------------------------------------------------
# SAVE SCHENGEN
# --------------------------------------------------

def SaveSchengenAirports(airports, filename):

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

            # LAT
            if latitude >= 0:
                lat_dir = "N"
            else:
                lat_dir = "S"
                latitude = -latitude

            lat_deg = int(latitude)
            lat_min = int((latitude - lat_deg) * 60)
            lat_sec = int((((latitude - lat_deg) * 60) - lat_min) * 60)

            lat_text = lat_dir + str(lat_deg).zfill(2) + str(lat_min).zfill(2) + str(lat_sec).zfill(2)

            # LON
            if longitude >= 0:
                lon_dir = "E"
            else:
                lon_dir = "W"
                longitude = -longitude

            lon_deg = int(longitude)
            lon_min = int((longitude - lon_deg) * 60)
            lon_sec = int((((longitude - lon_deg) * 60) - lon_min) * 60)

            lon_text = lon_dir + str(lon_deg).zfill(3) + str(lon_min).zfill(2) + str(lon_sec).zfill(2)

            file.write(airports[i].ICAO + " " + lat_text + " " + lon_text + "\n")
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

    i = 0
    found = False

    while i < len(airports) and found == False:
        if airports[i].ICAO == code:
            found = True
        else:
            i = i + 1

    if found:
        airports[i:i+1] = []
        return 0
    else:
        return -1


# --------------------------------------------------
# PLOT (VERSIÓN NORMAL)
# --------------------------------------------------

def PlotAirports(airports):

    contador_schengen = 0
    contador_no_schengen = 0

    i = 0
    while i < len(airports):
        if airports[i].Schengen:
            contador_schengen = contador_schengen + 1
        else:
            contador_no_schengen = contador_no_schengen + 1
        i = i + 1

    fig, ax = plt.subplots()

    ax.bar("Airports", contador_schengen, label="Schengen")
    ax.bar("Airports", contador_no_schengen,
           bottom=contador_schengen, label="No Schengen")

    ax.set_ylabel("Count")
    ax.set_title("Schengen Airports")
    ax.legend()

    plt.show()


# --------------------------------------------------
# PLOT EN TKINTER
# --------------------------------------------------

def PlotAirportsTk(frame, airports):

    contador_schengen = 0
    contador_no_schengen = 0

    i = 0
    while i < len(airports):
        if airports[i].Schengen:
            contador_schengen = contador_schengen + 1
        else:
            contador_no_schengen = contador_no_schengen + 1
        i = i + 1

    # limpiar frame
    for widget in frame.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(5, 4))
    ax = fig.add_subplot(111)

    ax.bar(["Airports"], [contador_schengen], label="Schengen")
    ax.bar(["Airports"], [contador_no_schengen],
           bottom=[contador_schengen], label="No Schengen")

    ax.set_ylabel("Count")
    ax.set_title("Schengen Airports")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


# --------------------------------------------------
# MAP (KML)
# --------------------------------------------------

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        os.system("xdg-open " + filename)


def MapAirports(airports):

    filename = "airports.kml"

    file = open(filename, "w")

    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    file.write('<Document>\n')

    file.write('<Style id="schengen">\n')
    file.write('<IconStyle><color>ff00ff00</color></IconStyle>\n')
    file.write('</Style>\n')

    file.write('<Style id="noschengen">\n')
    file.write('<IconStyle><color>ff0000ff</color></IconStyle>\n')
    file.write('</Style>\n')

    i = 0
    while i < len(airports):

        if airports[i].Schengen:
            style = "#schengen"
        else:
            style = "#noschengen"

        file.write('<Placemark>\n')
        file.write('<name>' + airports[i].ICAO + '</name>\n')
        file.write('<styleUrl>' + style + '</styleUrl>\n')
        file.write('<Point>\n')
        file.write('<coordinates>\n')
        file.write(str(airports[i].longitude) + "," + str(airports[i].latitude) + "\n")
        file.write('</coordinates>\n')
        file.write('</Point>\n')
        file.write('</Placemark>\n')

        i = i + 1

    file.write('</Document>\n')
    file.write('</kml>\n')

    file.close()

    open_file(filename)