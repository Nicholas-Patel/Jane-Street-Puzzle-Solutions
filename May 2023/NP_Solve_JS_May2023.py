#####################################
### Jane Street Puzzle [May 2023] ###
#####################################
# Nicholas Patel

# Find scrabble score of word
def scrabble_score(s):
    res = 0
    letters = [set("aeioulnstr"), set("dg"), set("bcmp"), set("fhvwy"), set("k"), set("jx"), set("qz")]
    vals = [1, 2, 3, 4, 5, 8, 10]
    for c in s:
        for i in range(len(letters)):
            if c in letters[i]:
                res += vals[i]
    return res

# Convert a list of binary strings to a list of letters
def find_words(l):
    result = []
    reference = ord("a") - 1
    for c in l:
        num = int(c, base=2)
        reference = ord('a')-1
        letter = chr(num%26 + reference)
        result.append(letter)
    print(result)

# First processing on solely the words matched (manual)
part1 = ["10011", "00011", "10010", "00001", "00010"]
part2 = ["00010", "01100", "00101", "10011", "10101"]
part3 = ["01101", "01111", "00100", "00100", "00000"]
combined = part1 + part2 + part3
find_words(combined)

# Hard-code words
words = [["polo", "england", "skyscraper", "dress", "tuxedo"], 
         ["agent", "compound", "deck", "shoe", "shorts"],
         ["boot", "plane", "school", "cap", "texas"],
         ["bomb", "dash", "telescope", "tin", "glove"],
         ["kiss", "governer", "sherlock", "suit", "sun"],
         ["space", "mill", "circle", "duck", "powder"],
         ["fever", "scorpion", "octopus", "silk", "war"],
         ["hotel", "foam", "cuckoo", "sheet", "penguin"],
         ["rabbit", "mud", "glasses", "shark", "dog"], 
         ["turtle", "cloak", "reindeer", "ice", "eagle"],
         ["bank", "soup", "cheese", "well", "potato"],
         ["magazine", "pie", "salad", "carrot", "pizza"],
         ["army", "paddle", "hamburger", "himalayas", "country"],
         ["cycle", "bride", "biscuit", "pacific", "lab"],
         ["ash", "kid", "queen", "novel", "jet"]]

# Second processing: create binary strings from words with odd scores
res = [[0 for _ in range(len(words[0]))] for _ in range(len(words))]
for i in range(len(words)):
    for j in range(len(words[0])):
        res[i][j] = str(scrabble_score(words[i][j]) % 2)
res = [''.join(row) for row in res]
find_words(res)

# Third processing: create binary strings from words with length > 5
res = [[0 for _ in range(len(words[0]))] for _ in range(len(words))]
for i in range(len(words)):
    for j in range(len(words[0])):
        res[i][j] = str(1 * (len(words[i][j]) > 5))
res = [''.join(row) for row in res]
find_words(res)

# Fourth processing: create binary strings from words with middle letter o or f
res = [[0 for _ in range(len(words[0]))] for _ in range(len(words))]
for i in range(len(words)):
    for j in range(len(words[0])):
        n = len(words[i][j])
        if n % 2 == 1 and words[i][j][n//2] in set("of"):
            res[i][j] = "1"
        else:
            res[i][j] = "0"
res = [''.join(row) for row in res]
find_words(res)

# Fifth processing: get middle letters of all words with len>5 and odd score
res = []
for i in range(len(words)):
    for j in range(len(words[0])):
            n = len(words[i][j])
            if n%2 and scrabble_score(words[i][j]) % 2 and n > 5:
                print(words[i][j])
                res.append(words[i][j][n//2])
print(res)

# Sixth processing: middle letters of code words
res = []
combined = [list(row) for row in combined]
for i in range(len(combined)):
    for j in range(len(combined[0])):
        used = combined[i][j]
        w = words[i][j]
        n = len(w)
        if used == "1" and n % 2:
            res.append(w[n//2])
print(res)


