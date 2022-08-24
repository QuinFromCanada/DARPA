import time
import board
import math
import busio
import terminalio
import displayio
import gc9a01
from adafruit_display_text import label
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.circle import Circle

# Release any resources currently in use for the displays
displayio.release_displays()

# attempt to auto-detect board type
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
lblNORTH = label.Label(font=terminalio.FONT, text="N", color=0xFF0000, scale=1)
lblNORTH.anchor_point = (0.5, 0.5)
lblNORTH.anchored_position = (120, 10)
main.append(lblNORTH)

# EAST LABEL
lblEAST = label.Label(font=terminalio.FONT, text="E", color=0xFFD300, scale=1)
lblEAST.anchor_point = (0.5, 0.5)
lblEAST.anchored_position = (230, 120)
main.append(lblEAST)

# WEST LABEL
lblWEST = label.Label(font=terminalio.FONT, text="W", color=0xFFD300, scale=1)
lblWEST.anchor_point = (0.5, 0.5)
lblWEST.anchored_position = (10, 120)
main.append(lblWEST)

# SOUTH LABEL
lblSOUTH = label.Label(font=terminalio.FONT, text="S", color=0xF3F3F3, scale=1)
lblSOUTH.anchor_point = (0.5, 0.5)
lblSOUTH.anchored_position = (120, 230)
main.append(lblSOUTH)

# SPEED LABEL
lblSPEED = label.Label(font=terminalio.FONT, text="00", color=0xFF0000, scale=4)
lblSPEED.anchor_point = (0.5, 0.5)
lblSPEED.anchored_position = (120, 120)
main.append(lblSPEED)

# TIME LABEL
#lblTIME = label.Label(font=terminalio.FONT, text="00:00", color=0x0000FF, scale=2)
#lblTIME.anchor_point = (0.5, 0.5)
#lblTIME.anchored_position = (120, 155)
#main.append(lblTIME)


# Main loop
while True:
    # update text property to change the text showing on the display
    # updating_label.text = "Time Is:\n{}".format(time.monotonic())
    time.sleep(1)
