#!/usr/bin/env python
# -*- encoding: utf-8 -#-

'''
report_pos_inch.py

Run this demo by calling: python report_pos_inch.py

Prints X.XXX, Y.YYY, where
X.XXX is the current AxiDraw X position and
Y.YYY is the current AxiDraw Y position, in inch units.

Requires Python 3.6 or newer and the AxiDraw python API, version 3.2 or newer.

AxiDraw python API documentation is hosted at: https://axidraw.com/doc/py_api/




About this software:

The AxiDraw writing and drawing machine is a product of Evil Mad Scientist
Laboratories. https://axidraw.com   https://shop.evilmadscientist.com

This open source software is written and maintained by Evil Mad Scientist
to support AxiDraw users across a wide range of applications. Please help
support Evil Mad Scientist and open source software development by purchasing
genuine AxiDraw hardware.

AxiDraw software development is hosted at https://github.com/evil-mad/axidraw

Additional AxiDraw documentation is available at http://axidraw.com/docs

AxiDraw owners may request technical support for this software through our
github issues page, support forums, or by contacting us directly at:
https://shop.evilmadscientist.com/contact





Copyright 2022 Windell H. Oskay, Evil Mad Scientist Laboratories

The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

from pyaxidraw import axidraw

ad = axidraw.AxiDraw() # Initialize class
ad.interactive()
ad.connect()  # Open USB serial session
if not ad.connected:
    exit()

result = ad.usb_query('QS\r') # Query global step position
result_list = result.strip().split(",")
a_pos, b_pos = int(result_list[0]), int(result_list[1])

x_pos_inch = (a_pos + b_pos) / (4 * ad.params.native_res_factor)
y_pos_inch = (a_pos - b_pos) / (4 * ad.params.native_res_factor)
if ad.options.resolution == 2:  # Low-resolution mode
    x_pos_inch *= 2
    y_pos_inch *= 2

print("{0:0.3f}, {1:0.3f}".format(x_pos_inch, y_pos_inch))

ad.disconnect()             # Close serial port to AxiDraw