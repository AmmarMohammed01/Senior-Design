import src.config.pcb_global_variables as gv

try:
    import board
    import neopixel
    gv.LIGHTS_AVAILABLE = True

    # Configuration
    PIXEL_PIN_TOP = board.D18   # GPIO18 - Top Ringlight
    PIXEL_PIN_BOTTOM = board.D12 # GPIO12 - Bottom Ringlight
    NUM_PIXELS = 16
    BRIGHTNESS = 0.3        # 0.0 to 1.0

    # Color constants
    WHITE_COLOR = (255,255,255)
    NO_COLOR = (0,0,0)

    # Initialize NeoPixel
    top_pixels = neopixel.NeoPixel(
        PIXEL_PIN_TOP,
        NUM_PIXELS,
        brightness=BRIGHTNESS,
        auto_write=False
    )

    bottom_pixels = neopixel.NeoPixel(
        PIXEL_PIN_BOTTOM,
        NUM_PIXELS,
        brightness=BRIGHTNESS,
        auto_write=False
    )

    def turn_on(light_name: str):
        '''Light name = "top" or "bottom"'''
        if light_name == "top":
            top_pixels.fill(WHITE_COLOR)
            top_pixels.show()
        elif light_name == "bottom":
            bottom_pixels.fill(WHITE_COLOR)
            bottom_pixels.show()


    def turn_off(light_name: str):
        '''Light name = "top" or "bottom"'''
        if light_name == "top":
            top_pixels.fill(NO_COLOR)
            top_pixels.show()
        elif light_name == "bottom":
            bottom_pixels.fill(NO_COLOR)
            bottom_pixels.show()


    def toggle_light(light_name: str) -> None:
        '''Toggle the light'''
        if light_name == "top":
            gv.TOP_LIGHT_ON = not gv.TOP_LIGHT_ON

        elif light_name == "bottom":
            gv.BOTTOM_LIGHT_ON = not gv.BOTTOM_LIGHT_ON

        if gv.TOP_LIGHT_ON:
            turn_on("top")
            turn_off("bottom")

        elif gv.BOTTOM_LIGHT_ON:
            turn_on("bottom")
            turn_off("top")

except (ImportError, ModuleNotFoundError):
    gv.LIGHTS_AVAILABLE = False
    print("Could not find 'board' and 'neopixel' Python libraries to setup lighting")

