from ctypes import POINTER, Structure, c_char_p, c_int


class sub_device(Structure):  # pylint: disable=invalid-name
    """
    Dummy for ``sub_device`` structure.
    """
    # pylint: disable=too-few-public-methods
    pass


sub_device_p = POINTER(sub_device)  # pylint: disable=invalid-name


class sub_handle(Structure):  # pylint: disable=invalid-name
    """
    Dummy for ``sub_handle`` structure.
    """
    # pylint: disable=too-few-public-methods
    pass


sub_handle_p = POINTER(sub_handle)  # pylint: disable=invalid-name
c_int_p = POINTER(c_int)

SIGNATURES = dict(
    sub_find_devices=([sub_device_p], sub_device_p),
    sub_open=([sub_device_p], sub_handle_p),
    sub_i2c_scan=([sub_handle_p, c_int_p, c_char_p], c_int),
    sub_i2c_read=([sub_handle_p, c_int, c_int, c_int, c_char_p, c_int], c_int),
    sub_i2c_write=([sub_handle_p, c_int, c_int, c_int, c_char_p, c_int], c_int),
    sub_gpiob_config=([sub_handle_p, c_int, c_int_p, c_int], c_int),
    sub_gpiob_write=([sub_handle_p, c_int, c_int_p, c_int], c_int),
    sub_gpiob_read=([sub_handle_p, c_int_p], c_int),
    sub_rs_set_config=([sub_handle_p, c_int, c_int], c_int),
    sub_rs_get_config=([sub_handle_p, c_int_p, c_int_p], c_int),
    sub_rs_timing=([sub_handle_p, c_int, c_int, c_int, c_int], c_int),
    sub_rs_xfer=([sub_handle_p, c_char_p, c_int, c_char_p, c_int], c_int),
    sub_close=([sub_handle_p], None),
    sub_fifo_config=([sub_handle_p, c_int], c_int),
    sub_fifo_read=([sub_handle_p, c_char_p, c_int, c_int], c_int),
    sub_strerror=([c_int], c_char_p)

)
