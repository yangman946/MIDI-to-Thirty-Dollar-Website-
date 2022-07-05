# MIDI to TDW converter by Clarence Yang 4/7/2022
# todo - clean up code

from mido import MidiFile
import sounds
import math
import os


# Takes an input file and converts it into a .🗿 output file 
class midi2tdw():

    def __init__(self, url):

        self.mid = MidiFile(url, clip=True) # Midi file to convert

        self.channels = [None] * 15 # one slot for each of the 15 channels
        
        self.NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.OCTAVES = list(range(11))
        self.NOTES_IN_OCTAVE = len(self.NOTES)
        self.errors = {
            'program': 'Bad input, please refer this spec-\n'
                    'http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/program_change.htm',
            'notes': 'Bad input, please refer this spec-\n'
                    'http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm'
        }

        # output .🗿 file
        self.output = f'out\\{os.path.splitext(os.path.basename(url))[0]}.🗿'

        # stores each track and their corresponding channel: track (indexed 0) - channel (indexed 1)
        self.tuple_list = []

        # stores all tracks in a single timeline
        self.stitchedtrack = []

        # tempo
        self.tempo = 500000

        # the length of each tick in microseconds
        self.tickduration = 0

        # total time in ticks elapsed
        self.elapsedtick = 0 

        self.settempo = False

        # begin stitching the tracks together
        self.stitch() 

    # main.py use
    def getoutput(self):
        return self.output   
        

    '''Simple functions'''
    def mspb2bpm(self, tempo): 
        """ converts microsecond per beat (MIDI default) to beats per minute 
        
        Parameter: 
            tempo: integer
                tempo is microseconds per beat 
        Returns: 
            BPM: integer 
        """

        return round(60/(tempo/1000000))


    def ticklength(self, tempo):
        """ calculates duration per tick in microseconds 
        
        Parameter: 
            tempo: integer
                tempo is microseconds per beat 
        Returns: 
            tick duration: float
        """
        
        return tempo/self.mid.ticks_per_beat 


    def ticklenght2bpm(self, ticks):
        """ calculates BPM of a tick delay
        
        Parameter: 
            ticks: integer
                total number of ticks in this delay
        Returns: 
            BPM: integer
        """
        length = abs(ticks) * self.tickduration #total time of note in microsec: 1 beat/length
        return self.mspb2bpm(length) # returns BPM


    ''' Stitching algorithm - will add and sort all events in a chronological timeline '''
    def stitch (self):
        for i, track in enumerate(self.mid.tracks):
            
            elapsedtick = 0 # will keep track of the current tick
            #print('Track {}: {}'.format(i, track.name))

            for msg in track:
                
                # record initial tempo 
                if (msg.type == "set_tempo" and self.settempo == False): 
                    self.settempo = True
                    # print(msg.tempo)
                    self.tempo = msg.tempo
                    self.tickduration = self.ticklength(self.tempo)
                    main = open(self.output, 'w')
                    main.write(f"!speed@{self.mspb2bpm(msg.tempo)}|")
                    main.close()


                # DEBUG code - isolate tracks
                '''
                if i != 9: 
                    continue
                '''

                # Set the instrument for the given channel
                if (msg.type == "program_change" and self.channels[msg.channel] == None):
                    
                    self.channels[msg.channel] = msg.program # sets each channels instrument 
                    print('Track {}: {} - channel {} sound {}'.format(i, track.name, msg.channel + 1, self.channels[msg.channel]))
                    self.tuple_list.append((i, msg.channel + 1)) # store the track and their respective channel



                '''
                if (msg.type == "note_on" or msg.type == "note_off" or msg.type == "set_tempo"):
                    if (msg.type != "set_tempo"):
                        if(msg.channel + 1 == 10 or i == 13): # lets not work with channel 10 or 13 for now
                            continue
                '''

                # keep track of current time
                elapsedtick += msg.time 
                
                # create a dictionary for the given event
                item = {
                    "msg": msg,
                    "tick": elapsedtick, # store the time it occurs in this track
                    "track": i
                }

                self.stitchedtrack.append(item) # add to stitched track


        self.stitchedtrack = sorted(self.stitchedtrack, key=lambda d: d['tick']) # sort the stitched track in ascending tick elapsed order

        '''
        # debug
        for item in stitchedtrack:
            if (item["msg"].type == "note_on" or item["msg"].type == "note_off"):
                print(item)
        '''


        print(self.tuple_list) # debug
        self.converttrack(self.stitchedtrack) # begin to convert the track



    def note_number_to_hz(self, note_number):
        """ Convert a (fractional) MIDI note number to its frequency in Hz.
        Parameter
            note_number : float
                MIDI note number, can be fractional.
        Returns
            note_frequency : float
                Frequency of the note in Hz.
        """
        # MIDI note numbers are defined as the number of semitones relative to C0
        # in a 440 Hz tuning
        return 440.0*(2.0**((note_number - 69)/12.0))


    def semitone(self, f):
        """ Calculates number of semitones a given frequency is above middle C
        Parameter:
            frequency: float
        Returns:
            semitones: integer
        """
        return round(12* math.log(f/261.63, 2))

    def generate_pitch_str(self, num: int) -> str:
        """ Formats pitch string
        Parameter: 
            pitch: integer
        Returns:
            pitch string: string
        """
        if num == 0:
            return ''
        else:
            return '@' + str(num)

            
    ''' converts MIDI to TDW '''
    def converttrack(self, stitchedtrack):
        
        combine = False 
        lastinterval = 0
        channelind = 0

        '''
        Loop through the track
        
        It is important to time each note in terms of the global tick: i.e., the time parameter is inaccurate here since it is relative to the last event in THAT SPECIFIC TRACK 
        hence not necessarily relative to the last played note (likely in another track).

        '''

        main = open(self.output, 'a', encoding="utf-8")

        # loop through the stitched track
        for index, item in enumerate(stitchedtrack):
            
            # if a tempo change has occurred
            if (item["msg"].type == "set_tempo"):
                # recalculate the tick duration
                self.tempo = item['msg'].tempo
                self.tickduration = self.ticklength(self.tempo)
                #main.write(f"!speed@{self.mspb2bpm(item['msg'].tempo)}|")
                #output += "_pause|" # or physical wait like another note or something
            
            # note played
            if (item["msg"].type == "note_on"):

                # we want to check the next note
                if (index < len(stitchedtrack)): # make sure we haven't reached the end of the script
                    i = index

                    # loop through each consecutive note to find a 'note_on' message
                    while i + 1 < len(stitchedtrack):
                        if stitchedtrack[i + 1]["msg"].type == "note_on": # if we found it
                            #calculate the delay to the next note
                            delay = stitchedtrack[i + 1]["tick"] - item["tick"]
                            if delay == 0: # if there's no delay then the notes are played simultaneously 
                                combine = True # combine the notes
                            elif lastinterval != delay: # we do not want to change the BPM if it hasn't changed
                                lastinterval = delay 
                                main.write(f"!speed@{self.ticklenght2bpm(delay)}|") # change the speed
                            break
                        else:
                            i += 1
                    
            
                # loop the tuple list to find the tracks instrument
                for i in self.tuple_list:
                    if i[0] == item["track"]:
                        channelind = i[1] # fetch the channel index of this track

                # convert the note into a TDW emoji 
                if (len(self.tuple_list) == 0): # sometimes midi files do not specify an instrument - default to 0 - piano
                    main.write(f"{sounds.sounds[0]}{self.generate_pitch_str(self.semitone(self.note_number_to_hz(item['msg'].note)))}|") 
                elif (channelind == 10 and self.channels[channelind - 1] in sounds.percussion_sounds): # sometimes MIDI files use non percussion notes in channel 10 (reserved for percussion)
                    main.write(f"{sounds.percussion_sounds[self.channels[channelind-1]]}{self.generate_pitch_str(self.semitone(self.note_number_to_hz(item['msg'].note)))}|")
                else: 
                    
                    if (channelind == 10):
                        combine = False
                        continue

                    # add the sound
                    main.write(f"{sounds.sounds[self.channels[channelind-1]]}{self.generate_pitch_str(self.semitone(self.note_number_to_hz(item['msg'].note)))}|") 

                if combine:
                    main.write("!combine|")
                    combine = False

        main.close()

# debug
# midi2tdw(f'in\\test7.mid')



