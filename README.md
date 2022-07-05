# MIDI to Thirty Dollar Website Converter

## About
Converts MIDI files to TDW Files. 

[Demo](https://youtu.be/ItuRIOVTB84)

## Usage 

* Clone This repo: `https://github.com/yangman946/MIDI-to-Thirty-Dollar-Website-.git`
* Install requirements `pip install -r requirements.txt`
* Add MIDI Files to [midi to 30 dollar website\in](https://github.com/yangman946/MIDI-to-Thirty-Dollar-Website-/tree/main/midi%20to%2030%20dollar%20website/in)
* Run `main.py`

Output files will show up at [midi to 30 dollar website\out](https://github.com/yangman946/MIDI-to-Thirty-Dollar-Website-/tree/main/midi%20to%2030%20dollar%20website/out)

## Running

I highly recommend you download the [Thirty Dollar Website rewrite](https://greasyfork.org/en/scripts/439347-thirty-dollar-rewrite) for a smoother playback, especially when dealing with larger files. 

Some MIDI Files also use non-percussion notes on channel 10 - which is reserved for percussion. This screws up the conversion so it is best to just disable percussion in [midi2tdw.py](https://github.com/yangman946/MIDI-to-Thirty-Dollar-Website-/blob/main/midi%20to%2030%20dollar%20website/midi2tdw.py)

## Contributing

This project is a work in progress, If you wish to contribute, submit a pull request and I will look at it ASAP. 

## Limitations

* 	~~Struggles with larger MIDI Files with more tracks and instruments~~ <-- Fixed by downloading the [Thirty Dollar Website rewrite](https://greasyfork.org/en/scripts/439347-thirty-dollar-rewrite)
* Haven't fully tested percussion
* Combining and timing bugs

