import time
import matplotlib.pyplot as plt
import pandas as pd
from uuid import uuid4
import os
import matplotlib
import numpy as np

#Use QtAgg backend to allow fullscreen compatability on all devices
#Requires PyQt6
matplotlib.use("QtAgg")

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]   

questions = [
    "In July there were at least 3 schools with more than 30 absences", 
    "School 5 had more absences than School 2 in January", 
    "In December there were at least 2 schools with less than 10 absences", 
    "School 7 had less absences than School 4 in May", 
    "School 1 had more absences in January than in May", 
    "School 8 had less absences in March than in August",
    "School 3's absences were between 0 and 10 in February", 
    "School 4 had at least 5 months with more than 25 absences", 
    "School 9's absences were between 15 and 25 in December", 
    "In November there were atleast 2 schools with absences between 10 and 20"
]

#stores correct answers worked out at runtime
correct_answers = []

#results of experiment
results = []

chart_types = ["scatter", "heatmap"]
#stores current chart type being used
chart_type = ""

def generate_dataset(trial_num):
    dataset = {}
    for i in range(10):
        dataset[f"School_{i+1}"] = np.random.randint(0, 50, size=12)

    match trial_num + 1:
        #In July there were at least 3 schools with more than 30 absences
        case 1:
            count = 0
            for i in range(10):
                if dataset[f"School_{i+1}"][months.index("Jul")] > 30:
                    count += 1
            correct_answers.append(1 if count >= 3 else 0)
        #School 5 had more absences than School 2 in January
        case 2:
            if dataset["School_5"][months.index("Jan")] > dataset["School_2"][months.index("Jan")]:
                correct_answer = 1
            else:
                correct_answer = 0
            correct_answers.append(correct_answer)
        #In December there were at least 2 schools with less than 10 absences
        case 3:
            count = 0
            for i in range(10):
                if dataset[f"School_{i+1}"][months.index("Dec")] < 10:
                    count += 1
            correct_answers.append(1 if count >= 2 else 0)
        #School 7 had less absences than School 4 in May
        case 4:
            if dataset["School_7"][months.index("May")] < dataset["School_4"][months.index("May")]:
                correct_answer = 1
            else:
                correct_answer = 0
            correct_answers.append(correct_answer)
        #School 1 had more absences in January than in May
        case 5:
            if dataset["School_1"][months.index("Jan")] > dataset["School_1"][months.index("May")]:
                correct_answer = 1
            else:
                correct_answer = 0
            correct_answers.append(correct_answer)
        #School 8 had less absences in March than in August
        case 6:
            if dataset["School_8"][months.index("Mar")] < dataset["School_8"][months.index("Aug")]:
                correct_answer = 1
            else:
                correct_answer = 0
            correct_answers.append(correct_answer)
        #School 3's absences were between 0 and 10 in February
        case 7:
            value = dataset["School_3"][months.index("Feb")]
            if value > 0 and value <= 10:
                correct_answer = 1
            else:
                correct_answer = 0
            correct_answers.append(correct_answer)
        #School 4 had at least 5 months with more than 25 absences 
        case 8:
            count = 0
            for month in dataset["School_5"]:
                if month > 25:
                    count += 1
            correct_answers.append(1 if count >= 5 else 0)
        #School 9's absences were between 15 and 25 in December
        case 9:
            value = dataset["School_9"][months.index("Dec")]
            if value > 15 and value <= 25:
                correct_answer = 1
            else:
                correct_answer = 0
            correct_answers.append(correct_answer)
        #In November there were atleast 2 schools with absences between 10 and 20
        case 10:
            count = 0
            for i in range(10):
                value = dataset[f"School_{i+1}"][months.index("Nov")]
                if value >= 10 and value <= 20:
                    count += 1
            correct_answers.append(1 if count >= 2 else 0)

    return dataset

def add_jitter(values, jitter_amount):
    values = np.asarray(values, dtype=float)
    return values + np.random.uniform(-jitter_amount, jitter_amount, values.shape)

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
    month_positions = np.arange(len(months))

    colors = plt.cm.inferno(np.linspace(0, 1, len(data)))
    markers = ['o', '^', 's']  

    for i, (school, absences) in enumerate(data.items()):
        jittered_months = add_jitter(month_positions, jitter_amount=0.2)
        jittered_absences = add_jitter(absences, jitter_amount=0.1)

        ax.scatter(jittered_months, jittered_absences, marker=markers[i % len(markers)], color=colors[i], alpha=0.5, label=school, edgecolors="black")

    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Absences", fontsize=12)
    ax.set_xticks(month_positions)
    ax.set_xticklabels(months, rotation=90)

    ax.legend(loc='upper left', fontsize='small', bbox_to_anchor=(1, 1))


def display_next_trial(trial_num, chart_type):
    fig, ax = plt.subplots()

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

        if event.key == str(correct_answer):
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
    for chart_num in range(len(chart_types)):
        correct_answers = []
        chart_type = chart_types[chart_num]
        for trial_num in range(10):
            display_next_trial(trial_num, chart_type)

    #UUID for participant anonimity
    fname = f"{uuid4()}.csv"

    while os.path.exists(fname):
        fname = f"{uuid4()}.csv"

    results_df = pd.DataFrame(results)
    results_df.to_csv(fname, index=False)
    print(f"Results saved to {fname}")