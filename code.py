### SYSTEM IMPORTS
import time
import board
import math
import busio
import terminalio
### DISPLAY IMPORTS
import displayio
import gc9a01
from adafruit_display_text import label
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.circle import Circle
# Release any resources currently in use for the displays
displayio.release_displays()

### - GPS IMPORTS
import adafruit_gps
# Create a serial connection for the GPS connection using default speed and
# a slightly higher timeout (GPS modules typically update once a second).
# These are the defaults you should use for the GPS FeatherWing.
# For other boards set RX = GPS module TX, and TX = GPS module RX pins.
uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)

# Create a GPS module instance.
gps = adafruit_gps.GPS(uart, debug=False)  # Use UART

# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command(b"PMTK220,1000") #500 = .5s, 1000 = 1s, 2000 = 2s
# Be sure to also increase your UART timeout above!

### attempt to auto-detect board type
import os
board_type = os.uname().machine

# print(board.board_id)  # uncomment if you want to print the board id

tft_clk  = board.SCK
tft_mosi = board.MOSI
tft_rst  = board.IO12
tft_dc   = board.IO6
tft_cs   = board.IO5
tft_bl   = board.IO14
spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)
    # spi.try_lock()
    # spi.configure(baudrate=12_000_000)  # default spi is 0.25MHz on QT Py, try 12MHz
    # spi.unlock()


# Make the displayio SPI bus and the GC9A01 display
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = gc9a01.GC9A01(display_bus, width=240, height=240, backlight_pin=tft_bl)

# Make the main display context
main = displayio.Group()
display.show(main)


# ====== LABELS & shapes

# Nav Ring
navRingCircle = Circle(120, 120, 120, fill=0x000000)
main.append(navRingCircle)
mainFaceCircle = Circle(120, 120, 98, fill=0x101010, outline=0x262626)
main.append(mainFaceCircle)

# Nav Pointer
navPointerCircle = Circle(120, 54, 8, fill=0xFF0000, outline=0xA0A0A0)
main.append(navPointerCircle)

# Blanking Center
blankingCenterCircle = Circle(120, 120, 36, fill=0x000000, outline=0x000000)
main.append(blankingCenterCircle)

# NORTH LABEL
lblNORTH = label.Label(font=terminalio.FONT, text="N", color=0xFF0000, scale=2)
lblNORTH.anchor_point = (0.5, 0.5)
lblNORTH.anchored_position = (120, 10)
main.append(lblNORTH)

# EAST LABEL
lblEAST = label.Label(font=terminalio.FONT, text="E", color=0xFFD300, scale=2)
lblEAST.anchor_point = (0.5, 0.5)
lblEAST.anchored_position = (230, 120)
main.append(lblEAST)

# WEST LABEL
lblWEST = label.Label(font=terminalio.FONT, text="W", color=0xFFD300, scale=2)
lblWEST.anchor_point = (0.5, 0.5)
lblWEST.anchored_position = (10, 120)
main.append(lblWEST)

# SOUTH LABEL
lblSOUTH = label.Label(font=terminalio.FONT, text="S", color=0xF3F3F3, scale=2)
lblSOUTH.anchor_point = (0.5, 0.5)
lblSOUTH.anchored_position = (120, 230)
main.append(lblSOUTH)

# SPEED LABEL
lblSPEED = label.Label(font=terminalio.FONT, text="00", color=0xFF0000, scale=4)
lblSPEED.anchor_point = (0.5, 0.5)
lblSPEED.anchored_position = (120, 104)
main.append(lblSPEED)

# DISTANCE LABEL
lblDISTANCE = label.Label(font=terminalio.FONT, text="8"*4, color=0xFF0000, scale=2)
lblDISTANCE.anchor_point = (0.5, 0.5)
lblDISTANCE.anchored_position = (120, 136)
main.append(lblDISTANCE)



# TIME LABEL
#lblTIME = label.Label(font=terminalio.FONT, text="00:00", color=0x0000FF, scale=2)
#lblTIME.anchor_point = (0.5, 0.5)
#lblTIME.anchored_position = (120, 155)
#main.append(lblTIME)



# Print GPS info, test script
def GPSdataPrint(void):
    # Print out details about the fix like location, date, etc.
    print("=" * 40)  # Print a separator line.
    print("Fix timestamp: {:02}:{:02}:{:02}".format(
        #gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
        #gps.timestamp_utc.tm_mday,  # struct_time object that holds
        #gps.timestamp_utc.tm_year,  # the fix time.  Note you might
        gps.timestamp_utc.tm_hour,  # not get all data like year, day,
        gps.timestamp_utc.tm_min,  # month!
        gps.timestamp_utc.tm_sec,
        )
    )
    print("Latitude: {0:.6f} degrees".format(gps.latitude))
    print("Longitude: {0:.6f} degrees".format(gps.longitude))
    print("Precise Latitude: {:2.}{:2.4f} degrees".format(
        gps.latitude_degrees, gps.latitude_minutes))
    print("Precise Longitude: {:2.}{:2.4f} degrees".format(
            gps.longitude_degrees, gps.longitude_minutes)
    )
    print("Fix quality: {}".format(gps.fix_quality))
    # Some attributes beyond latitude, longitude and timestamp are optional
    # and might not be present.  Check if they're None before trying to use!
    if gps.satellites is not None:
        print("# satellites: {}".format(gps.satellites))
    if gps.altitude_m is not None:
        print("Altitude: {} meters".format(gps.altitude_m))
    if gps.speed_knots is not None:
        print("Speed: {} knots".format(gps.speed_knots))
    if gps.track_angle_deg is not None:
        print("Track angle: {} degrees".format(gps.track_angle_deg))



