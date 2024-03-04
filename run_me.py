# MIT License

# Copyright (c) 2023 [Philippe Lopez]

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
import os
import argparse
from configparser import ConfigParser

from ctypes import *
edsdk = windll.edsdk

from packages.toolkit import set_log
from packages.eos_dslr import EOS_DSLR
from packages.eos_eclipsis import EOS_ECLIPSIS

set_log(prefix=os.path.basename(__file__).split('.')[0])

parser = argparse.ArgumentParser(description='Eclipsis - Automated Eclipse Photography')
parser.add_argument('cfg', type=str, help='Configuration file')
parser.add_argument('--run_partial', action='store_true', help='Force to execute the Partial phase as planned regardless of the contacts date/time provided except for the duration defined as the maximum one between C1-C2 and between C3-C4')
parser.add_argument('--run_drings', action='store_true', help='Force to execute the Diamonds Ring phase as planned regardless of the contacts date/time provided except for the duration defined with overlap over totality and partial phase')
parser.add_argument('--run_totality', action='store_true', help='Force to execute the Totality phase as planned regardless of the contacts date/time provided except for the duration between C2-C3 minus the C2&C3 Time overlap')
parser.add_argument('--run_totality_panic', action='store_true', help='Force to execute the Totality phase as planned regardless of the contacts date/time provided at the fastest pace as possible')
parser.add_argument('--run_annularity', action='store_true', help='Force to execute the Annularity phase as planned regardless of the contacts date/time provided except for the duration between C2-C3 minus the C2&C3 Time overlap')
parser.add_argument('--test', action='store_true', help='Test the inputs from the configuration for debug')
parser.add_argument('--test_tse_rescheduler', action='store_true', help='Test the behavior of the totality resheduler during totality used when running late')
parser.add_argument('--ase', action='store_true', help='Running for Annular Solar Eclipse')

args = parser.parse_args()

if not os.path.isfile(args.cfg):
    logging.critical(f'Config file {args.cfg} does not exist')
if args.cfg is None or not os.path.isfile(args.cfg):
    ini_files_list = []
    for dirpath, subdirs, files in os.walk('.'):
        ini_files_list += [dirpath + os.sep + file for file in files if file.endswith('.ini')]
    if ini_files_list:
        print("Select an ini file:")
        for idx, ini_file in enumerate(ini_files_list):
            print('{0:2}: {1}'.format(idx, ini_file))
        selection = -1
        while (int(selection) < 0 or int(selection) >= len(ini_files_list)):
            selection = input('Select a Config File: ')
            if not selection.isdigit():
                selection = -1
        try:
            args.cfg = ini_files_list[int(selection)]
        except:
            logging.error(f"Invalid selection {selection}")
            exit()
    else:
        logging.critical("No config files found!")
        exit()

config = ConfigParser()
config.read(args.cfg)

# Mandatory
Error_Flag = False
contacts_date_time_dict = {}
for s in ['date', 'time']:
    for i in range(4):
        try:
            contacts_date_time_dict[f'c{i+1}_{s}'] = config.get('contacts_date_time', f'c{i+1}_{s}')
        except:
            logging.critical(f'Could not get c{i} {s} information from Configuration File')
            Error_Flag = True

knobs_dict = {}
required_knobs_dict = {
    'cam_settings': ['iso', 'aperture'],
    'partial': ['partial_period'],
    'totality': ['totality_sweep_shutterspeed', 'totality_sweep_aperture', 'totality_sweep_iso'],
    'annularity': ['annularity_period'],
}
for config_section, knobs_list in required_knobs_dict.items():
    for knob in knobs_list:
        try:
            knobs_dict[knob] = config.get(config_section, knob)
        except:
            if config_section == 'totality' and args.ase or config_section == 'annularity' and not args.ase:
                continue
            else:
                logging.critical(f'Could not get {knob} information from Configuration File')
                Error_Flag = True

# Optional
optionals_knobs_dict = {
    'partial': {
        'partial_shutterspeed'       : None, 
        'partial_shot_redundancy'    : '0',
        'partial_shot_duration'      : '0'
    },
    'c2_c3': {
        'before_c2_or_after_c3_time' : '0', 
        'after_c2_or_before_c3_time' : '0', 
        'c2_c3_shutterspeed'         : None, 
        'c2_c3_drive_mode'           : 'Single shooting'
    },
    'totality': {
        'totality_drive_mode'        : 'High speed continuous +', 
        'totality_max_fps'           : '8'
    },
    'annularity': {
        'annularity_shutterspeed'    : None, 
        'annularity_shot_redundancy' : '0',
        'annularity_shot_duration'   : '0'
    },
    'general': {
        'print_execution_time'       : 'False'
    },
    'cam_settings': {
        'busy_period_guarband'       : '0.5',
        'auto_focus_mode'            : 'Off',
        'loop_value'                 : 1,
    }
}
for config_section, knobs_default_dict in optionals_knobs_dict.items():
    for knob, default_value in knobs_default_dict.items():
        try:
            knobs_dict[knob] = config.get(config_section, knob)
        except:
            knobs_dict[knob] = default_value
            if config_section == 'totality' and args.ase or config_section == 'annularity' and not args.ase:
                continue
            elif default_value is not None:
                logging.warning(f'No setting for {config_section} {knob} from Configuration File. Will use default is {default_value}')
            else:
                logging.warning(f'No setting for {config_section} {knob} from Configuration File. Will be calculated')

if Error_Flag:
    exit()

edsdk.EdsInitializeSDK()

if args.test or args.test_tse_rescheduler:
    MyEOS = None
else:
    MyEOS = EOS_DSLR()

MyProg = EOS_ECLIPSIS(
    camera=MyEOS,
    contacts_date_time_dict=contacts_date_time_dict,
    knobs_dict=knobs_dict,
    annular_eclipse=args.ase,
    test_tse_rescheduler=args.test_tse_rescheduler
)
if args.run_partial:
    MyProg.partial_phase(force_exec=True)
elif args.run_drings:
    MyProg.c2_c3_phases(force_exec=True)
elif args.run_totality:
    MyProg.totality_phase(force_exec=True)
elif args.run_totality_panic:
    MyProg.totality_phase(panic_mode=True)
elif args.run_annularity:
    MyProg.annularity_phase(force_exec=True)
elif args.ase:
    MyProg.run_ase()
else:
    MyProg.run_tse()