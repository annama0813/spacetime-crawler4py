stop_words = set()
with open("stop_words.txt", encoding="utf8") as file:
    for line in file:
        stop_words.add(line.rstrip('\n'))
print(stop_words)