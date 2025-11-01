_ADDON_NAME_ = 'SCT to PNG'

from ...util.misc  import FileDescriptor
from ...constants  import TEMP_FOLDER

import os
import io
import PIL.Image
import lz4.block
from texture2ddecoder import decode_astc, decode_etc2a8

# --------- UI updater
import sys
from ...settings   import _setter, config
from ...constants  import IMG_FORMATS
SCT_AS_IMGAE_FORMAT = config.getint('PLUGIN', 'SctAsImageFormat', fallback=0)
widget = None

def addSctFormat(v: bool):
    if v:
        if not 'sct' in IMG_FORMATS:
            IMG_FORMATS.append('sct')
    else:
        if 'sct' in IMG_FORMATS:
            IMG_FORMATS.remove('sct')

addSctFormat(SCT_AS_IMGAE_FORMAT)

def changed(val):
    global SCT_AS_IMGAE_FORMAT
    SCT_AS_IMGAE_FORMAT = val != 0
    addSctFormat(SCT_AS_IMGAE_FORMAT)
    _setter('PLUGIN', 'SctAsImageFormat', 1 if SCT_AS_IMGAE_FORMAT else 0)

if 'PyQt6' in sys.modules:
    from PyQt6.QtWidgets import QApplication, QWidget
    app = QApplication.instance()
    add_setting = app.property('CreateSetting')

    if add_setting:
        widget: QWidget = add_setting(title=f'[<b>{_ADDON_NAME_}</b>] SCT as image format', description='', value=SCT_AS_IMGAE_FORMAT, type='checkbox', options=[], onchanged=changed)

def destroy():
    global widget
    if widget:
        widget.parentWidget().layout().removeWidget(widget)
        widget.deleteLater()
        widget = None
        addSctFormat(False)





# ------- Main
def main(file: FileDescriptor):

    dest_path = file.path
    data_bytes = file.bytes
    info = file.tree_file

    fm = data_bytes
    
    fm.seek(0)

    sct_sign = fm.read(3)

    is_sct2 = fm.read(1) == b'\x32'

    if is_sct2 is not True: # Old format

        byte_format = fm.read_uint8()

        width = fm.read_uint16()

        height = fm.read_uint16()

        uncompressed_size = fm.read_uint32()

        compressed_size = fm.read_uint32()

        byte_data = fm.read( compressed_size )

        data = lz4.block.decompress( byte_data, uncompressed_size = uncompressed_size )

    else:
        dataLen = fm.read_uint32()
        _ = fm.read_uint32()
        offset = fm.read_uint32()
        block_width = block_height = fm.read_uint32()
        byte_format = fm.read_uint32() # 40 for normal images, 19 for some smaller ones
        width = fm.read_uint16()
        height = fm.read_uint16()
        width2 = fm.read_uint16()
        height2 = fm.read_uint16()
        fm.seek(offset)
        uncompressed_size = fm.read_uint32()
        compressed_size = fm.read_uint32()

        if compressed_size == dataLen - 80:
            byte_data = fm.read( compressed_size )
            data = lz4.block.decompress( byte_data, uncompressed_size = uncompressed_size )
        else:
            fm.seek(offset)
            byte_data = fm.read( compressed_size )
            data = byte_data

    if is_sct2:
        match byte_format:
            case 19:
                image_data = decode_etc2a8(data, width, height)
            case 40:
                image_data = decode_astc(data, width, height, 4, 4)
            case 47:
                image_data = decode_astc(data, width, height, 8, 8)
            case _:
                raise Exception(f'Unknown SCT2 byte format for file {file.tree_file["full_path"]} byte format f{byte_format}')
    else:
        match byte_format:
            case 2:
                image = pil_image_RGBA32( data, width, height )

            case 4:
                image = pil_image_RGB16_A( data, width, height )

            case _: # czn -> lucas_attack_play2_bg_s.sct [format 102]
                raise Exception(f'Unknown SCT byte format for file {file.tree_file["full_path"]} byte format {byte_format}')

    image = PIL.Image.frombytes('RGBA', (width, height), image_data, 'raw', 'BGRA')

    if dest_path is None:
        file.bytes.clear()
        file.bytes += image_to_byte_array( image )
    else:
        # check if it's a drag and drop operation
        # if it is moving file to the temp folder then don't change the file name!
        if os.path.dirname(dest_path) == TEMP_FOLDER :
            file_name = dest_path
        else:
            file_name = dest_path.replace(".sct", ".png")

        file.path = None #dest_path.replace(".sct", ".png")
        image.save( file_name, 'PNG' )

def pil_image_RGB16_A(data, width, height):
    img   = PIL.Image.frombytes('RGB', (width, height), data, 'raw', 'BGR;16', 0, 1)
    alpha = PIL.Image.new('L', img.size, 255)
    alpha.putdata(data[-width*height:])
    img.putalpha(alpha)
    return img

def pil_image_RGBA32(data, width, height):
    return PIL.Image.frombytes('RGBA', (width, height), data, 'raw', 'RGBA')


def image_to_byte_array(image: PIL.Image, format='PNG') -> bytes:
  # BytesIO is a file-like buffer stored in memory
  imgByteArr = io.BytesIO()
  # image.save expects a file-like as a argument
  image.save(imgByteArr, format=format)
  # Turn the BytesIO object back into a bytes object
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr