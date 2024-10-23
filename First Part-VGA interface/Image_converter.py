from PIL import Image

def combine_rgb_to_12bit(r, g, b):
    return ((r & 0xF0) << 4) | ((g & 0xF0) >> 0) | ((b & 0xF0) >> 4)

image = Image.open('Lena_75_100.png')
image = image.convert('RGB')
pixel = image.load()
out_file = open('../Lena_mod_hex.txt', 'w')

# Scrittura file per riempire la memoria su quartus
out_file.write('DEPTH = 32768;\n'
               ' WIDTH = 12;\n'
               ' ADDRES_RADIX=HEX;\n'
               ' DATA_RADIX = HEX;\n'
               ' CONTENT BEGIN\n')

address = 0
for y in range(256):
    for x in range(128):
        try:
            r, g, b = pixel[x, y][:3]
            r_4bit = r & 0xF0
            g_4bit = g & 0xF0
            b_4bit = b & 0xF0
            combined_value = combine_rgb_to_12bit(r, g, b)

            out_file.write(f'{address:01X} : {combined_value:03X};\n')
            address += 1
        except IndexError:
            out_file.write(f'{address:01X} : 000;\n')
            address += 1


out_file.write('END;\n')

out_file.close()

# Scrittura file per riempire la memoria su digital
out_file_bin = open('../Lena_mod_hex.bin', 'wb')

for y in range(256):
    for x in range(128):
        try:
            r, g, b = pixel[x, y][:3]
            r_4bit = r & 0xF0
            g_4bit = g & 0xF0
            b_4bit = b & 0xF0
            combined_value = combine_rgb_to_12bit(r, g, b)
            print(combined_value)
            out_file_bin.write(combined_value.to_bytes(2, byteorder='big'))
        except IndexError:
            out_file_bin.write((0).to_bytes(2, byteorder='big'))

out_file_bin.close()