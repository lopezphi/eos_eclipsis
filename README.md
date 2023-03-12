# EOS ECLIPSIS - Automated Eclipse Photography

## LICENSE DISCLAIMER
**MIT License**

**Copyright (c) 2023 [Philippe Lopez]**

**Permission is hereby granted, free of charge, to any person obtaining a copy**
**of this software and associated documentation files (the "Software"), to deal**
**in the Software without restriction, including without limitation the rights**
**to use, copy, modify, merge, publish, distribute, sublicense, and/or sell**
**copies of the Software, and to permit persons to whom the Software is**
**furnished to do so, subject to the following conditions:**

**The above copyright notice and this permission notice shall be included in all**
**copies or substantial portions of the Software.**

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR**
**IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,**
**FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE**
**AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER**
**LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,**
**OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE**
**SOFTWARE.**

## Overview
- This little piece of software run codes in batch mode (no Graphical User Interface).
- It uses the Canon SDK library: https://developercommunity.usa.canon.com/s/downloads/camera-downloads
- The code is written in python https://www.python.org/
- It controls one Canon EOS camera during a Solar Eclipse to execute exposure sequences 
as defined in a configuration file, for Partial / Diamonds Ring and Totality Phases.
    - During Totality, based on the number of photos, total exposure time, max frames per second
    and average busy time, it will determine a period of time for each photo based on its exposure
    to shoot in burst mode.
    - During Totality and Diamond Rings Phase, the camera will take no break and will take as many
    photos as possible.
    - During Totality, the expected Shoot mode is continuous, and even though the duration for 
    several shots are identical, it will result having different number of photos for each shot,
    but at least one.
- It will try to automatically recover any delays due to an unexpected unresponsive
camera or unexpected intensive activites on the laptop or for whatever reasons in any phases during 
the execution of the code itself.
- It can also jump to the right phase execution if it is started belated to catch up on the plan.
So it can be restarted anytime several times in case you get disconnected with the camera 
(while changing the baterry for example, and for whatever reasons) 
    - If it catch up during the Partial Phase, it will take one shot and synchronize back to original
    period of time as defined by the configuration file.
    - If it catch up during the Diamonds Ring Phase, it will execute the plan in a shorter (the 
    remaining) period of time.
    - If it catch up during the Totality Phase and the remaining time period is still ok, it will shorten
    the period of burst time for each photo of the sweep sequence. If the remaining time is too short to 
    be executed properly, it will determine a shorter sweep sequence to be able to be executed properly 
    during that time left. Worst case will be to determine and use the shortest possible sweep sequence 
    with 1/1 step for both ISO and Shutter Speed and run it even if there is not enough time margin.
- It can also execute the plan as defined but outside the defined contact times for any Phases
in case the laptop get desynchronized with the time or you are not where you were supposed 
to be or for whatever reasons. It will immediately execute:
    - For the Partial phase, it will take the longest duration between C1-C2 and C3-C4, and 
    take a shot at every period of of time as defined, during that duration.
    - For the Diamond Rings phase, it will use the 2 overlaps period of time as defined to take 
    photos consecutively in that given lapse of time.
    - For the Totality phase, it will use the C2-C3 period of time to execute the sweep
    sequence as defined in the configuration file.
- If this is the end of the world, the laptop is desynchronized or you landed in an unexpected 
location and you are just very late on the Totality Phase, there is your last chance ticket: 
a panic mode to execute the plan for the Totality at the fastest pace.

## Usage disclaimer
- You're free to use this code, which is guaranteed to be not bug-free.
- And before using it, you are more than advised to intensively test it over and over and over
again the code along with your configuration file, and in many 'scenarios' to check how it 
behaves and check you get what you would expect to get. The rule is: What has not been tested 
does not work, and what has been tested can work, and not vice versa.

## How it works?
1. Define your execution plan in the configuration file.
    1. C1 C2 C3 C4 Contacts Date and Time.
    2. The default Aperture Value and ISO Speed.
    3. Define an estimated average camera busy time after a single shot.
    4. Define if you want to turn On Auto Focus during Partial + Diamond Rings (Default is Off).
    5. Partial Phases:
        1. Define the Shutter Speed or let the program calculate one (and decide to use it or not!),
        2. Define the period of time for shooting,
        3. Define any shot redundancy at every period cycle.
    6. Diamonds Ring Phases:
        1. Define the Shutter Speed or let the program calculate one (and decide to use it or not!),
        2. Define the time window for shooting during the end/beginning of Partial and Totality Phases,
        3. No period of time for shoting: It will take successive shots,
        3. Define the Drive Mode of the Camera (Highly recommended is Single Shot. In Continuous mode, 
        the camera will propbably hang for a very long (too) period of time (5-10s) at the end of this 
        Phase, leading to enter the Totality Phase late!).
    7. Totality Phase:
        1. Define the sweep for the exposure with a start, end and step points,
        2. Define the same for the ISO, but can be defined as an empty list,
        3. Define the Drive Mode of the Camera (Highly recommended a High Speed Continuous),
        4. Define the maximum frame per second supported by the Camera (BE conservative as the camera will 
        run into buffer overflow during this very stressful phase).
2. Test the configuration file with the --test knob without the Camera connected for a quick inputs check.
It does not replace testing the configuration file along with the camera.
3. Plug the camera to the laptop and stop any Canon Utilities or any softwares that
would connect to the Camera.
4. Have a configuration file for test with current date and near time and check how it goes 
(check the log files) and make any adjustements if needed.
5. From whatever termninal and whatever OS, execute : `python run_me.py <config_file>`.

## How to use?
1. Help Menu: `python run_me.py --help`
2. Expected usage: `python run_me.py <config_file>`. And let it runs! Even if sadly you are late!
3. For other 'panic' modes, when whatever goes wrong unexpectedly, prepare some batch files to execute 
in one-click, like:
    1. `python run_me.py <config_file> --run_partial`
    2. `python run_me.py <config_file> --run_drings`
    3. `python run_me.py <config_file> --run_totality`
    4. `python run_me.py <config_file> --run_totality_panic`

## Limitation - Known bugs
- There is no watchdog to keep the camera connected while waiting without activities. And with a not 
too long time period during Partial Phase, that should be ok. Anyhow it is better to keep devices 
off for doing nothing to save on batteries.
- For sure, I'm very limited in this camera connection protocol. For now, I have been 
completely unsuccesful in trying to get information from the camera. I just know how to set. The handlers
are most likely wrong.
- The only known bugs are the unknown ones waiting in the wood to be catched and reported.
- This has been tested mainly for NonAF / Electronic Shutter / Burst Shoot only in Total Phase and 
Single Shot for others phases. Others usecases might be more fragile.