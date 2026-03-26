import matplotlib.pyplot as plt
import os


class Airport:
    def __init__(self, ICAO, latitude, longitude):
        self.ICAO = ICAO
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.Schengen = False


def IsSchengenAirport(code):
    if code == "":
        return False

    prefix = code[0:2]
    array = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG',
             'EH', 'LH', 'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP',
             'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
    found = False
    i = 0

    while i < len(array) and not found:
        if prefix == array[i]:
            found = True
        else:
            i += 1
    return found


def SetSchengen(airport):
    airport.Schengen = IsSchengenAirport(airport.ICAO)
    return airport.Schengen


def PrintAirport(airport):
    print("Code: ", airport.ICAO)
    print("Coordinates: ", airport.longitude, " , ", airport.latitude)
    print("Schengen:", airport.Schengen)


def LoadAirports(filename):
    airports = []

    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        return []

    i = 1
    while i < len(lines):

        parts = lines[i].split()

        if len(parts) >= 3:

            code = parts[0]

            # LATITUDE
            coord_sign = parts[1][0]
            coord = parts[1][1:]

            deg = int(coord[0:2])
            min_ = int(coord[2:4])
            sec = int(coord[4:6])

            latitude = deg + min_ / 60 + sec / 3600
            if coord_sign == 'S':
                latitude = -latitude

            # LONGITUDE
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

        i += 1

    return airports


def SaveSchengenAirports(airports, filename):
    if len(airports) == 0:
        return -1

    with open(filename, "w") as file:
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

            i += 1

    if written:
        return 0
    else:
        return -1


def AddAirport(airports, airport):
    i = 0
    found = False

    while i < len(airports) and not found:
        if airports[i].ICAO == airport.ICAO:
            found = True
        else:
            i += 1

    if not found:
        airports.append(airport)
        return 0
    else:
        return -1


def RemoveAirport(airports, code):
    i = 0
    found = False

    while i < len(airports) and not found:
        if airports[i].ICAO == code:
            found = True
        else:
            i += 1

    if found:
        airports[i:i + 1] = []
        return 0
    else:
        return -1


def PlotAirports(airports):
    contador_schengen = 0
    contador_no_schengen = 0

    for airport in airports:
        if airport.Schengen:
            contador_schengen += 1
        else:
            contador_no_schengen += 1

    fig, ax = plt.subplots()

    ax.bar("Airports", contador_schengen, label="Schengen", color="steelblue")
    ax.bar("Airports", contador_no_schengen, bottom=contador_schengen,
           label="No Schengen", color="#1D9A6C")

    ax.set_ylabel("Count")
    ax.set_title("Schengen Airports")
    ax.legend()

    plt.show()


def MapAirports(airports):
    filename = "airports.kml"

    with open(filename, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write('<Document>\n')

        f.write('<Style id="schengen">\n')
        f.write('<IconStyle>\n')
        f.write('<color>ff00ff00</color>\n')
        f.write('</IconStyle>\n')
        f.write('</Style>\n')

        f.write('<Style id="noschengen">\n')
        f.write('<IconStyle>\n')
        f.write('<color>ff0000ff</color>\n')
        f.write('</IconStyle>\n')
        f.write('</Style>\n')

        for airport in airports:
            if airport.Schengen:
                style = "#schengen"
            else:
                style = "#noschengen"

            f.write('  <Placemark>\n')
            f.write(f'<name>{airport.ICAO}</name>\n')
            f.write(f'<styleUrl>{style}</styleUrl>\n')
            f.write('<Point>\n')
            f.write('<coordinates>\n')
            f.write(f'{airport.longitude},{airport.latitude}\n')
            f.write('</coordinates>\n')
            f.write('</Point>\n')
            f.write('</Placemark>\n')

        f.write('</Document>\n')
        f.write('</kml>\n')

    os.startfile(filename)
