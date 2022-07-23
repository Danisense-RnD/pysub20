######
pysub20
######


pysub20 is a LGPL_ licensed, simple pure Python_ binding for sub20_ library: a software that allows PC works with a SUB-20 device.
SUB-20 is a versatile and efficient bridge device providing simple interconnect between PC (USB host) and different HW
devices and systems via popular interfaces such as I2C, SPI, MDIO, RS232, RS485, SMBus, ModBus, IR and others.
You could find more information about the SUB-20 device on the official site: http://www.xdimax.com/sub20/sub20.html

Requirements
------------
You MUST have a sub20 library installed in your system. To proceed with the installation take a look at the SUB-20 documentaion:  http://www.xdimax.com/sub20/sub20.html. 

Usage
-----
Initialization:

>>> import sub20
>>> subdev = sub20.SUBDevice()
>>> subdev.open()

Then you can use the wrapped sub20 functions in your code. To understand how to use them properly I strongly recommend to read the sub20 documentation first: http://www.xdimax.com/sub20/doc/sub20-man.pdf
