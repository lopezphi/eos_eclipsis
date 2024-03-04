import glob
import os
import datetime

from PIL import Image
from PIL.ExifTags import TAGS

jpeg_folder = r"F:\Pictures\2023_04_17-22 - Australie\2023_04_20 - Total Solar Eclipse\Close-Up\JPEG_Partial1"
cr3_folder = r"F:\Pictures\2023_04_17-22 - Australie\2023_04_20 - Total Solar Eclipse\Close-Up\CR3"

def get_potential_existing_key(number, numbers_list, sensitivity):
    key = None
    if number in numbers_list:
        key = number
    else:
        for i in range(int(number) - int(sensitivity), int(number) + int(sensitivity)):
            if float(i) in numbers_list:
                key = float(i)
    return key


file_data_dict = {}
for input_file_path in sorted(glob.glob(jpeg_folder + os.sep + "*.JPG")):
    input_file_size = os.path.getsize(input_file_path)
    cr3_file_path = cr3_folder + os.sep + input_file_path.split(os.sep)[-1].replace('.JPG', '.CR3')
    image = Image.open(input_file_path)
    exifdata = image.getexif()
    timestamp = None
    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        if tag == "DateTime":
            formated_date = datetime.datetime.strptime(exifdata.get(tag_id),"%Y:%m:%d %H:%M:%S")
            timestamp = datetime.datetime.timestamp(formated_date)
    if timestamp is None:
        print(f"ERROR: No Date Time found for file: {input_file_path}")
        continue
    key = get_potential_existing_key(timestamp, list(file_data_dict.keys()), 2)
    if key is None:
        key = timestamp
        file_data_dict[key] = []
    file_data_dict[key].append([input_file_path, cr3_file_path, input_file_size])

for files_list in file_data_dict.values():
    max_file_size = max([file_info[2] for file_info in files_list])
    for file_info in files_list:
        if file_info[2] != max_file_size:
            if os.path.isfile(file_info[0]):
                print(f"Deleting file {file_info[0]}")
                os.remove(file_info[0])
            if os.path.isfile(file_info[1]):
                print(f"Deleting file {file_info[1]}")
                os.remove(file_info[1])