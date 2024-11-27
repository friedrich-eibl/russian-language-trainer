import csv
import random

dict_file = "test_dict.csv"
data = []
with open(dict_file, mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(row)



#print(data)

rounds = 0
max_rounds = 30
score = 0

pronouns = ["я", "ты", "он", "мы", "вы", "они"]
while rounds < max_rounds:
    rounds+=1

    word = random.choice(data)
    form = random.randint(1, 6)

    sub = input(f"{word[0]}, {form}:        {pronouns[form-1]} ")

    if sub == word[form].strip():
        score+=1
        print('correct\n')
    else:
        print('nope\n')
        #print(word[form]) ## debug


print(f"Score:  {score}/{max_rounds}")
