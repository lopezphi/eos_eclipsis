import timeit
import tifffile as tiff
import numpy as np
import glob, os
import time
import tifftools
import copy

input_folder = r"F:\Pictures\2023_04_17-22 - Australie\2023_04_20 - Total Solar Eclipse\Close-Up\CR3\TIFF16_Partial1"
first = '2023_04_20_IMG_0017.TIF'
last = '2023_04_20_IMG_0000.TIF'
reverse = False
min_location_is_ok = False


input_folder = r"F:\Pictures\2023_04_17-22 - Australie\2023_04_20 - Total Solar Eclipse\Close-Up\CR3\TIFF16_Partial2"
first = '2023_04_20_IMG_1807.TIF'
last = '2023_04_20_IMG_0000.TIF'
reverse = False
min_location_is_ok = True

output_folder = input_folder + "_Centered"
if not os.path.isdir(output_folder):
    os.mkdir(output_folder)

# avg_sun_diameter_tolerance_pct = 0.75
pixel_avging_nb = 11

file_nb = 0
avg_sun_diameter_list_dict = {'x': [], 'y': []}
avg_sun_diameter_dict = {}
# sun_location_boundaries = {'x': [0, 8257], 'y': [0, 5508]}
pixel_point = int(pixel_avging_nb / 2)
# increase when sum_avg decrease (from 5000 to 15000)
# info_hack = tifftools.read_tiff('2023_04_20_IMG_0887bb.TIF')

def is_valid_increase(delta_t, pixel_avging_nb, pixel_pt, current_max):
    if delta_t[pixel_pt] < current_max / 30 or delta_t[pixel_pt] > current_max / 2:
        return False
    sum_delta = 0
    for i in range(pixel_avging_nb):
        if delta_t[pixel_pt] < delta_t[i] and i != pixel_pt:
            return False
        sum_delta += delta_t[i] 
    if delta_t[pixel_pt] > sum_delta:
        return False
    return True

def is_valid_decrease(delta_t, pixel_avging_nb, pixel_pt, current_max):
    if delta_t[pixel_pt] > -current_max / 30 or delta_t[pixel_pt] < -current_max / 2:
        return False
    sum_delta = 0
    for i in range(pixel_avging_nb):
        if delta_t[pixel_pt] > delta_t[i] and i != pixel_pt:
            return False
        sum_delta += delta_t[i]
    if delta_t[pixel_pt] < sum_delta:
        return False
    return True

def get_delta(sum_list, row_start, row_end, col_start, col_end):
    delta_t = []
    for col in range(col_start, col_end):
        my_sum = [0, 0]
        for row in range(row_start, row_end):
            my_sum[0] += sum_list[row][col]
            my_sum[1] += sum_list[row][col+1]
        delta_t.append((my_sum[1] - my_sum[0]) / (row_end-row_start-1))
    return delta_t

# def is_max_increase(delta_t, pixel_avging_nb, pixel_pt):
#     for i in range(pixel_avging_nb):
#         if delta_t[pixel_pt] < delta_t[i] and i != pixel_pt:
#             return False
#     return True

# def is_valid_increase(delta_t, pixel_pt, current_max):
#     if delta_t[pixel_pt] < current_max / 30 or delta_t[pixel_pt] > current_max / 2:
#         return False
#     return True

# def is_max_decrease(delta_t, pixel_avging_nb, pixel_pt):
#     for i in range(pixel_avging_nb):
#         if delta_t[pixel_pt] > delta_t[i] and i != pixel_pt:
#             return False
#     return True

# def is_valid_decrease(delta_t, pixel_pt, current_max):
#     if delta_t[pixel_pt] > -current_max / 30 or delta_t[pixel_pt] < -current_max / 2:
#         return False
#     return True

# def is_increase_glitch(delta_t, pixel_avging_nb, pixel_pt):
#     sum_delta = 0
#     for i in range(pixel_avging_nb):
#         sum_delta += delta_t[i] 
#     if delta_t[pixel_pt] > sum_delta:
#         return True
#     else:
#         return False

# def is_decrease_glitch(delta_t, pixel_avging_nb, pixel_pt):
#     sum_delta = 0
#     for i in range(pixel_avging_nb):
#         sum_delta += delta_t[i]
#     if delta_t[pixel_pt] < sum_delta:
#         return True
#     else:
#         return False

