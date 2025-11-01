_ADDON_NAME_ = 'WEBP Loop'

from ...extract import FileDescriptor

def main( file: FileDescriptor ):

    data = file.bytes
    anmf = data.find( b'\x41\x4E\x4D\x46' ) # ANMF

    if anmf > -1:
        data[anmf - 2] = 0