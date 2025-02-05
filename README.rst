#######
pysub20
#######


pysub20 is a LGPL licensed, simple pure Python binding for sub20 library: a software that allows PCs to work with a SUB-20 device.
SUB-20 is a versatile and efficient bridge device providing simple interconnect between PC (USB host) and different HW devices and systems via popular interfaces such as I2C, SPI, MDIO, RS232, RS485, SMBus, ModBus, IR and others.
You could find more information about the SUB-20 device on the official site: http://www.xdimax.com/sub20/sub20.html

The main goal of the project is that: to make the use of the SUB-20 library more convenient and pythonic. It's possible to use SUB-20 dll/so directly but it's a bit inconvenient, because every time you have to wrap the C library functions with Python c_type signatures.

Requirements
------------
You MUST have a sub20 library installed in your system. To proceed with the installation take a look at the SUB-20 documentation:  http://www.xdimax.com/sub20/sub20.html.

Usage
-----

**Low-level API:**
The low-level API is the raw Python functions converted from the SUB-20 C library functions.
You can use them 'as is' with regard to the SUB-20 and Python c_types documentation.

```python
from sub20.ctypeslib.libsub import SIGNATURES, sub_version
from sub20.ctypeslib.utils import load_ctypes_library
libname = "sub20.dll" if sys.platform == "win32" else "libsub.so"
libsub = load_ctypes_library(libname, SIGNATURES)
sub_errno = c_int.in_dll(libsub, "sub_errno")
libsub.sub_open(None)
# ... your code with SUB-20 functions
libsub.close()
```

**High-level API:**
A high level API tries to hide routine operations under the hood and make the SUB-20 library more pythonic and simple. The core of the high-level API is SUBDevice class. You don't have to load libraries explicitly because it's happening during the class instantiation.

from sub20 import SUBDevice
subdev = sub20.SUBDevice()
subdev.open()

Then you can use the implemented functions in your code. To properly use them it’s strongly recommended to read the SUB-20 documentation first: http://www.xdimax.com/sub20/doc/sub20-man.pdf

NB: If you don't have a sub20 library in your system and you try to create a SUBDevice instance then you'll get an ImportError exception.

List of implemented functions:
------------------------------

sub_get_serial_number,
sub_get_product_id,
sub_get_version,
sub_get_version_dict,
sub_reset,
sub_eep_read,
sub_eep_write,
sub_i2c_freq,
sub_i2c_config,
sub_i2c_start,
sub_i2c_stop,
sub_i2c_scan,
sub_i2c_read,
sub_i2c_write,
sub_i2c_transfer,
sub_gpio_config,
sub_gpio_read,
sub_gpio_write,
sub_gpiob_config,
sub_gpiob_read,
sub_gpiob_write,
sub_rs_set_config,
sub_rs_get_config,
sub_rs_timing,
sub_rs_xfer,
sub_fifo_config,
sub_fifo_read,
strerror,
sub_mdio22,
sub_mdio45,
sub_mdio_xfer,
sub_mdio_xfer_ex,

Examples
-------------
Get the list of all sub20 devices in the system:

```python
from ctypes import create_string_buffer, c_int
from sub20.ctypeslib.libsub import SIGNATURES
from sub20.ctypeslib.utils import load_ctypes_library

def get_sub20_devs(_libsub):
    sub20devs = []
   _device = _libsub.sub_find_devices(None)
   while _device:
       _handler = _libsub.sub_open(_device)
       if _handler:
           sub20devs.append(_handler)
       _device = _libsub.sub_find_devices(_device)
   return sub20devs


BUFFER_SIZE = 64
MAX_BUF_SZ = 64
libsub = load_ctypes_library("sub20.dll", SIGNATURES)
sub_errno = c_int.in_dll(libsub, "sub_errno")
rx_buf_sz = MAX_BUF_SZ
rx_buf = create_string_buffer(rx_buf_sz)
devs = get_sub20_devs(libsub)
# ... Then you can do with handlers whatever you want: for example, get all serial numbers
for dev in devs:
   if libsub.sub_get_serial_number(dev, rx_buf, rx_buf_sz) < 0:
       print("Error")
       continue
   print(rx_buf.value.decode('UTF-8'))
```

MDIO operations

```python
# generate mdio write/read frame
# ... init sub20 lib
hndl = libsub.sub_open(None)
contains = c_int()
libsub.sub_mdio22(hndl, SUB_MDIO22_READ, 0x01, 0x12, 0, byref(contains) );
libsub.sub_mdio22(hndl, SUB_MDIO22_WRITE, 0x02, 0x05, 0x55AA, byref(contains))
```

```python
# Generate a sequence of independent MDIO frames
# ... init sub20
hndl = libsub.sub_open(None)
# Define the array type
frame_count = 2
sub_mdio_frame_array = sub_mdio_frame * frame_count
# Allocate the array and populate it
mdios_array = sub_mdio_frame_array()
# Populate with data
mdios_array[0].clause22.op = SUB_MDIO22_READ
mdios_array[0].clause22.phyad = 0x01
mdios_array[0].clause22.regad = 0x12
mdios_array[1].clause45.op = SUB_MDIO45_ADDR
mdios_array[1].clause45.prtad = 0x04
mdios_array[1].clause45.devad = 0x02
mdios_array[1].clause45.data = 0x55A7
rc = libsub.sub_mdio_xfer(hndl, frame_count, mdios_array)
print(rc)
```

**How to install**
run command 
``pip install .`` or if placed in a subfolder
``pip install submodulePath/.``