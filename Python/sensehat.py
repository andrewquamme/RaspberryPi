from sense_emu import SenseHat
##from sense_hat import SenseHat

sense = SenseHat()

r = (255, 0, 0)
g = (0, 255, 0)
b = (0, 0, 255)
y = (255, 255, 0)

message = "Hi!"

##sense.set_rotation(180)
sense.show_letter("Z")
##sense.show_message(message, text_colour=blue)
##sense.clear()

sense.set_pixel(0,0,r)
pixels = [
    g,g,g,g,g,g,g,g,
    g,g,g,g,g,g,g,g,
    g,b,b,g,g,b,b,g,
    g,b,b,g,g,b,b,g,
    g,g,g,b,b,g,g,g,
    g,g,b,b,b,b,g,g,
    g,g,b,b,b,b,g,g,
    g,g,b,g,g,b,g,g
]

sense.set_pixels(pixels)
