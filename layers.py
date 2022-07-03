import neopixel

class LayeredNeoPixel:
    """
    Layering for NeoPixel arrays.

    This class implements layers of pixels, where layer 0 is the
    top.  Each pixel has an alpha (transparency).  The bottom
    layer is implied as black with 100% transparency (0,0,0,1.0)
    """
    def __init__(self, np: neopixel.NeoPixel, layers: int = 4):
        """
        Create a layered NeoPixel array
        :param np: the underlying (physical) neopixel array
        :param layers: number of desired layers (default 4)
        """
        # Construct the priority array
        num_leds = len(np)
        self.layers = [[None for i in range(0, layers)] for j in range(0, num_leds)]
        self.np = np
        self.current_layer = layers - 1

    def set_layer(self, layer: int):
        """
        Set the current layer
        :param layer: new current layer
        :return:
        """
        if layer < 0 or layer > len(self.layers) - 1:
            raise Exception("no such layer")
        self.current_layer = layer

    def set(self, led: int, red: int, grn: int, blu: int, alpha: float = 1.0, layer: int = -1):
        """
        Set a pixel
        :param led:
        :param red:
        :param grn:
        :param blu:
        :param alpha:
        :param layer: (defaults to bottom most layer)
        :return:
        """
        if layer == -1:
            layer = self.current_layer
        elif layer >= len(self.layers):
            raise Exception("priority does not exist")
        self.layers[led][layer] = (red, grn, blu, alpha)

    def setw(self, led: int, red: int, grn: int, blu: int, alpha: int = 1.0, layer: int = -1):
        """
        Set a pixel then update the neopixel array
        :param led:
        :param red:
        :param grn:
        :param blu:
        :param alpha:
        :param layer: (defaults to bottom most layer)
        :return:
        """
        self.set(led, red, grn, blu, alpha=alpha, layer=layer)
        self.write()

    def relinquish(self, layer: int):
        """
        Clear all values of all pixels on the specified layer
        :param layer:
        :return:
        """
        for i in range(0, len(self.layers)):
            self.layers[i][layer] = None

    def relinquishw(self, layer: int):
        """
        Clear all values of all pixels on the specified layer,
        then update the neopixel array
        :param layer:
        :return:
        """
        self.relinquish(layer)
        self.write()

    def relinquishto(self, layer: int):
        """
        Clear all layers below (but not including) the specified layer
        :param layer:
        :return:
        """
        for i in range(0, layer):
            self.relinquish(i)

    def relinquishtow(self, layer: int):
        """
        Clear all yaers below (but int including) the specified layer,
        then update the neopixel array
        :param layer:
        :return:
        """
        self.relinquishto(layer)
        self.write()

    def _alpha_blend(self, led_num: int) -> list:
        values = [x for x in self.layers[led_num] if x is not None]

        #
        # The background is solid black
        #
        r0, g0, b0, a0 = 0.0, 0.0, 0.0, 1.0

        #
        # One at a time, layer the next color
        # on top of the existing color.  This starts
        # out as the background color but changes
        # as more and more layers up the stack are
        # blended in
        #
        for layer in reversed(values):
            r1 = float(layer[0])
            g1 = float(layer[1])
            b1 = float(layer[2])
            a1 = float(layer[3]) or 1.0

            #
            # The alpha of the new pixel, but
            # don't overwrite the existing alpha
            # as we need it for the calculations
            #
            a01 = (1.0 - a1) * a0 + a1

            #
            # For each color, blend the current color
            # adjusting for the new total transparency'
            #
            r0 = ((1.0 - a1)*a0*r0 + (a1*r1)) / a01
            g0 = ((1.0 - a1)*a0*g0 + (a1*g1)) / a01
            b0 = ((1.0 - a1)*a0*b0 + (a1*b1)) / a01

            a0 = a01
        return int(r0), int(g0), int(b0)

    def write(self)
        """
        Update the neopixel array.  When updating several
        pixels at once, you can call set() multiple times
        then do a single write() to update the array, rather than
        calling setw() and forcing a hardware refresh each time.
        :return: 
        """
        for i in range(0, len(self.layers)):
            self.np[i] = self._alpha_blend(i)
        self.np.write()
