import timeit
import tifffile as tiff
import numpy as np
import glob, os
import json
import tifftools
import copy

input_folder = r"F:\Pictures\2023_04_17-22 - Australie\2023_04_20 - Total Solar Eclipse\Close-Up\TIFF16_Totality"
# input_folder = r"F:\Pictures\2023_04_20\Close-Up\TIFF16b"
output_folder = r"F:\Pictures\2023_04_17-22 - Australie\2023_04_20 - Total Solar Eclipse\Close-Up\TIFF16_Totality_Centered"

if not os.path.isdir(output_folder):
    os.mkdir(output_folder)

first = '2023_04_20_IMG_0859.TIF'
last = '2023_04_20_IMG_0860.TIF'
# first = '2023_04_20_IMG_1105.TIF'
# last = '2023_04_20_IMG_1118.TIF'
process = False
file_nb = 0
max_moon_diameter = 2495
moon_location_boundaries = {'x': [1800, 5100], 'y': [1700, 4400]}
moon_location_boundaries = {'x': [2700, 5400], 'y': [1800, 4400]}
# increase when sum_avg decrease (from 5000 to 15000)
varation_data = [-12000, 12000]
# info_hack = tifftools.read_tiff('2023_04_20_IMG_0887bb.TIF')
for input_file_path in glob.glob(input_folder + os.sep + "*.TIF"):
    if input_file_path.endswith(first):
        process = True
    elif input_file_path.endswith(last):
        process = False
    if process:
        file_name = input_file_path.split(os.sep)[-1]
        # input_file_path = '2023_04_20_IMG_0887bb.TIF'
        # file_name = input_file_path.split(os.sep)[-1]
        file_nb += 1
        print(f"\n{file_nb}. Reading Image file: {input_file_path}")
        t0 = timeit.default_timer()
        image_array = tiff.imread(input_file_path)
        t1 = timeit.default_timer()
        print(f"\tImage Reading Runtime: {round(t1-t0, 3)} second(s)...")
        print(f"\tImage Size: {image_array.shape[1]}x{image_array.shape[0]}. Type: {image_array.dtype}.")
        if image_array.dtype == 'uint16':
            sum_max = 256 * 256 * 3
        elif image_array.dtype == 'uint8':
            sum_max = 256 * 3
        image_pixels_nb = image_array.shape[1] * image_array.shape[0]
        info_org = tifftools.read_tiff(input_file_path)
        
        # temp_output_file_path = output_folder + os.sep + file_name.replace('.', '_temp.')
        # info_dst = tifftools.read_tiff(temp_output_file_path)
        # for k, v in info_org['ifds'][0]['tags'].items():
        #     if k not in info_dst['ifds'][0]['tags'] or k == 305:
        #         # if k != 700 and k != 34853 and k != 34675:
        #         if k == 271 or k == 272 or k == 34665:
        #             info_dst['ifds'][0]['tags'][k] = v
        #             print(k, v)
        #             # exit()
        # output_file_path = output_folder + os.sep + file_name
        # if os.path.isfile(output_file_path):
        #     os.remove(output_file_path)
        # tifftools.write_tiff(info_dst, output_file_path)
        # exit()

        t0 = timeit.default_timer()
        variation_dict = {'x': [], 'y': []}
        debug_dict = {'x': [], 'y': []}
        previous_progression = -1
        print("\tAnalyzing... Please be patient...")
        sum_list = []
        image_size = int(image_array.shape[1]) * int(image_array.shape[0])
        sum_avg = 0
        nb_saturated_pixels = 0
        for row_idx in range(image_array.shape[0]):
            progression = int(100*row_idx/(image_array.shape[0] - 1))
            if progression != previous_progression:
                print(f"\t\tParsing Progression: {int(progression)}%", end="\r", flush=True)
            previous_progression = progression
            row_sum = []
            for col_idx in range(image_array.shape[1]):
                current_sum = sum(image_array[row_idx][col_idx])
                if current_sum > sum_max * 0.999:
                    nb_saturated_pixels += 1
                row_sum.append(current_sum)
                sum_avg += current_sum / image_size
            sum_list.append(row_sum)
        percentage_saturated_pixels = round(100 * nb_saturated_pixels / image_pixels_nb, 2)
        print(f"\n\t\tPixel Average Value: {sum_avg}")
        print(f"\t\tSaturated Pixels Percentage: {percentage_saturated_pixels}%")
        # sum_avg *= 5
        sum_tol = sum_avg * 2.25 + 50000
        for row_idx in range(image_array.shape[0]):
            progression = int(100*row_idx/(image_array.shape[0] - 1))
            if progression != previous_progression:
                print(f"\t\tRow Processing Progression: {int(progression)}%", end="\r", flush=True)
            previous_progression = progression
            varation_data = [-12000, 12000]
            location_data = [[0, 0], [0, 0]]
            debug_data = [[], []]
            sum_t0 = sum_list[row_idx][0]
            sum_t1 = sum_list[row_idx][1]
            sum_t2 = sum_list[row_idx][2]
            corona_saturation = False
            for col_idx in range(3, image_array.shape[1], 1):
                sum_t3 = sum_list[row_idx][col_idx]
                delta_t0 = sum_t1 - sum_t0
                delta_t1 = sum_t2 - sum_t1
                delta_t2 = sum_t3 - sum_t2
                if varation_data[0] > delta_t0 and delta_t0 < delta_t1 and delta_t0 < delta_t2 and sum_t2 < sum_tol and sum_t3 < sum_tol and (delta_t1 < -500 or delta_t2 < -500) and (sum_t0 > sum_max * 0.925 or percentage_saturated_pixels < 3):
                    debug_data[0] = [delta_t0, delta_t1, delta_t2, sum_t0, sum_t1, sum_t2, sum_t3, sum_tol, varation_data]
                    varation_data[0] = delta_t0
                    location_data[0] = [row_idx, col_idx - 2]
                if varation_data[1] < delta_t2 and delta_t0 < delta_t2 and delta_t1 < delta_t2 and sum_t0 < sum_tol and sum_t1 < sum_tol and (delta_t0 > 500 or delta_t1 > 500) and (sum_t3 > sum_max * 0.925 or percentage_saturated_pixels < 3):
                    debug_data[1] = [delta_t0, delta_t1, delta_t2, sum_t0, sum_t1, sum_t2, sum_t3, sum_tol, varation_data]
                    varation_data[1] = delta_t2
                    location_data[1] = [row_idx, col_idx - 1]
                if sum_t0 > sum_max * 0.999 and sum_t1 > sum_max * 0.999 and sum_t2 > sum_max * 0.999 and sum_t3 > sum_max * 0.999 and not corona_saturation and percentage_saturated_pixels > 0.7:
                    if location_data[0] != [0, 0]:
                        location_data[0] = [0, 0]
                        varation_data[0] = 0
                        # print("DEBUG2", col_idx, "", sum_t0, sum_t1, sum_t2, sum_t3, "", delta_t0, delta_t1, delta_t2, "", varation_data, location_data)
                    corona_saturation = True
                if sum_t0 < sum_avg * 0.099 and sum_t1 < sum_avg * 0.099 and sum_t2 < sum_avg * 0.099 and sum_t3 < sum_avg * 0.099 and not corona_saturation and percentage_saturated_pixels > 0.7:
                    if location_data[1] != [0, 0]:
                        location_data[1] = [0, 0]
                        varation_data[1] = 0
                # if row_idx == 3105 or row_idx == 3105:
                #     if 1805 < col_idx < 1820 or 4290 < col_idx < 4305:
                #         print("DEBUG", row_idx, col_idx, "", sum_tol, sum_t0, sum_t1, sum_t2, sum_t3, "", delta_t0, delta_t1, delta_t2, "", varation_data, location_data)
                sum_t0 = sum_t1
                sum_t1 = sum_t2
                sum_t2 = sum_t3
            if not corona_saturation and percentage_saturated_pixels > 0.7:
                location_data = [[0, 0], [0, 0]]
            variation_dict['y'].append(location_data)
            debug_dict['y'].append(debug_data)
        # print(variation_dict['y'][610])

        previous_progression = -1
        print("")
        for col_idx in range(image_array.shape[1]):
            progression = int(100*col_idx/(image_array.shape[1] - 1))
            if progression != previous_progression:
                print(f"\t\tCol Processing Progression: {int(progression)}%", end="\r", flush=True)
            previous_progression = progression
            varation_data = [-12000, 12000]
            location_data = [[0, 0], [0, 0]]
            sum_t0 = sum_list[row_idx][0]
            sum_t1 = sum_list[row_idx][1]
            sum_t2 = sum_list[row_idx][2]
            corona_saturation = False
            for row_idx in range(3, image_array.shape[0], 1):
                sum_t3 = sum_list[row_idx][col_idx]
                delta_t0 = sum_t1 - sum_t0
                delta_t1 = sum_t2 - sum_t1
                delta_t2 = sum_t3 - sum_t2
                if varation_data[0] > delta_t0 and delta_t0 < delta_t1 and delta_t0 < delta_t2 and sum_t2 < sum_tol and sum_t3 < sum_tol and (delta_t1 < -500 or delta_t2 < -500) and (sum_t0 > sum_max * 0.925 or percentage_saturated_pixels < 3):
                    debug_data[0] = [delta_t0, delta_t1, delta_t2, sum_t0, sum_t1, sum_t2, sum_t3, sum_tol, copy.deepcopy(varation_data[0]), varation_data]
                    varation_data[0] = delta_t0
                    location_data[0] = [row_idx - 2, col_idx]
                if varation_data[1] < delta_t2 and delta_t0 < delta_t2 and delta_t1 < delta_t2 and sum_t0 < sum_tol and sum_t1 < sum_tol and (delta_t0 > 500 or delta_t1 > 500) and (sum_t3 > sum_max * 0.925 or percentage_saturated_pixels < 3):
                    debug_data[1] = [delta_t0, delta_t1, delta_t2, sum_t0, sum_t1, sum_t2, sum_t3, sum_tol, copy.deepcopy(varation_data[1]), varation_data]
                    varation_data[1] = delta_t2
                    location_data[1] = [row_idx - 1, col_idx]
                if sum_t0 > sum_max * 0.999 and sum_t1 > sum_max * 0.999 and sum_t2 > sum_max * 0.999 and sum_t3 > sum_max * 0.999 and not corona_saturation and percentage_saturated_pixels > 0.7:
                    if location_data[0] != [0, 0]:
                        location_data[0] = [0, 0]
                        varation_data[0] = 0
                    corona_saturation = True
                if sum_t0 < sum_avg * 0.099 and sum_t1 < sum_avg * 0.099 and sum_t2 < sum_avg * 0.099 and sum_t3 < sum_avg * 0.099 and not corona_saturation and percentage_saturated_pixels > 0.7:
                    if location_data[1] != [0, 0]:
                        location_data[1] = [0, 0]
                        varation_data[1] = 0
                if col_idx == 4700 or col_idx == 4700 :
                    if 1925 < row_idx < 1935 or 4415 < row_idx < 4425:
                        print("DEBUG", row_idx, col_idx, "", sum_tol, sum_t0, sum_t1, sum_t2, sum_t3, "", delta_t0, delta_t1, delta_t2, "", varation_data, location_data)
                sum_t0 = sum_t1
                sum_t1 = sum_t2
                sum_t2 = sum_t3
            if not corona_saturation and percentage_saturated_pixels > 0.7:
                location_data = [[0, 0], [0, 0]]
            variation_dict['x'].append(location_data)
            debug_dict['x'].append(debug_data)
        # print(variation_dict['x'][759])
        # print(variation_dict['x'][756])
        # print(variation_dict['x'][747])

        t1 = timeit.default_timer()
        print(f"\n\tImage Analyzing Runtime: {round(t1-t0, 3)} second(s)...")

        max_diameter = {'x': 0, 'y': 0}
        moon_center = {'x': 0, 'y': 0}
        variation_debug = {'x': [], 'y': []}
        for axis, variation_list_list in variation_dict.items():
            for idx, variation_list in enumerate(variation_list_list):
                if axis == 'x' and variation_list[0][0] != 0 and  variation_list[1][0] < moon_location_boundaries['y'][1] and  variation_list[0][0] > moon_location_boundaries['y'][0]:
                    current_diameter = variation_list[1][0] - variation_list[0][0]
                    current_center = variation_list[0][0] + current_diameter / 2
                elif axis == 'y' and variation_list[0][1] != 0 and  variation_list[1][1] < moon_location_boundaries['x'][1] and  variation_list[0][1] > moon_location_boundaries['x'][0]:
                    current_diameter = variation_list[1][1] - variation_list[0][1]
                    current_center = variation_list[0][1] + current_diameter / 2
                else:
                    current_diameter = 0
                # print(axis, variation_list, current_diameter, current_center)

                if max_moon_diameter > current_diameter > max_diameter[axis]:
                    max_diameter[axis] = current_diameter
                    moon_center[axis] = current_center
                    variation_debug[axis] = [variation_list, debug_dict[axis][idx]]
                #     previous_center = current_center
                #     print("DEBUG", axis, moon_center, current_diameter, current_center, variation_list, idx)
                # elif current_diameter == max_diameter[axis] != 0:
                #     moon_center[axis] += (current_center - previous_center) / 2
                #     print("DEBUG2", axis, moon_center, current_diameter, current_center, previous_center, variation_list)
                #     previous_center = current_center
                    # else:
                    #     print("DEBUG3", axis, moon_center, current_diameter, current_center, previous_center, variation_list)
                    #     print(f"ERROR: Uncontinuous identical max diameter for moon detection: {previous_center}, {current_center}")
            # if axis == 'x':
            #     for idx in range(740, 780, 1):
            #         print(variation_list_list[idx])

        # print(f"Picture center: {image_array.shape[1]/2} x {image_array.shape[0]/2}")
        print(f"\tMoon Diameter: {max_diameter}")
        print(f"\tMoon center: {moon_center['y']} x {moon_center['x']}")
        x_shift = round(image_array.shape[1] / 2 - moon_center['y'], 0)
        y_shift = round(image_array.shape[0] / 2 - moon_center['x'], 0)
        print(f"\tImage X-Shift: {x_shift}. Image Y-Shift: {y_shift}")
        if abs(max_diameter['y'] - max_diameter['x']) > 40 or max_diameter['x'] == 0 or max_diameter['y'] == 0:
            print("\tERROR: Moon Diameter is not looking good!!")
            print(f"\tDEBUG variation_list: {variation_debug}")
            exit()
        elif abs(max_diameter['y'] - max_diameter['x']) > 5 or max_diameter['x'] == 0 or max_diameter['y'] == 0:
            print("\tWARNING: Moon Diameter is not looking good!!")
            print(f"\tWARNING variation_list: {variation_debug}")

        print("\tBuilding New Image...")
        t0 = timeit.default_timer()
        new_image_array = []
        if x_shift > 0:
            if y_shift > 0:
                for row_idx in range(image_array.shape[0]):
                    progression = int(100*row_idx/(image_array.shape[0] - 1))
                    if progression != previous_progression:
                        print(f"\t\tBuilding Progression: {int(progression)}%", end="\r", flush=True)
                    previous_progression = progression
                    new_row = []
                    for col_idx in range(image_array.shape[1]):
                        if row_idx <= y_shift or col_idx <= x_shift:
                            new_row.append([0,0,0])
                        else:
                            new_row.append(image_array[int(row_idx - y_shift)][int(col_idx - x_shift)])
                    new_image_array.append(new_row)
            else:
                for row_idx in range(image_array.shape[0]):
                    progression = int(100*row_idx/(image_array.shape[0] - 1))
                    if progression != previous_progression:
                        print(f"\t\tBuilding Progression: {int(progression)}%", end="\r", flush=True)
                    previous_progression = progression
                    new_row = []
                    for col_idx in range(image_array.shape[1]):
                        if row_idx - y_shift >= image_array.shape[0] or col_idx <= x_shift:
                            new_row.append([0,0,0])
                        else:
                            new_row.append(image_array[int(row_idx - y_shift)][int(col_idx - x_shift)])
                    new_image_array.append(new_row)
        else:
            if y_shift > 0:
                for row_idx in range(image_array.shape[0]):
                    progression = int(100*row_idx/(image_array.shape[0] - 1))
                    if progression != previous_progression:
                        print(f"\t\tBuilding Progression: {int(progression)}%", end="\r", flush=True)
                    previous_progression = progression
                    new_row = []
                    for col_idx in range(image_array.shape[1]):
                        if row_idx <= y_shift or col_idx - x_shift >= image_array.shape[1]:
                            new_row.append([0,0,0])
                        else:
                            new_row.append(image_array[int(row_idx - y_shift)][int(col_idx - x_shift)])
                    new_image_array.append(new_row)
            else:
                for row_idx in range(image_array.shape[0]):
                    progression = int(100*row_idx/(image_array.shape[0] - 1))
                    if progression != previous_progression:
                        print(f"\t\tBuilding Progression: {int(progression)}%", end="\r", flush=True)
                    previous_progression = progression
                    new_row = []
                    for col_idx in range(image_array.shape[1]):
                        if row_idx - y_shift >= image_array.shape[0] or col_idx - x_shift >= image_array.shape[1]:
                            new_row.append([0,0,0])
                        else:
                            new_row.append(image_array[int(row_idx - y_shift)][int(col_idx - x_shift)])
                    new_image_array.append(new_row)

        t1 = timeit.default_timer()
        print(f"\n\tNew Image Building Runtime: {round(t1-t0, 3)} second(s)...")

        output_file_path = output_folder + os.sep + file_name
        temp_output_file_path = output_folder + os.sep + file_name.replace('.', '_temp.')
        print(f"\tWriting Image file: {output_file_path}")
        t0 = timeit.default_timer()
        tiff.imwrite(temp_output_file_path, np.array(new_image_array, dtype=np.uint16))
        info_dst = tifftools.read_tiff(temp_output_file_path)
        for k, v in info_org['ifds'][0]['tags'].items():
            if k not in info_dst['ifds'][0]['tags'] or k == 305:
                # if k != 700:
                info_dst['ifds'][0]['tags'][k] = v
                # else:
                #     info_dst['ifds'][0]['tags'][k] = info_hack['ifds'][0]['tags'][k]
        if os.path.isfile(output_file_path):
            os.remove(output_file_path)
        tifftools.write_tiff(info_dst, output_file_path)
        try:
            os.remove(temp_output_file_path)
        except:
            time.sleep(1)
            os.remove(temp_output_file_path)
        t1 = timeit.default_timer()
        print(f"\tImage Writing Runtime: {round(t1-t0, 3)} second(s)...")
