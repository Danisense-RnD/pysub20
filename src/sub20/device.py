# -*- coding: utf-8 -*-
# Copyright (C) 2022 Paul Grebeniuk <paul@coolautomation.com>

# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 2.1 of the License, or (at your
# option) any later version.

# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

"""
    sub20.Device
    =====================
    Device class implementation of :mod:`sub20`.
    .. moduleauthor::  Paul Grebeniuk  <paul@coolautomation.com>
"""

import sys
from ctypes import create_string_buffer, c_int

from sub20.ctypeslib.libsub20 import SIGNATURES
from sub20.ctypeslib.utils import load_ctypes_library
from sub20._errors import SubDeviceError, SubNotFoundError, SubNotOpenedError

# Enum

""" RS232/RS485"""
RS_RX_ENABLE = 0x80
RS_TX_ENABLE = 0x40

# Character Size
RS_CHAR_5 = 0x00
RS_CHAR_6 = 0x02
RS_CHAR_7 = 0x04
RS_CHAR_8 = 0x06
RS_CHAR_9 = 0x07

# Parity
RS_PARITY_NONE = 0x00
RS_PARITY_EVEN = 0x20
RS_PARITY_ODD = 0x30

# Stop Bits
RS_STOP_1 = 0x00
RS_STOP_2 = 0x08

# Timing Flags
RS_RX_BEFORE_TX = 0x01
RS_RX_AFTER_TX = 0x02

FIFO_SELECT_UART = 0x02


class SUBDevice(object):
    def __init__(self, buffer_size=64):
        libname = 'sub20.dll' if sys.platform == "win32" \
            else 'libsub.so'

        self._libsub, self.sub_errno = load_ctypes_library(libname, SIGNATURES)
        self._device = None
        self.buffer_size = buffer_size
        self.rx_buf = create_string_buffer(buffer_size)

    def open(self):
        self._device = self._libsub.sub_open(None)
        if not self._device:
            raise SubNotFoundError()

    def sub_i2c_scan(self):
        if not self._device:
            raise SubNotOpenedError()
        addresses = []

        counter = c_int(1)
        rc = self._libsub.sub_i2c_scan(self._device, counter, self.rx_buf)
        if not rc:
            for ii in range(0, counter.value):
                addresses.append(ord(self.rx_buf[ii]))
        return addresses

    def sub_i2c_read(self, sa, ma, sa_sz, ma_sz):
        if not self._device:
            raise SubNotOpenedError()
        _rc = self._libsub.sub_i2c_read(self._device, sa, ma, sa_sz, self.rx_buf, ma_sz)
        if _rc:
            raise SubDeviceError(f"Error {self.sub_errno}")
        return self.rx_buf

    def sub_i2c_write(self, sa, ma, sa_sz, data_buf, ma_sz):
        if not self._device:
            raise SubNotOpenedError()
        _rc = self._libsub.sub_i2c_read(self._device, sa, ma, sa_sz, data_buf, ma_sz)
        if _rc:
            raise SubDeviceError(f"Error {self.sub_errno}")

    def sub_gpiob_config(self, set_par, mask):
        if not self._device:
            raise SubNotOpenedError()
        get_par = c_int(1)
        _rc = self._libsub.sub_gpiob_config(self._device, set_par, get_par, mask)
        if _rc:
            raise SubDeviceError(f"Error {self.sub_errno}")
        return get_par.value

    def sub_gpiob_read(self):
        if not self._device:
            raise SubNotOpenedError()
        get_par = c_int(1)
        _rc = self._libsub.sub_gpiob_read(self._device, get_par)
        if _rc:
            raise SubDeviceError(f"Error {self.sub_errno}")
        return get_par.value

    def sub_gpiob_write(self, set_par, mask):
        if not self._device:
            raise SubNotOpenedError()
        get_par = c_int(1)
        _rc = self._libsub.sub_gpiob_write(self._device, set_par, get_par, mask)
        if _rc:
            raise SubDeviceError(f"Error {self.sub_errno}")
        return get_par.value

    def sub_rs_set_config(self, config, baud):
        if not self._device:
            raise SubNotOpenedError()
        _rc = self._libsub.sub_rs_set_config(self._device, config, baud)
        if _rc:
            raise SubDeviceError(f"Error {self.sub_errno}")

    def sub_rs_get_config(self):
        if not self._device:
            raise SubNotOpenedError()
        config = c_int(8)
        baud = c_int(8)
        _rc = self._libsub.sub_rs_get_config(self._device, config, baud)
        if _rc:
            raise SubDeviceError(f"Error {self.sub_errno}")
        return config.value, baud.value

    def sub_rs_timing(self, flags, tx_space_us, rx_msg_us, rx_byte_us):
        if not self._device:
            raise SubNotOpenedError()
        _rc = self._libsub.sub_rs_timing(self._device, flags, tx_space_us, rx_msg_us, rx_byte_us)
        if _rc:
            raise SubDeviceError(f"Error {self.sub_errno}")

    def sub_rs_xfer(self, tx_buf, tx_sz):
        if not self._device:
            raise SubNotOpenedError()
        _rc = self._libsub.sub_rs_xfer(self._device, tx_buf, tx_sz, self.rx_buf, self.buffer_size)
        if _rc == -1:
            raise SubDeviceError(f"Error {self.sub_errno}")
        return _rc

    def sub_fifo_config(self, config):
        if not self._device:
            raise SubNotOpenedError()
        _rc = self._libsub.sub_fifo_config(self._device, config)
        if _rc:
            strerr = self._libsub.strerror(self.sub_errno)
            raise SubDeviceError(f"Error {self.sub_errno}: {strerr}")

    def sub_fifo_read(self, to_ms):
        if not self._device:
            raise SubNotOpenedError()
        _rc = self._libsub.sub_fifo_read(self._device, self.rx_buf, self.buffer_size, to_ms)
        if _rc < 0:
            strerr = self._libsub.strerror(self.sub_errno)
            raise SubDeviceError(f"Error {self.sub_errno}: {strerr}")
        return _rc

    def close(self):
        if self._device:
            self._libsub.sub_close(self._device)
