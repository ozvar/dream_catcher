import os
import pandas as pd

from datetime import datetime


def collect_inputs():
    # each prompt requests text input on aspect of cognition
    inputs = dict()
    print("Describe the situation:")    
    inputs['situation'] = input()
    print("Describe the automatic thought:")
    inputs['thought'] = input()
    print("Rate your belief in the thought out of 100")
    inputs['thought_belief'] = input()
    print("Describe your emotion(s)")
    inputs['emotions'] = input()
    print("Rate the strength of your emotion(s) out of 100")
    inputs['emotions_strength'] = input()
    print("If possible, label the type of distortion present in this thought")
    inputs['distortion'] = input()
    print("Provide one or more constructive alternatives to this thought")
    inputs['alternatives'] = input()
    print("Describe the outcome of this process")
    inputs['outcome'] = input()

    return inputs


def format_datetime():
    # format current datetime as string: month abbreviation, day, year, hour, then minute
    now = datetime.now()
    dt = now.strftime("%b %d, %Y %H:%M")  

    return dt


def create_df(inputs):
    # format inputs as dataframe
    df = pd.DataFrame({
                "Date & Time": format_datetime(),
                "Situation": inputs['situation'], 
                "Automatic thought": f"{inputs['thought']} - Belief: {inputs['thought_belief']}",
                "Emotion(s)": f"{inputs['emotions']} - Strength: {inputs['emotions_strength']}",
                "Distortion": inputs['distortion'],
                "Alternative thoughts": inputs['alternatives'],
                "Outcome": inputs['outcome']
                },
                index=[0])
    
    return df


def join_records(new_df, record_dir):
    # if one exists, merge new record with existing dataframe
    file_path = os.path.join(record_dir, "record.pickle")
    if os.path.isfile(file_path):
        prev_df = pd.read_pickle(file_path)
        new_df = pd.concat([prev_df, new_df])

    return new_df


def format_save(df, record_dir):
    # output merged records to markdown, and pickle for simple reads in future
    pickle_path = os.path.join(record_dir, "record.pickle")
    md_path = os.path.join(record_dir, "diary.md")
    df.to_pickle(pickle_path)
    md = df.to_markdown(index=False)
    with open(md_path, 'w') as f:
        f.write(md)
        

if __name__ == "__main__":

    dir_path = os.path.dirname(os.path.realpath(__file__))
    inputs = collect_inputs()
    record = create_df(inputs) 
    diary = join_records(new_df=record, record_dir=dir_path)
    format_save(df=diary, record_dir=dir_path)
    print("Records updated")

