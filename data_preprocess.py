import argparse
import os
from pydub import AudioSegment
from scipy.io.wavfile import write
import numpy as np
import re

DATA_PATH = "../data/cts_news"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--time_limit",default=120, type=int)
    args = parser.parse_args()
    
    for file in os.listdir(DATA_PATH):
        if file.endswith("mp3"):
            convert_to_inference_data(file, args.time_limit)

    text_preprocess()


def convert_to_inference_data(file, time_limit):
    origin_path = os.path.join(DATA_PATH, file)
    target_path = os.path.join(DATA_PATH, "wav", file[:-4] + ".wav")

    print(origin_path, target_path)
    
    try:
        sound = AudioSegment.from_mp3(origin_path)
    except Exception as e:
        print(f"Can't load {origin_path}")
        return

    
    if sound.duration_seconds > time_limit:
        print(f"{file} is longer than 120 sec...")        
        return
    
    sound = sound.set_frame_rate(8000) # workaround
    sound = sound.set_sample_width(2)

    sound_array = np.array(sound.get_array_of_samples())
    sound_array = sound_array.astype("int16")
    
    soundfile.write(target_path, sound_array, 16000, subtype='PCM_16')
    print(f"Converted and saved at {target_path}")


def text_preprocess():
    source_path = os.path.join(DATA_PATH, "trans_origin.txt")
    with open(source_path) as f:
        s = f.read()
    s = s.split("\n")
    
    new_list = []
    for text in s:
        text = re.sub(r"\t.*?[市|縣|國]", "\t", text)
        text = re.sub(r"新聞來源.+", "", text)
        text = text.split("\t")
        text[0] = text[0].replace("mp3", "wav")

        text = "\t".join(text)
        new_list.append(text)
    print(f"Got {len(new_list)} lines data.")
    target_path = os.path.join(DATA_PATH, "wav", "trans_processed.txt")
    with open(target_path, "w+") as f:
        f.write("\n".join(new_list))
    print(f"save at {target_path}")


if __name__ == "__main__":
    main()
    
    