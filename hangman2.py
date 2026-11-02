word=input('enter a word :').lower()
top=[' ']*len(word)
middle=['-']*len(word)
bottom=[' ']*len(word)

chance=2
wrong=0
def hangman(top, middle, bottom):
    for i in range(len(top)):
        print(top[i],end=' ')
    print()
    for i in range(len(middle)):
        print(middle[i],end=' ')
    print()
    for i in range(len(bottom)):
        print(bottom[i],end=' ')
    print()

while True:
    hangman(top, middle, bottom)
    guess=input('enter a char :').lower()
    if len(guess) == len(word):
        if guess == word:
            print('you win!!')
            break
        else:
            chance =chance - 1
            print('word wrong!!')
            if chance == 0:
                print('you lose!!')
                print('the word was :',word)
                break
    elif len(guess) == 1:
        flag=False
        for i in range(len(word)):
            if word[i] == guess:
                top[i] = guess
                flag = True
        if flag == False:
            bottom[wrong] = guess
            wrong =wrong + 1
        if wrong == len(word):
            print('you lose!!')
            print('the word was :',word)
            break
        elif top == list(word):
            print('you win!!')
            break
        








        
        
        
                















            














                






                
            
        
