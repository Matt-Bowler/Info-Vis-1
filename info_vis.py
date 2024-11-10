import time
import matplotlib.pyplot as plt
import pandas as pd
from uuid import uuid4
import os
import matplotlib

#Use QtAgg backend to allow fullscreen compatability on all devices
#Requires PyQt6
matplotlib.use("QtAgg")

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]   

#replace with our own datasets
datasets_heatmap = [
    {
        'School_1': [5, 12, 7, 8, 15, 10, 9, 18, 7, 6, 11, 12],
        'School_2': [8, 13, 15, 10, 5, 11, 16, 9, 17, 14, 10, 13],
        'School_3': [14, 7, 10, 15, 8, 12, 6, 5, 30, 20, 9, 10],  
        'School_4': [12, 14, 10, 11, 9, 8, 10, 15, 13, 12, 25, 17],
        'School_5': [5, 12, 7, 8, 30, 10, 9, 18, 7, 6, 11, 12],  
        'School_6': [8, 13, 15, 10, 15, 11, 16, 9, 17, 14, 10, 13],
        'School_7': [14, 7, 10, 15, 8, 12, 6, 5, 18, 20, 9, 10],
        'School_8': [5, 12, 7, 8, 15, 10, 30, 18, 7, 6, 11, 12],  
        'School_9': [8, 13, 15, 10, 5, 11, 16, 9, 17, 14, 10, 13],
        'School_10': [14, 7, 10, 15, 8, 12, 6, 5, 18, 20, 25, 28] 
    }
]

datasets_scatterplot = [
    {
        'School_1': [5, 12, 7, 8, 15, 10, 9, 18, 7, 6, 11, 12],
        'School_2': [8, 13, 15, 10, 5, 11, 16, 9, 17, 14, 10, 13],
        'School_3': [14, 7, 10, 15, 8, 12, 6, 5, 30, 20, 9, 10],  
        'School_4': [12, 14, 10, 11, 9, 8, 10, 15, 13, 12, 25, 17],
        'School_5': [5, 12, 7, 8, 30, 10, 9, 18, 7, 6, 11, 12],  
        'School_6': [8, 13, 15, 10, 15, 11, 16, 9, 17, 14, 10, 13],
        'School_7': [14, 7, 10, 15, 8, 12, 6, 5, 18, 20, 9, 10],
        'School_8': [5, 12, 7, 8, 15, 10, 30, 18, 7, 6, 11, 12],  
        'School_9': [8, 13, 15, 10, 5, 11, 16, 9, 17, 14, 10, 13],
        'School_10': [14, 7, 10, 15, 8, 12, 6, 5, 18, 20, 25, 28] 
    }
]

#replace with our Questions
questions = ["Question 1", "Question 2", "Question 3", "Question 4", "Question 5", "Question 6","Question 7", "Question 8", "Question 9", "Question 10"]
correct_answers = ["1", "2", "1", "2", "2", "2", "1", "1", "2", "1"]


#results of experiment
results = []

def plot_heatmap(data, ax):
    schools = list(data.keys())
    absences = [data[school] for school in schools]
    heatmap = ax.imshow(absences, aspect='auto', cmap='viridis')
    ax.set_title("Chart 1")
    ax.set_xticks(range(12))
    ax.set_xticklabels(months, rotation=90)
    ax.set_yticks(range(10))
    ax.set_yticklabels(schools)
    plt.colorbar(heatmap, ax=ax, orientation='vertical')

def plot_scatterplot(data, ax):
    ax.set_title("Chart 2")
    for school, absences in data.items():
        ax.plot(months, absences, marker='o', label=school)
    ax.set_xlabel("Month")
    ax.set_ylabel("Absences")

    plt.xticks(rotation=90)

    ax.legend(loc='upper left', fontsize='small', bbox_to_anchor=(1, 1))



def display_next_trial(trial_num):
    fig, (ax1, ax2) = plt.subplots(1,2)

    #relace 0 with trial num
    plot_heatmap(datasets_heatmap[0], ax1)
    plot_scatterplot(datasets_scatterplot[0], ax2)

    plt.suptitle(questions[trial_num], fontsize=14)
    fig.text(0.5, 0.95, "Press 1 or 2 on your keyboard to answer which chart below answers the above question", ha='center', va='center', fontsize=10)

    manager = plt.get_current_fig_manager() 
    manager.full_screen_toggle()

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1) 

    start_time = time.time()

    fig.canvas.mpl_connect("key_press_event", lambda event: on_key_press(event, trial_num, start_time))
    plt.show(block=True)

def on_key_press(event, trial_num, start_time):
    if event.key in ["1", "2"]:
        response_time = time.time() - start_time
        correct_answer = correct_answers[trial_num]
        is_correct = 0

        if event.key == correct_answer:
            is_correct = 1

        results.append({
            "Trial Number": trial_num + 1,
            "Question": questions[trial_num],
            "Correct Answer": correct_answer,
            "Participant Response": event.key.upper(),
            "Accuracy": is_correct,
            "Response Time (seconds)": response_time
        })
        plt.close()


if __name__ == "__main__":
    for trial_num in range(0, 10):
        display_next_trial(trial_num)

    #UUID for participant anonimity
    fname = f"{uuid4()}.csv"

    while os.path.exists(fname):
        fname = f"{uuid4()}.csv"

    results_df = pd.DataFrame(results)
    results_df.to_csv(fname, index=False)
    print(f"Results saved to {fname}")