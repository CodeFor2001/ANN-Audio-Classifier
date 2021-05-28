# -*- coding: utf-8 -*-
import os
import librosa
import math
import json

DATASET_PATH = "sound_leak"
JSON_PATH = "new_data.json"
SAMPLE_RATE = 22050
SAMPLES_PER_TRACK = SAMPLE_RATE*7
def save_mfcc(dataset_path, json_path, n_mfcc = 13, n_fft=2048, hop_length=512,num_segments=1):
    
    #dict to store dataa
    data={
        "mapping":[],
        "mfcc":[],
        "labels":[]}
    num_samples_per_segment= int(SAMPLES_PER_TRACK / num_segments)
    expected_num_mfcc_per_segment= math.ceil(num_samples_per_segment / hop_length)
    
    
    #loop through all folders
    for i,(dirpath,dirnames,filenames) in enumerate(os.walk(dataset_path)):
        
        if dirpath is not dataset_path:
            #save mapping
            dirpath_components = dirpath.split("/")
            semantic_label = dirpath_components[-1]
            data["mapping"].append(semantic_label)  
            print("\nProcessing {}".format(semantic_label))
            for f in filenames:
                file_path = os.path.join(dirpath, f) 
                #load audio
                signal,sr = librosa.load(file_path, sr=SAMPLE_RATE)
                
                #extracting mfcc and storing it
                for s in range(num_segments):
                    start_sample = num_samples_per_segment * s
                    finish_sample = start_sample+ num_samples_per_segment
                    mfcc = librosa.feature.mfcc(signal[start_sample:finish_sample],sr=sr,
                                                n_fft=n_fft,
                                                n_mfcc= n_mfcc,
                                                hop_length=hop_length)  
                    mfcc = mfcc.T
                    if len(mfcc) == expected_num_mfcc_per_segment:
                        data["mfcc"].append(mfcc.tolist())
                        data["labels"] .append(i-1)                       
                        print("{} segment:{}".format(file_path, s))
                

    with open(json_path,"w")as fp:
        json.dump(data, fp, indent=4)
        
        
if __name__ == "__main__":
    save_mfcc(DATASET_PATH, JSON_PATH,num_segments=10)






















                          