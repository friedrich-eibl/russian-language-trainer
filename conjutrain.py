import csv
import random

dict_file = "test_dict.csv"
eval_file = "eval.csv"


def write_csv(data, f_csv):
    with open(f_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def train():
    data = []
    with open(dict_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)

    learned = []
    with open(eval_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            learned.append(row)

    #print(data)

    rounds = 0
    max_rounds = 30
    score = 0

    pronouns = ["я", "ты", "он", "мы", "вы", "они"]
    while rounds < max_rounds:
        if not any('0' in word_learned for word_learned in learned):
            print('nothing left to learn !!!')
            return
        
        rounds+=1

        word_idx = random.randint(0, len(data) - 1)
        word = data[word_idx]
        form = random.randint(1, 6)

        if learned[word_idx][form] == 1:
            rounds -= 1
            continue

        sub = input(f"{word[0]}, {form}:        {pronouns[form-1]} ")

        if sub == word[form].strip():
            score+=1
            learned[word_idx][form] = 1
            write_csv(learned, eval_file)
            print('correct\n')
        else:
            print('nope\n')
            #print(word[form]) ## debug


    print(f"Score:  {score}/{max_rounds}")


train()