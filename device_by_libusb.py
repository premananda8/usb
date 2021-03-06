import os
import platform
import sys

import usb.backend.libusb1


def get_usb_dll():
    os_type, os_bit, dll_file = None, None, None
    sysbit = platform.machine()
    ostype = platform.system()
    if ostype == "Windows":
        os_type = "_windows"
        dll_file = "libusb-1.0.dll"
        if sysbit == "AMD64":
            os_bit = "x64"
        elif sysbit == "AMD86" or sysbit == "AMD32":
            os_bit = "x86"
    elif ostype == "Darwin":
        os_type = "_osx"
        dll_file = ".keep"
        if sysbit == "x86_64":
            os_bit = "x64"
        elif sysbit == "x86":
            os_bit = "x86"
        elif sysbit == "x64":
            os_bit = "x64"
    elif ostype == "Linux":
        os_type = "_linux"
        dll_file = ".keep"
        if sysbit == "i686":
            os_bit = "x64"

    print("OS Type:" + str(platform.system()))

    return os_type, os_bit, dll_file


try:
    path = sys.executable
    path = path.replace("python.exe", "")  # installed directory
    path = path.replace("Scripts\\", "")  # for venv
    if os.path.exists(path):
        os_type, os_bit, dll_file = get_usb_dll()
        if os_type is not None and os_bit is not None and dll_file is not None:
            backend = usb.backend.libusb1.get_backend(find_library=lambda
                x: path + "Lib/site-packages/libusb/_platform/" + os_type + "/" + os_bit + "/" + dll_file)  # x: path + "Lib/site-packages/libusb/_platform/"+ "_windows/x64" + "/libusb-1.0.dll"

            dev = usb.core.find(idVendor=0x25AD, idProduct=0xffff, backend=backend)
            if dev is None:
                raise ValueError('Device not found')

            # set the active configuration. With no arguments, the first
            # configuration will be the active one
            #dev.set_configuration()

            # get an endpoint instance
            #cfg = dev.get_active_configuration()
            #intf = cfg[(1, 2)]

            # ep = usb.util.find_descriptor(
            #     intf,
            #     # match the first OUT endpoint
            #     custom_match= \
            #         lambda e: \
            #             usb.util.endpoint_direction(e.bEndpointAddress) == \
            #             usb.util.ENDPOINT_OUT)
            #
            # assert ep is not None
            #
            # print(list(dev))
            print(dev.serial_number)
except Exception as e:
    print(str(e))