### --- Move compass indicator around the outside
def compass(northDeg):
    radiansN = math.radians(northDeg-90)
    northX = (120 + 110 * math.cos(radiansN))
    northY = (120 + 110 * math.sin(radiansN))

    radiansE = math.radians(northDeg)
    eastX = (120 + 110 * math.cos(radiansE))
    eastY = (120 + 110 * math.sin(radiansE))

    radiansS = math.radians(northDeg+90)
    southX = (120 + 110 * math.cos(radiansS))
    southY = (120 + 110 * math.sin(radiansS))

    radiansW = math.radians(northDeg+180)
    westX = (120 + 110 * math.cos(radiansW))
    westY = (120 + 110 * math.sin(radiansW))

    #print("Deg:{},X:{},Y:{}".format(northDeg, int(northX),int(northY)))  #math test output
    lblNORTH.anchored_position = (northX, northY)
    lblEAST.anchored_position = (eastX, eastY)
    lblSOUTH.anchored_position = (southX, southY)
    lblWEST.anchored_position = (westX, westY)



### --- Move heading indicator
def CalcHeading(lat1, long1, lat2, long2, NorthAngle):
    #const y = Math.sin(λ2-λ1) * Math.cos(φ2);
    y = math.sin(long2-long1) * math.cos(lat2)
    #const x = Math.cos(φ1)*Math.sin(φ2) - Math.sin(φ1)*Math.cos(φ2)*Math.cos(λ2-λ1);
    x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(long2-long1)
    #const θ = Math.atan2(y, x);
    angle = math.atan2(y, x)
    #const brng = (θ*180/Math.PI + 360) % 360; // in degrees
    bearing = (angle*180/math.pi + 360) % 360
    print("bearing: {}".format(bearing))


    # Updates the heading display circle
    radiansHeading = math.radians(bearing-90+NorthAngle)
    headingX = (110 + 76 * math.cos(radiansHeading)) #Not sure why i have to use 110 and not 120
    headingY = (110 + 76 * math.sin(radiansHeading)) #Not sure why i have to use 110 and not 120

    navPointerCircle.x = int(headingX)
    navPointerCircle.y = int(headingY)



# ‘haversine’ formula for finding distance between 2 points
def CalcDistance(Lat1, Long1, Lat2, Long2):
    R = 6372.8 # this is in km.  For miles use 3959.87433

    dLat = math.radians(Lat2 - Lat1)
    dLon = math.radians((Long2 - Long1))
    lat1 = math.radians(Lat1)
    lat2 = math.radians(Lat2)

    a = math.sin(dLat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dLon/2)**2
    c = 2*math.asin(math.sqrt(a))

    calculatedDistance = R*c
    print("distance: {}" .format(calculatedDistance))

    # if the distance is more then 1000m show K for KM, if its under 1k show distance in meters
    if calculatedDistance >= 1000:
        calculatedDistance = "{}K".format(int(calculatedDistance/1000))
        lblDISTANCE.color=0xFF0000
    elif calculatedDistance < 1:
        calculatedDistance = "{}m".format(int(calculatedDistance*1000))
        lblDISTANCE.color = 0x00FF00
    else:
        calculatedDistance = "{}".format(int(calculatedDistance))
        lblDISTANCE.color=0xFF0000

    lblDISTANCE.text = calculatedDistance



### -------- MAIN LOOP ---------------


# Main loop GPS update every second.
last_print = time.monotonic()
headingDeg = 0

# Main loop
while True:

    gps.update()
    # Every second print out current location details if there's a fix.
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current

        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            print("Waiting for fix...")
            print("# satellites: {}".format(gps.satellites))
            continue
        # We have a fix! (gps.has_fix is true)

        lat1 = (gps.latitude)
        long1 = (gps.longitude)

        ### --- Distance Test Points, use https://www.movable-type.co.uk/scripts/latlong.html to verify
        ## - CN tower test co-ordinence
        lat2 = 43.6426
        long2 = -79.3871

        ## - Sydney Opera House test co-ordinence
        #lat2 = -33.8568
        #long2 = -151.2153

        print("-----")
        if gps.track_angle_deg is not None:
            NorthAngle = int(gps.track_angle_deg)
            compass(NorthAngle)
        else:
            NorthAngle = 0
        print("North A:{}".format(NorthAngle))

        CalcDistance(lat1, long1, lat2, long2)
        CalcHeading(lat1, long1, lat2, long2, NorthAngle)



