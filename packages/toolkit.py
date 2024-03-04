import datetime
import time
import logging
import os
import threading

def set_log(prefix, log_folder='logs'):
    # date
    date_time = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")

    # create logger and formater
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formater = logging.Formatter('%(asctime)s.%(msecs)03d - %(levelname)-8s: %(message)s', "%Y-%m-%d %H:%M:%S")

    # file handler
    if not os.path.isdir(log_folder):
        os.makedirs(log_folder)
    fh = logging.FileHandler(log_folder + os.sep + f"{prefix}-{date_time}.log")
    fh.setFormatter(formater)
    fh.setLevel(logging.INFO)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setFormatter(formater)
    ch.setLevel(logging.INFO)

    # add ch and fh to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

def log_execution_time(execution, start_time, end_time, unit="ms"):
    if unit == "s":
        scale = 1
    elif unit == "ms":
        scale = 1e3
    else:
        logging.info(f"Unit {unit} not supported. Default is s")
        scale = 1
        unit = "s"
    execution_time = round(scale * (end_time - start_time), 3)
    logging.info(f"{execution} done in {execution_time}{unit}.")

def foo():
	print(time.ctime())
	threading.Timer(10, foo).start()