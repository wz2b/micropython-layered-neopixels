# Neopixel Layering with Alpha Blending

## Summary

This library adds virtual layers to a NeoPixel
array using a virtual transparency (alpha) channel.
This allows you to have backgrounds as well as to have
pixel by pixel overrides that can be cleared by layer.
This is useful in cases where multiple sources can drive
the array and some of them have higher priorities than
others.

This library was primarily designed for Micropython, though
it can be used anywhere the neopixel library is implemented.

## Example

```python
import machine
from neopixel import NeoPixel
from layers import LayeredNeoPixel

pin = machine.Pin(16)

lp = LayeredNeoPixel(NeoPixel(pin), layers=4)

# example: lp.set( ledNum, r, g, b, alpha=a, layer=x)
lp.setw(1, 128, 0, 64, alpha=1.0, layer=3)

# example: set multiple pixels
lp.set(1, 0, 255, 0, alpha=0.55, layer=1)
lp.set(2, 0, 255, 0, alpha=0.55, layer=1)
lp.set(3, 0, 255, 0, alpha=0.55, layer=1)
lp.write()

# Clear layer 1 and update array
lp.relinquishw(1)

# Relinquish (clear) everything up to but not including
# the bottom layer
lp.relinquishtow(3)
```

_set()_ affects the specified layer in memory, while _setw()_
also re-computes the alpha blend then writes to the physical
neopixel array.

The _relinquish_ terminology comes from the BACnet concept of
priorities.  In BACnet, values are written to a _priority
array_ and the final output is the highest value in the priority
array that is not null.  For example, a room's temperature
setpoints can be placed into "weekend" mode, but if someone
comes into work they can set the room to "occupied" at a
higher priority.  This still allows the normal controls to
be retained even though the higher priority is currently
active.  In the case of the NeoPixel layer array, this behavior
is accomplished by always writing LEDs at an alpha of 1.0
regardless of layer.

For more traditional color blending cases transparency is set
for each pixel on each layer, then the actual color is
computed starting with the bottom and working up the layer
stack to the "top" (layer 0).  Colors are combined using
alpha blending, where alpha=1.0 is opaque (layer completely
overrides all other layers), alpha=0.0 is transparent (this
layer has no effect on the final color), and everything between
is some degree of translucency.

The default number of layers is 4, plus an implied
black background (0, 0, 0, a=1.0).

# License

This project is licensed under Apache 2.0 and is
copyright (c) 2022 Christopher Piggott.  All rights reserved.

Contributions, comments, pull requests, and issues are welcome at
https://github.com/wz2b/micropython-layered-neopixels
