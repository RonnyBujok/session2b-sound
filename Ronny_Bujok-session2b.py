import csv
import os
from pydub import AudioSegment, silence
from pydub.playback import play

# We have three conditions: High Frequency (HF), Low Frequency (LF), and Non-Words (NW).
# All words for each condition are stored in one .wav file.
# Your task is to:
#       split the words on the silence
#       make sure they all have the same loudness
#       save them in a folder corresponding to their condition (folder names: HF, LF, NW)

path_to_repository = "K:\\01. Ronny_PhD\\02. IMPRS\\Courses\\Python\\session2b-sound\\session2b-sound"  # add your own path here!

# This piece of code is here to help you.
# It reads a text file with information about the stimuli you are going to split (names & condition),
# and returns a dictionary named 'stimuli' with condition as key, and the word itself as value.
# Use this dictionary to name the files you have to save.
stimuli_info = open(os.path.join(path_to_repository, "lexdec_stimuli.txt"))
stimuli_reader = csv.reader(stimuli_info, delimiter=',')
headers = next(stimuli_reader, None)

# Create the dictionary
stimuli = {}
for stimulus in stimuli_reader:
    if stimulus[2] not in stimuli.keys():
        stimuli[stimulus[2]] = list()
    stimuli[stimulus[2]].append(stimulus[3])

# Put them in alphabetical order
for condition, words in stimuli.items():
    sort = sorted(words)
    stimuli[condition] = sort

# change the non-word condition name
stimuli["NW"] = stimuli.pop("none")

# Now you have the stimulus names. Let's take a look at the dictionary:
print(stimuli)




# YOUR CODE HERE.




# where are the soundfiles?
sound_folder = "K:\\01. Ronny_PhD\\02. IMPRS\\Courses\\Python\\session2b-sound\\session2b-sound\\raw"

# create new folders for all three conditions

new_folder_HF = "K:\\01. Ronny_PhD\\02. IMPRS\\Courses\\Python\\session2b-sound\\session2b-sound\\HF"
if not os.path.isdir(new_folder_HF):
    os.mkdir(new_folder_HF)
new_folder_LF = "K:\\01. Ronny_PhD\\02. IMPRS\\Courses\\Python\\session2b-sound\\session2b-sound\\LF"
if not os.path.isdir(new_folder_LF):
    os.mkdir(new_folder_LF)
new_folder_NW = "K:\\01. Ronny_PhD\\02. IMPRS\\Courses\\Python\\session2b-sound\\session2b-sound\\NW"
if not os.path.isdir(new_folder_NW):
    os.mkdir(new_folder_NW)

# create silence
silent_time = AudioSegment.silent(duration=200)

# load the full sound files

sound_path_HF = os.path.join(sound_folder, "HF_recording.wav")
sound_path_LF = os.path.join(sound_folder, "LF_recording.wav")
sound_path_NW = os.path.join(sound_folder, "NW_recording.wav")
sound_HF = AudioSegment.from_wav(sound_path_HF)
sound_LF = AudioSegment.from_wav(sound_path_LF)
sound_NW = AudioSegment.from_wav(sound_path_NW)

# split sound file on silences into all the individual stimuli

list_HF = silence.split_on_silence(sound_HF, min_silence_len=200, silence_thresh=-50)
list_LF = silence.split_on_silence(sound_LF, min_silence_len=200, silence_thresh=-50)
list_NW = silence.split_on_silence(sound_NW, min_silence_len=200, silence_thresh=-50)

# create new lists that will contain the stimuli with normalized volume

list_HF_normalized = []
list_LF_normalized = []
list_NW_normalized = []

# set target volume (arbitrary number for the purpose of this exercise)
target_volume = -6

# make the volume equal for all stimuli in all three , do that for all stimuli individually! Append the normalized
# files to the previously defined lists

for sound in list_HF:
    change = target_volume - sound.dBFS
    target_sound = sound.apply_gain(change)
    list_HF_normalized.append(target_sound)
for sound in list_LF:
    change = target_volume - sound.dBFS
    target_sound = sound.apply_gain(change)
    list_LF_normalized.append(target_sound)
for sound in list_NW:
    change = target_volume - sound.dBFS
    target_sound = sound.apply_gain(change)
    list_NW_normalized.append(target_sound)


# export all individual files as wav into the new folders! Name them with the names contained in the dictionary!
# the index of the sound files in the lists corresponds to the index of the correct name in the list in the dictionary

for i in range(len(list_HF_normalized)):
    sound = list_HF_normalized[i]
    filename = stimuli['HF'][i] + '.wav'
    new_path = os.path.join(new_folder_HF, filename)
    sound.export(new_path, format='wav')

for i in range(len(list_LF_normalized)):
    sound = list_LF_normalized[i]
    filename = stimuli['LF'][i] + '.wav'
    new_path = os.path.join(new_folder_LF, filename)
    sound.export(new_path, format='wav')

for i in range(len(list_NW_normalized)):
    sound = list_NW_normalized[i]
    filename = stimuli['NW'][i] + '.wav'
    new_path = os.path.join(new_folder_NW, filename)
    sound.export(new_path, format='wav')

# Some hints:
# 1. Where are the stimuli? check
# 2. How loud do you want your stimuli to be? Store it in a variable check
# 3. Where do you want to save your files? Make separate folders for the conditions. check
# 4. Do you normalize the volume for the whole sequence or for separate words? Why (not)? Try it if you like :)
# must be for every stimulus individually because the average for every stimulus will be different
# check
# 5. You can check whether your splitting worked by playing the sound, or by printing the length of the resulting list
# CHECK
# 6. Use the index of the word [in the list of words you get after splitting]
# to get the right text from the dictionary. check
# 7. Recall you can plot your results to see what you have done.
# Good luck!
