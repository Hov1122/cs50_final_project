import random
import sqlite3

sentences = open("sentences.txt", "r")
text = sentences.readlines()

# Remove new line symbols
for i in range(len(text)):
    text[i] = text[i].replace('\n', '')

sentences.close()

conn2 = sqlite3.connect('texts.db', check_same_thread=False)

cursor2 = conn2.cursor()

choice = random.randint(0, len(text) - 1)
some_text = text

old_text = cursor2.execute("SELECT text FROM dbt")
old_text = [item for t in old_text for item in t]

for i in range(len(some_text)): 
    if some_text[i] not in old_text:
        data = [str(some_text[i])]
        cursor2.execute("INSERT INTO dbt(text) VALUES(?);", 
                            data)
        conn2.commit()

t_grade = cursor2.execute("SELECT text, text_id FROM dbt")
t_grade = dict(t_grade)

# Add only those texts which isnt in db yet
easy_id = cursor2.execute("SELECT easy_id FROM easy")
easy_id = [item for t in easy_id for item in t]
medium_id = cursor2.execute("SELECT medium_id FROM intermediate")
medium_id = [item for t in medium_id for item in t]
hard_id = cursor2.execute("SELECT hard_id FROM advanced")
hard_id = [item for t in hard_id for item in t]  

for key in t_grade:
    
    letter = sentence = 0
    word = 1
    for i in key:
        if i.isalpha():
            letter += 1
        elif i == " ":
            word += 1
        elif i in ['?', '.', '!']:
            sentence += 1
    index = round(5.88 * letter / word - 29.6 * sentence / word - 15.8)
    if index <= 4 and t_grade[key] not in easy_id:
        cursor2.execute("INSERT INTO easy VALUES(?);", 
                            [t_grade[key]])
        conn2.commit()
    if (index > 4 and index <= 7) and t_grade[key] not in medium_id:
        cursor2.execute("INSERT INTO intermediate VALUES(?);", 
                            [t_grade[key]])
        conn2.commit()
    if index > 7 and t_grade[key] not in hard_id:
        cursor2.execute("INSERT INTO advanced VALUES(?);", 
                            [t_grade[key]])
        conn2.commit()
conn2.close()