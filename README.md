# H1 Cognitive Remediation Tool for Auditory Hallucinations

This script is to be used with an initialized Raspberry Pi running (Raspberry Pi OS 64-bit full) connected to an IQaudIO Codec Zero HAT.

## H2 Raspberry Pi Initialization:
Follow the steps at: https://www.raspberrypi.com/documentation/computers/getting-started.html

I used a RPi Zero 2 W but any model with standard 40 GPIO pins will work with the HAT.

## H2 Codec Zero Attachment and Configuration:
Follow the steps for the Codec Zero at: https://www.raspberrypi.com/documentation/accessories/audio.html


## H2 Project Idea: A device to be used in cognitive remediation for auditory hallucinations

- This python script interacts with the Raspberry Pi and attached hardware to record ambient sound and compare the last 15 seconds of recording versus the prior minute and 45 seconds.
- If a novel sound signal is detected a green LED on the Codec Zero lights up, if not a red LED lights up.
- This can be used by an indivual expericing transient auditory hallucinations to differentiate a hallucination from an actual ambient sound.
