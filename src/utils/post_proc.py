import csv
import numpy as np
import os
import argparse

def post_processing(val_path, evaluation_file, new_evaluation_file, n_shots=5):
    '''Post processing of a prediction file by removing all events that have shorter duration
    than 60% of the minimum duration of the shots for that audio file.
    
    Parameters
    ----------
    val_path: path to validation set folder containing subfolders with wav audio files and csv annotations
    evaluation_file: .csv file of predictions to be processed
    new_evaluation_file: .csv file to be saved with predictions after post processing
    n_shots: number of available shots
    '''
    dict_duration = {}
    folders = os.listdir(val_path)
    for folder in folders:
        files = os.listdir(val_path+folder)
        for file in files:
            if file[-4:] == '.csv':
                audiofile = file[:-4]+'.wav'
                annotation = file
                events = []
                with open(val_path+folder+'/'+annotation) as csv_file:
                        csv_reader = csv.reader(csv_file, delimiter=',')
                        for row in csv_reader:
                            if row[-1] == 'POS' and len(events) < n_shots:
                                events.append(row)
                min_duration = 10000
                for event in events:
                    if float(event[2])-float(event[1]) < min_duration: # 计算5个shot中，时间最短的一个shot
                        min_duration = float(event[2])-float(event[1])
                dict_duration[audiofile] = min_duration

    results = []
    with open(evaluation_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # skip the headers
        for row in reader:
            results.append(row)

    new_results = [['Audiofilename', 'Starttime', 'Endtime']]
    for event in results:
        audiofile = event[0]
        min_dur = dict_duration[audiofile]
        if float(event[2])-float(event[1]) >= 0.6*min_dur:
            new_results.append(event) #ruo

    with open(new_evaluation_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(new_results)
        
    return
    
if __name__ == "__main__":
    # print(os.getcwd())
    parser = argparse.ArgumentParser()
    parser.add_argument('-val_path', type=str, default="/media/b227/0090ae43-1009-4c49-a645-e82a32b74d82/b227/ygw/Development_set/Dcase2021/Development_Set/Validation_Set/",help='path to validation folder with wav and csv files')
    parser.add_argument('-evaluation_file', type=str,default="DCASE2021Task5-main/src/src/output_csv/tim/Eval_out_tim.csv", help='path and name of prediction file')
    parser.add_argument('-new_evaluation_file', type=str, default="DCASE2021Task5-main/src/src/output_csv/tim/Eval_out_tim_post.csv",help="name of prost processed prediction file to be saved")
    
    args = parser.parse_args()

    post_processing( args.val_path, args.evaluation_file, args.new_evaluation_file)
