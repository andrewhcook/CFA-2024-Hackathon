This script is to be used with an initialized Raspberry Pi running (Raspberry Pi OS 64-bit full) connected to an IQaudIO Codec Zero HAT.

Raspberry Pi Initialization:

Codec Zero Attachment and Configuration:

Project Idea:
A device to be used in cognitive remediation for auditory hallucinations

- This python script interacts with the Raspberry Pi and attached hardware to record ambient sound and compare the last 15 seconds of recording versus the prior minute and 45 seconds.
- If a novel sound signal is detected a green LED on the Codec Zero lights up, if not a red LED lights up.
- This can be used by an indivual expericing transient auditory hallucinations to differentiate a hallucination from an actual ambient sound.
