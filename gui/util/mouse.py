import os

try:
    if os.name == 'nt':
        from ctypes import windll
        # check if the buttons are inverted: 0x01 = left ----- 0x02 = right mouse button
        btn_code = 0x01 if windll.user32.GetSystemMetrics(23) == 0 else 0x02
        def mouse_pressed():
            '''
                Check if the left button is pressed
            '''
            return windll.user32.GetKeyState(btn_code) not in [0, 1]
            #                       ^ this returns either 0 or 1 when button is not being held down
    else:
        import mouse
        def mouse_pressed():
            return mouse.is_pressed()
except: # it's not important if the module wasn't loaded, drag and drop events won't be set
    mouse_pressed = None