process = False
for input_file_path in sorted(glob.glob(input_folder + os.sep + "*.TIF"),  reverse=reverse):
    if input_file_path.endswith(first):
        process = True
    elif input_file_path.endswith(last):
        process = False
    if process:
        tstart = timeit.default_timer()
        file_name = input_file_path.split(os.sep)[-1]
        # input_file_path = '2023_04_20_IMG_0887bb.TIF'
        # file_name = input_file_path.split(os.sep)[-1]
        file_nb += 1
        print(f"\n{file_nb}. Reading Image file: {input_file_path}")
        image_array = tiff.imread(input_file_path)
        print(f"\tImage Size: {image_array.shape[1]}x{image_array.shape[0]}. Type: {image_array.dtype}.")
        if image_array.dtype == 'uint16':
            sum_max = 256 * 256 * 3
        elif image_array.dtype == 'uint8':
            sum_max = 256 * 3
        image_pixels_nb = image_array.shape[1] * image_array.shape[0]
        info_org = tifftools.read_tiff(input_file_path)

        t0 = timeit.default_timer()
        variation_dict = {'x': [], 'y': []}
        debug_dict = {'x': [], 'y': []}
        previous_progression = -1
        print("\tAnalyzing... Please be patient...")
        sum_list = []
        image_size = int(image_array.shape[1]) * int(image_array.shape[0])
        sum_avg = 0
        current_max = 0
        nb_saturated_pixels = 0
        for row_idx in range(image_array.shape[0]):
            progression = int(100*row_idx/(image_array.shape[0] - 1))
            if progression != previous_progression:
                print(f"\t\tParsing Progression: {int(progression)}%", end="\r", flush=True)
            previous_progression = progression
            # col_sum = []
            # for col_idx in range(image_array.shape[1]):
            #     current_sum = sum(image_array[row_idx][col_idx])
            #     current_max = max(current_max, current_sum)
            #     if current_sum > sum_max * 0.999:
            #         nb_saturated_pixels += 1
            #     col_sum.append(current_sum)
            #     sum_avg += current_sum / image_size

            col_sum = image_array[row_idx].sum(axis=1, dtype='int64')
            current_max = max(current_max, max(col_sum))
            nb_saturated_pixels += sum(col_sum > sum_max * 0.999)
            sum_list.append(col_sum)
        percentage_saturated_pixels = round(100 * nb_saturated_pixels / image_pixels_nb, 2)
        sum_avg = int(round(sum(sum(sum_list)) / image_size, 0))
        print(f"\n\t\tPixel Average Value: {sum_avg}")
        print(f"\t\tPixel Max Value: {current_max}")
        print(f"\t\tSaturated Pixels Percentage: {percentage_saturated_pixels}%")

        # delta_t = [sum(sum_list[row+1][:pixel_avging_nb])/pixel_avging_nb - sum(sum_list[row][:pixel_avging_nb])/pixel_avging_nb for row in range(pixel_avging_nb)]
        # delta_t = get_delta(sum_list, 0, pixel_avging_nb, 0, pixel_avging_nb)
        # print(delta_t)
        # print(len(sum_list[0]), sum_list[0])
        # print(len(sum_list[1]), sum_list[1])
        # print(len(sum_list[:2][0]), sum_list[:2])
        # exit()
        for row_idx in range(image_array.shape[0]):
            progression = int(100*row_idx/(image_array.shape[0] - 1))
            if progression != previous_progression:
                print(f"\t\tRow Processing Progression: {int(progression)}%", end="\r", flush=True)
            previous_progression = progression
            variation_data = [0, 0]
            location_data = [[0, 0], [0, 0]]
            # debug_data = [[], []]
            # sum_t = [sum_list[row_idx][i] for i in range(pixel_avging_nb)]
            delta_t = [sum_list[row_idx][i+1] - sum_list[row_idx][i] for i in range(pixel_avging_nb)]
            for col_idx in range(pixel_avging_nb+1, image_array.shape[1]-1):
                # sum_t.append(sum_list[row_idx][col_idx])
                # delta_t = [sum_t[i+1] - sum_t[i] for i in range(pixel_avging_nb)]
                
                # if row_idx == 2069 and (465 < col_idx < 480): # or 3015 < col_idx < 3025 or 5355 < col_idx < 5365 or 5425 < col_idx < 5435):
                #     print(row_idx, col_idx, sum_t, delta_t, variation_data, debug_data, is_valid_increase(delta_t, pixel_point, current_max), is_max_increase(delta_t, pixel_avging_nb, pixel_point), is_increase_glitch(delta_t, pixel_avging_nb, pixel_point), is_valid_decrease(delta_t, pixel_point, current_max), is_max_decrease(delta_t, pixel_avging_nb, pixel_point), is_decrease_glitch(delta_t, pixel_avging_nb, pixel_point))
                if is_valid_increase(delta_t, pixel_avging_nb, pixel_point, current_max) and variation_data[0] == 0: #  and is_max_increase(delta_t, pixel_avging_nb, pixel_point) and not is_increase_glitch(delta_t, pixel_avging_nb, pixel_point) and variation_data[0] == 0:
                    # debug_data[0] = [delta_t, copy.deepcopy(sum_t), [row_idx, col_idx - pixel_point], variation_data]
                    variation_data[0] = delta_t[pixel_point]
                    location_data[0] = [row_idx, col_idx - pixel_point]
                if is_valid_decrease(delta_t, pixel_avging_nb, pixel_point, current_max): # and is_max_decrease(delta_t, pixel_avging_nb, pixel_point) and not is_decrease_glitch(delta_t, pixel_avging_nb, pixel_point):
                    # debug_data[1] = [delta_t, copy.deepcopy(sum_t), [row_idx, col_idx - pixel_point], variation_data]
                    variation_data[1] = delta_t[pixel_point]
                    location_data[1] = [row_idx, col_idx - pixel_point]
                delta_t.append(sum_list[row_idx][col_idx+1] - sum_list[row_idx][col_idx])
                delta_t.pop(0)
                # delta_t = get_delta(sum_list, row_idx-pixel_point, row_idx-pixel_point+pixel_avging_nb, col_idx, col_idx-pixel_point+pixel_avging_nb)
                # print(col_idx, len())
                # delta_t = [sum_list[col_idx:col_idx+pixel_avging_nb+1][i+1].sum(axis=0)/pixel_avging_nb - sum_list[col_idx:col_idx+pixel_avging_nb+1][i].sum(axis=0)/pixel_avging_nb for i in range(pixel_avging_nb)]
            variation_dict['x'].append(location_data)
            # debug_dict['x'].append(debug_data)

        previous_progression = -1
        print("")
        for col_idx in range(image_array.shape[1]):
            progression = int(100*col_idx/(image_array.shape[1] - 1))
            if progression != previous_progression:
                print(f"\t\tCol Processing Progression: {int(progression)}%", end="\r", flush=True)
            previous_progression = progression
            variation_data = [0, 0]
            location_data = [[0, 0], [0, 0]]
            # debug_data = [[], []]
            # sum_t = [sum_list[i][col_idx] for i in range(pixel_avging_nb)]
            delta_t = [sum_list[i][col_idx] - sum_list[i][col_idx] for i in range(pixel_avging_nb)]
            for row_idx in range(pixel_avging_nb+1, image_array.shape[0]-1):
                # sum_t.append(sum_list[row_idx][col_idx])
                # delta_t = [sum_t[i+1] - sum_t[i] for i in range(pixel_avging_nb)]
                # if col_idx == 3010 and (820 < row_idx < 830 or 910 < row_idx < 920 or 2350 < row_idx < 2360 or 3300 < row_idx < 3310):
                #     print(row_idx, col_idx, sum_t, delta_t, variation_data, debug_data, is_valid_increase(delta_t, pixel_point, current_max), is_max_increase(delta_t, pixel_avging_nb, pixel_point), is_increase_glitch(delta_t, pixel_avging_nb, pixel_point), is_valid_decrease(delta_t, pixel_point, current_max), is_max_decrease(delta_t, pixel_avging_nb, pixel_point), is_decrease_glitch(delta_t, pixel_avging_nb, pixel_point))
                if is_valid_increase(delta_t, pixel_avging_nb, pixel_point, current_max) and variation_data[0] == 0: # and is_max_increase(delta_t, pixel_avging_nb, pixel_point) and not is_increase_glitch(delta_t, pixel_avging_nb, pixel_point) and variation_data[0] == 0:
                    # debug_data[0] = [delta_t, copy.deepcopy(sum_t), [row_idx - pixel_point, col_idx], variation_data]
                    variation_data[0] = delta_t[pixel_point]
                    location_data[0] = [row_idx - pixel_point, col_idx]
                if is_valid_decrease(delta_t, pixel_avging_nb, pixel_point, current_max): # and is_max_decrease(delta_t, pixel_avging_nb, pixel_point) and not is_decrease_glitch(delta_t, pixel_avging_nb, pixel_point):
                    # debug_data[1] = [delta_t, copy.deepcopy(sum_t), [row_idx - pixel_point, col_idx], variation_data]
                    variation_data[1] = delta_t[pixel_point]
                    location_data[1] = [row_idx - pixel_point, col_idx]
                delta_t.append(sum_list[row_idx+1][col_idx] - sum_list[row_idx][col_idx])
                delta_t.pop(0)
            variation_dict['y'].append(location_data)
            # debug_dict['y'].append(debug_data)

        t1 = timeit.default_timer()
        print(f"\n\tImage Analyzing Runtime: {round(t1-t0, 3)} second(s)...")

        max_diameter = {'x': 0, 'y': 0}
        sun_center_list = {'x': [0], 'y': [0]}
        # variation_debug = {'x': [], 'y': []}
        current_diameter = {}
        for axis, location_data_list_list in variation_dict.items():
            # first_pass = False
            # if not avg_sun_diameter_list_dict[axis]:
            #     first_pass = True
            # else:
            #     avg_sun_diameter_dict[axis] = sum(avg_sun_diameter_list_dict[axis]) / len(avg_sun_diameter_list_dict[axis])
            for idx, location_data_list in enumerate(location_data_list_list):
                if axis == 'x' and location_data_list[0][1] != 0: # and location_data_list[1][1] < sun_location_boundaries['x'][1] and location_data_list[0][1] > sun_location_boundaries['x'][0]:
                    current_diameter[axis] = location_data_list[1][1] - location_data_list[0][1]
                    current_center = location_data_list[0][1] + current_diameter[axis] / 2
                elif axis == 'y' and location_data_list[0][0] != 0: # and location_data_list[1][0] < sun_location_boundaries['y'][1] and location_data_list[0][0] > sun_location_boundaries['y'][0]:
                    current_diameter[axis] = location_data_list[1][0] - location_data_list[0][0]
                    current_center = location_data_list[0][0] + current_diameter[axis] / 2
                else:
                    current_diameter[axis] = 0
                # print(axis, variation_list, current_diameter, current_center)

                if current_diameter[axis] > max_diameter[axis]:
                    # if first_pass or avg_sun_diameter_dict[axis] * (1 + avg_sun_diameter_tolerance_pct / 100) > current_diameter[axis]:
                    max_diameter[axis] = current_diameter[axis]
                    sun_center_list[axis] = [current_center]
                        # variation_debug[axis] = [location_data_list, debug_dict[axis][idx]]
                elif current_diameter[axis] == max_diameter[axis] != 0:
                    sun_center_list[axis].append(current_center)

        # if first_pass:
        #     avg_sun_diameter_dict = copy.deepcopy(max_diameter)
        #     avg_sun_diameter_list_dict['x'].append(max_diameter['x'])
        #     avg_sun_diameter_list_dict['y'].append(max_diameter['y'])
        
        # if max_diameter['x'] < avg_sun_diameter_dict['x'] / (1 + avg_sun_diameter_tolerance_pct / 100):
        #     print(f"WARNING/INFO: Current Diameter on x is too small: {max_diameter['x']}. Will determine the center based on the avg diameter")
        #     print(f"Current Average Diameter: {avg_sun_diameter_dict}")
        #     print(f"\tDEBUG variation_list: {variation_debug}")
        #     min_location = max_location = None
        #     for idx, location_data_list in enumerate(variation_dict['x']):
        #         if min_location_is_ok:
        #             if location_data_list[0][1] != 0: # and location_data_list[0][1] > sun_location_boundaries['x'][0]:
        #                 if min_location is None or min_location > location_data_list[0][1]:
        #                     min_location = location_data_list[0][1]
        #                     sun_center['x'] = min_location + avg_sun_diameter_dict['x'] / 2
        #                     max_diameter['x'] = avg_sun_diameter_dict['x']
        #         else:
        #             if location_data_list[1][1] != 0: # and location_data_list[1][1] < sun_location_boundaries['x'][1]:
        #                 if max_location is None or max_location < location_data_list[1][1]:
        #                     max_location = location_data_list[1][1]
        #                     sun_center['x'] = max_location - avg_sun_diameter_dict['x'] / 2
        #                     max_diameter['x'] = avg_sun_diameter_dict['x']
        # else:
        #     avg_sun_diameter_list_dict['x'].append(max_diameter['x'])

        # if max_diameter['y'] < avg_sun_diameter_dict['y'] / (1 + avg_sun_diameter_tolerance_pct / 100):
        #     print(f"WARNING/INFO: Current Diameter on y is too small: {max_diameter['y']}. Will determine the center based on the avg diameter.")
        #     print(f"Current Average Diameter: {avg_sun_diameter_dict}")
        #     print(f"\tDEBUG variation_list: {variation_debug}")
        #     min_location = max_location = None
        #     for idx, location_data_list in enumerate(variation_dict['y']):
        #         if min_location_is_ok:
        #             if location_data_list[0][0] != 0: # and location_data_list[0][0] > sun_location_boundaries['y'][0]:
        #                 if min_location is None or min_location > location_data_list[0][0]:
        #                     min_location = location_data_list[0][0]
        #                     sun_center['y'] = min_location + avg_sun_diameter_dict['y'] / 2
        #                     max_diameter['y'] = avg_sun_diameter_dict['y']
        #         else:
        #             if location_data_list[0][0] != 0: # and location_data_list[1][0] < sun_location_boundaries['y'][1]:
        #                 if max_location is None or max_location < location_data_list[1][0]:
        #                     max_location = location_data_list[1][0]
        #                     sun_center['y'] = max_location - avg_sun_diameter_dict['y'] / 2
        #                     max_diameter['y'] = avg_sun_diameter_dict['y']
        # else:
        #     avg_sun_diameter_list_dict['y'].append(max_diameter['y'])


        # print(f"\tPicture center: {image_array.shape[1]/2} x {image_array.shape[0]/2}")
        # print(f"\tDEBUG variation_list: {variation_debug}")
        sun_center = {
            'x': np.average(sun_center_list['x']),
            'y': np.average(sun_center_list['y'])
        }
        print(f"\tMax Arc or Diameter: {max_diameter}")
        print(f"\tSun center: {sun_center['x']} x {sun_center['y']}")
        x_shift = round(image_array.shape[1] / 2 - sun_center['x'], 0)
        y_shift = round(image_array.shape[0] / 2 - sun_center['y'], 0)
        print(f"\tImage X-Shift: {x_shift}. Image Y-Shift: {y_shift}")
        # if abs(max_diameter['y'] - max_diameter['x']) > 20 or max_diameter['x'] == 0 or max_diameter['y'] == 0:
        #     print("\tERROR: Sun Diameter is not looking good!!")
        #     print(f"\tDEBUG variation_list: {variation_debug}")
        #     exit()
        # elif abs(max_diameter['y'] - max_diameter['x']) > 5 or max_diameter['x'] == 0 or max_diameter['y'] == 0:
        #     print("\tWARNING: Sun Diameter is not looking good!!")
        #     print(f"\tWARNING variation_list: {variation_debug}")

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
            try:
                os.remove(temp_output_file_path)
            except:
                print(f"ERROR: Could not remove temporary file {temp_output_file_path}. To be done manually!!")
        t1 = timeit.default_timer()
        print(f"\tImage Writing Runtime: {round(t1-t0, 3)} second(s)...")

        tend = timeit.default_timer()
        print(f"\tImage Full Process Runtime: {round(tend-tstart, 3)} second(s)...")

