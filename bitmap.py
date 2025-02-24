# TODO: this file is incomplete and its function is already being fulfilled using PIL

"""
Functionality for creating and modifying bitmap files.

References:
    https://en.wikipedia.org/wiki/BMP_file_format
    https://lmcnulty.me/words/bmp-output/
    https://github.com/jtkirkpatrick/bitmap
"""

from utils import sanitize_input


class Bitmap(object):
    """Creates a bitmap object."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.row_pad = (self.width * 3) % 4

    def save(self, path):
        """Saves the bitmap object to a .bmp file specified by the path argument."""
        # TODO: complete this
        # input validation
        path = sanitize_input(path)
        if not path.endswith(".bmp"):
            path += ".bmp"

        path = f"testing/{path}"   # TODO: comment out this line
        # print(path)

        # calculate file size
        file_size = 14 + 40 + (3 * self.height * (self.width + self.row_pad))    # BMP header + DIB header + pixel array
        file_size_bytes = file_size.to_bytes(4, "little")
        # print(file_size_bytes)

        # convert height and width to bytes
        height_bytes = self.height.to_bytes(4, "little")
        width_bytes = self.width.to_bytes(4, "little")

        with open(path, 'wb') as file:
            file.write(bytearray([
                # BMP header
                0x42, 0x4d,                 # header field ("BM" in hex)
                file_size_bytes[0],         # size of bmp file in bytes
                file_size_bytes[1],
                file_size_bytes[2],
                file_size_bytes[3],
                0x00, 0x00, 0x00, 0x00,     # reserved
                0x36, 0x00, 0x00, 0x00,     # offset

                # DIB header
                0x28, 0x00, 0x00, 0x00,     # DIB header size (40)
                width_bytes[0],            # bit map width
                width_bytes[1],
                width_bytes[2],
                width_bytes[3],
                height_bytes[0],             # bit map height
                height_bytes[1],
                height_bytes[2],
                height_bytes[3],
                0x01, 0x00,                 # number of color planes (1)
                0x18, 0x00,                 # number of bits per pixel (24 for RGB)
                0x00, 0x00, 0x00, 0x00,     # compression (none)
                0x00, 0x00, 0x00, 0x00,     # x pixels per meter
                0x00, 0x00, 0x00, 0x00,     # y pixels per meter
                0x00, 0x00, 0x00, 0x00,     # number of colors
                0x00, 0x00, 0x00, 0x00,     # important colors

                # color table


                # pixel array

            ]))

            # Pixel array (all black pixels)
            for y in range(self.height):
                for x in range(self.width):
                    file.write(bytearray([0, 0, 0]))

            file.write(bytearray([0] * self.row_pad))

        print(f"Saved {path} as bmp file.")


if __name__ == '__main__':
    test = Bitmap(2, 1)
    test.save("bmp_test")
