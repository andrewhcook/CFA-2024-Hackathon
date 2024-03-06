import signal
from gpiozero import Button, LED
import subprocess
import numpy as np
import librosa
import time
from time import sleep
from scipy.stats import median_abs_deviation
import os

buffer = []

# Set the duration and sample rate
max_duration = 120  # seconds
fs = 44100  # Sample rate



recording_file = "/home/ac/recording"
file_extension = ".wav"
filename = recording_file + file_extension
trimmed_filename =   recording_file + "-trimmed" + file_extension
pre_trimmed_filename = recording_file + "-pre-trimmed" + file_extension
temp_filename = "/home/ac/temp" + file_extension
exists = os.path.exists(filename)
if not exists:
    with open(os.path.join(filename), 'w') as fp:
        pass
other_exists = os.path.exists(trimmed_filename)

if not other_exists:
    cmd = "arecord -f S16_LE -d 5 -c 1 -r 44100 {}".format(trimmed_filename)
    subprocess.call(cmd, shell=True)

temp_exists = os.path.exists(temp_filename)
if not temp_exists:
    with open(os.path.join(temp_filename), 'w') as fp:
        pass

temp2_exists = os.path.exists(pre_trimmed_filename)

if not temp2_exists:
    cmd = "ffmpeg -i {} -c copy {}".format(trimmed_filename, pre_trimmed_filename)
    subprocess.call(cmd, shell = True)


green_led = LED(23)
red_led = LED(24)


def process_terminate():
    # Terminate the recording process
    process.terminate()


def record_audio():
    green_led.on()
    red_led.on()
    sleep(3)
    green_led.off()
    red_led.off()
    command = [ "arecord", "-f", "S16_LE", "-c", "1", "-r", "44100", filename]
    global process
    process = subprocess.Popen(command)



def green_LED_on():
    green_led.on()
    sleep(2)
    green_led.off()


def red_LED_on():
    red_led.on()
    sleep(2)
    red_led.off()



def get_duration(file_path):
    cmd = 'ffprobe -i {} -show_entries format=duration -of csv="p=0"'.format(file_path)
    bytecode = subprocess.check_output(cmd, shell=True)
    string = bytecode.decode("utf-8")
    output = float(string)
    print(output)
    return float(output)  # Duration in seconds


def clip_last_two_minutes(file_path, output_path):
    duration = get_duration(file_path)
    if duration < 120:
        cmd = 'ffmpeg -y -i {} -t 120  {}'.format(file_path, output_path)
        subprocess.call(cmd, shell=True)
    else:
        start_time = duration - 120
        cmd = 'ffmpeg -y -i {} -ss {} -t 120 {}'.format(file_path, start_time, output_path)
        subprocess.call(cmd, shell=True)


def signal_handler():
    process_terminate()
    # add files together
    cmd= 'ffmpeg -y -i {} -i {} -filter_complex [0:a][1:a]concat=n=2:v=0:a=1 {}'.format(trimmed_filename, filename, pre_trimmed_filename)
    subprocess.call(cmd, shell=True)

    clip_last_two_minutes(pre_trimmed_filename, trimmed_filename)


    y, sr = librosa.load(trimmed_filename)

    # Extract the first 1 minute and 45 seconds (105 seconds)
    y_start = y[:105 * sr]

    # Extract the last 15 seconds
    y_end = y[-15 * sr:]

    # Extract features (MFCCs)
    mfcc_start = librosa.feature.mfcc(y=y_start, sr=sr)
    mfcc_end = librosa.feature.mfcc(y=y_end, sr=sr)

    # Compute the mean and MAD of each MFCC
    mean_mfccs_start = np.mean(mfcc_start, axis=1)
    mad_mfccs_start = median_abs_deviation(mfcc_start, axis=1)

    mean_mfccs_end = np.mean(mfcc_end, axis=1)
    mad_mfccs_end = median_abs_deviation(mfcc_end, axis=1)

    # Initialize a list to hold the outliers
    outliers = []

    # Define a threshold for outlier detection
    threshold = 1.5
    print(len(mean_mfccs_start))
    # Check each MFCC of each frame for outliers
    for i, (median_start, mad_start, median_end, mad_end) in enumerate(
            zip(mean_mfccs_start, mad_mfccs_start, mean_mfccs_end, mad_mfccs_end)):
        if median_end < median_start - threshold * mad_start or median_end > median_start + threshold * mad_start:
            outliers.append(i)
    if len(outliers) > 0:
        print("signal detected")
        green_LED_on()
    else:
        print("no signal detected")
        red_LED_on()
    print("found {} outlier(s)".format(len(outliers)))
    print("stamps: {}".format(outliers))
    record_audio()


button = Button(27)
button.when_pressed = signal_handler
record_audio()
signal.pause()

