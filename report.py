# The report has 4 parts
# 1. [DONE] Number of unique pages
# 2. [TODO] Number of words of the longest page
# 3. [DONE] 50 most common words
# 4. [TODO] Number of subdomains in ics.uci.edu domain? List subdomains ordered alphabetically and number of unique pages in each subdomain. lines containing URL, number (http://vision.ics.uci.edu, 10

# -----------------------------------------
# --------------- Part 1 ------------------
# ---------Number of unique pages----------
# -----------------------------------------
with open("url.txt", encoding="utf8") as file:
    url_count = 0
    for line in file:
        url_count += 1
    print('-------------------------------------')
    print('Part 1. Number of unique URLs =', url_count)
    print('-------------------------------------')



# -----------------------------------------
# --------------- Part 2 ------------------
# ---Number of words of the longest page---
# -----------------------------------------
with open("longestpage.txt", encoding="utf8") as file:
    print('-------------------------------------')
    print('Part 2. Number of words of the longest page =', file.readline())
    print('Link =', file.readline())
    print('-------------------------------------')


# -----------------------------------------
# --------------- Part 3 ------------------
# ---------Top 50 common words-------------
# -----------------------------------------

print('-------------------------------------')
print('Part 3. Top 50 Common Words')
print('-------------------------------------')

# Variables
stop_words = set()  # List of words to not count
word_freq = dict()  # Map to count occurrences of each word

# Create stop_words set
with open("stop_words.txt", encoding="utf8") as file:
    for line in file:
        stop_words.add(line.rstrip('\n'))

# Parse content.txt and create the word_freq map
with open("content.txt", encoding="utf8") as file:
    for line in file:
        for word in line.split(' '):
            if word in stop_words:      # Skip if it's a stop word
                continue
            elif word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1

# Print the top 50 words sorted from highest to lowest
i = 1
for token, count in sorted(word_freq.items(), key=lambda x: x[1], reverse=True):
    if i > 50:
        break
    print(f'{i}.', token, '=>', count)
    i += 1



# -----------------------------------------
# --------------- Part 4 ------------------
# ------------List of subdomains-----------
# -----------------------------------------
print('-------------------------------------')
print('Part 4. List of subdomains')
print('-------------------------------------')

#with open("url.txt", encoding="utf8") as file:
#    for line in file:
