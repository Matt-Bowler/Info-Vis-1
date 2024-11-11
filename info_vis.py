import time
import matplotlib.pyplot as plt
import pandas as pd
from uuid import uuid4
import os
import matplotlib
import sys
import random
import numpy as np

#Use QtAgg backend to allow fullscreen compatability on all devices
#Requires PyQt6
matplotlib.use("QtAgg")

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]   

#replace with our Questions
#e.g. in july there were 3 schools with more than 15 absences
questions = [
    "Question 1", 
    "Question 2", 
    "Question 3", 
    "Question 4", 
    "Question 5", 
    "Question 6",
    "Question 7", 
    "Question 8", 
    "Question 9", 
    "Question 10"
]

#stores correct answers worked out at runtime
correct_answers = []


#results of experiment
results = []
#chart type used for experiment
chart_type = ""

def generate_dataset(trial_num):
    dataset = {}
    for i in range(10):
        dataset[f"School_{i+1}"] = np.random.randint(0, 30, size=12)

    match trial_num:
        #TODO: Depending on question (trial num) workout correct answer for random dataset generated above and append to correct_answers
        case 1:
            print("")
    return dataset

def plot_heatmap(data, ax):
    schools = list(data.keys())
    absences = [data[school] for school in schools]
    heatmap = ax.imshow(absences, aspect='auto', cmap='viridis')
    ax.set_xticks(range(12))
    ax.set_xticklabels(months, rotation=90)
    ax.set_yticks(range(10))
    ax.set_yticklabels(schools)
    ax.set_xlabel("Month")
    ax.set_ylabel("School")

    plt.colorbar(heatmap, ax=ax, orientation='vertical').set_label("Absences", rotation=270, labelpad = 15)

def plot_scatterplot(data, ax):
    for school, absences in data.items():
        ax.scatter(months, absences, marker='o', label=school)
    ax.set_xlabel("Month")
    ax.set_ylabel("Absences")

    plt.xticks(rotation=90)

    ax.legend(loc='upper left', fontsize='small', bbox_to_anchor=(1, 1))



def display_next_trial(trial_num, chart_type):
    #change to 1 graph per trial
    fig, ax = plt.subplots()

    #relace 0 with trial num
    if chart_type == "scatter":
        plot_scatterplot(generate_dataset(trial_num), ax)
    elif chart_type == "heatmap":
        plot_heatmap(generate_dataset(trial_num), ax)
    else: 
        raise ValueError("Invalid chart type")


    plt.suptitle(questions[trial_num], fontsize=14)
    fig.text(0.5, 0.92, "True or false press either 1 or 0 on your keyboard (1 = True, 0 = False)", ha='center', va='center', fontsize=10)

    manager = plt.get_current_fig_manager() 
    manager.full_screen_toggle()

    start_time = time.time()

    fig.canvas.mpl_connect("key_press_event", lambda event: on_key_press(event, trial_num, start_time))
    plt.show(block=True)

def on_key_press(event, trial_num, start_time):
    if event.key in ["1", "0"]:
        response_time = time.time() - start_time
        correct_answer = correct_answers[trial_num]
        is_correct = 0

        if event.key == correct_answer:
            is_correct = 1

        results.append({
            "Trial Number": trial_num + 1,
            "Chart Type": chart_type.capitalize(),
            "Question": questions[trial_num],
            "Correct Answer": correct_answer,
            "Participant Response": event.key.upper(),
            "Accuracy": is_correct,
            "Response Time (seconds)": response_time
        })
        plt.close()


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: python info_vis.py <scatter/heatmap>")
        exit(-1)
    
    if sys.argv[1].lower() == "scatter":
        chart_type = "scatter"
    elif sys.argv[1].lower() == "heatmap":
        chart_type = "heatmap"
    else:
        print("Usage: python info_vis.py <scatter/heatmap>")
        exit(-1)

    for trial_num in range(0, 10):
        display_next_trial(trial_num, chart_type)

    #UUID for participant anonimity
    fname = f"{uuid4()}.csv"

    while os.path.exists(fname):
        fname = f"{uuid4()}.csv"

    results_df = pd.DataFrame(results)
    results_df.to_csv(fname, index=False)
    print(f"Results saved to {fname}")