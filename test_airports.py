from airport import *

# --------------------------------------------------
# TEST AIRPORT CLASS
# --------------------------------------------------

print("=== TEST AIRPORT CLASS ===")

airport1 = Airport("LEBL", 41.2974, 2.0833)
SetSchengen(airport1)
PrintAirport(airport1)

airport2 = Airport("KJFK", 40.6413, -73.7781)
SetSchengen(airport2)
PrintAirport(airport2)


# --------------------------------------------------
# TEST LOAD AIRPORTS
# --------------------------------------------------

print("\n=== TEST LOAD AIRPORTS ===")

airports = LoadAirports("Airports.txt")

print("Number of airports loaded:", len(airports))

i = 0
while i < len(airports) and i < 5:
    SetSchengen(airports[i])
    PrintAirport(airports[i])
    i += 1


# --------------------------------------------------
# TEST ADD AIRPORT
# --------------------------------------------------

print("\n=== TEST ADD AIRPORT ===")

new_airport = Airport("TEST", 10.0, 20.0)
SetSchengen(new_airport)

result = AddAirport(airports, new_airport)

if result == 0:
    print("Airport added correctly")
else:
    print("Airport already exists")


# --------------------------------------------------
# TEST REMOVE AIRPORT
# --------------------------------------------------

print("\n=== TEST REMOVE AIRPORT ===")

result = RemoveAirport(airports, "TEST")

if result == 0:
    print("Airport removed correctly")
else:
    print("Airport not found")


# --------------------------------------------------
# TEST SAVE SCHENGEN
# --------------------------------------------------

print("\n=== TEST SAVE SCHENGEN ===")

i = 0
while i < len(airports):
    SetSchengen(airports[i])
    i += 1

result = SaveSchengenAirports(airports, "test_schengen.txt")

if result == 0:
    print("Schengen airports saved correctly")
else:
    print("Error saving Schengen airports")


# --------------------------------------------------
# TEST PLOT
# --------------------------------------------------

print("\n=== TEST PLOT ===")

PlotAirports(airports)


# --------------------------------------------------
# TEST MAP
# --------------------------------------------------

print("\n=== TEST MAP ===")

MapAirports(airports)