import random as rnd
import itertools

class SakClass:
    def __init__(self):
        self.letters = {
            "number_of_letters":102,
            "Α": [1, 12],
            "Β": [8, 1],
            "Γ": [4, 2],
            "Δ": [4, 2],
            "Ε": [1, 8],
            "Ζ": [10, 1],
            "Η": [1, 7],
            "Θ": [10, 1],
            "Ι": [1, 8],
            "Κ": [2, 4],
            "Λ": [3, 3],
            "Μ": [3, 3],
            "Ν": [1, 6],
            "Ξ": [10, 1],
            "Ο": [1, 9],
            "Π": [2, 4],
            "Ρ": [2, 5],
            "Σ": [1, 7],
            "Τ": [1, 8],
            "Υ": [2, 4],
            "Φ": [8, 1],
            "Χ": [8, 1],
            "Ψ": [10, 1],
            "Ω": [3, 3],
        }
        
        self.greek_alphabet = (
            "Α", "Β", "Γ", "Δ", "Ε", "Ζ", "Η", "Θ", "Ι", "Κ", "Λ", "Μ",
            "Ν", "Ξ", "Ο", "Π", "Ρ", "Σ", "Τ", "Υ", "Φ", "Χ", "Ψ", "Ω"
        )
        
    
    def __repr__(self):
        return 'Sak instance'
    
    def check_letter(self, letter):
        if self.letters[letter][1]>0:
            return True
        else:
            return False
    
    def reduce_letter(self, letter):
        if self.check_letter(letter)==True:
            self.letters[letter][1]=self.letters[letter][1]-1
            self.letters["number_of_letters"]=self.letters["number_of_letters"]-1
            
    def increase_letter(self, letter):
        self.letters[letter][1]=self.letters[letter][1]+1
        self.letters["number_of_letters"]=self.letters["number_of_letters"]+1
            
    def getletters(self, N):
        my_list=[]
        counter=0
        if N > self.letters["number_of_letters"]:
            N = self.letters["number_of_letters"]
        while counter<N:
            num = rnd.randint(0, len(self.greek_alphabet)-1)
            letter = self.greek_alphabet[num]
            if self.check_letter(letter)==True:
                my_list.append(letter)
                self.reduce_letter(letter)
                counter=counter+1
            
        return my_list
    
    def putbackletters(self, a_list):
        for letter in a_list:
            self.increase_letter(letter)
            
    def calculate(self, word):
        my_sum=0
        for letter in word:
            my_sum = my_sum + self.letters[letter][0]
        return my_sum
    
    def is_empty(self):
        if self.letters["number_of_letters"]==0:
            return True
        return False

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.hand = []
        
    def __repr__(self):
        return 'Player instance'
    
#     def start_message(self, sak):
#         print("---------------------------------------------")
#         print("Στο σακουλάκι: ", end =" ")
#         print(str(sak.letters["number_of_letters"]), end =" ")
#         print(" γράμματα - Παίζεις:", end =" ")
#         print(self.name + " - Score: " + str(self.score))
#         print("Γραμματα: ", end =" ")
#         print(self.hand)
        
    def end_message(self, sak):
        print("Στο σακουλάκι: ", end =" ")
        print(str(sak.letters["number_of_letters"]), end =" ")
        print(" γράμματα.", end =" ")
        print(self.name + " - Score: " + str(self.score))
        print("Γραμματα: ", end =" ")
        print(self.hand)
        print("---------------------------------------------")
        
    def promted_play(play):
        def inner(self, sak, words):
            print("---------------------------------------------")
            print("Στο σακουλάκι: ", end =" ")
            print(str(sak.letters["number_of_letters"]), end =" ")
            print(" γράμματα - Παίζεις:", end =" ")
            print(self.name + " - Score: " + str(self.score))
            print("Γραμματα: ", end =" ")
            print(self.hand)
            return play(self, sak, words)
            
        return inner
    
class Human(Player):
    def __repr__(self):
        return 'Human instance'
    
    @staticmethod
    def check_hand(temp_answer, temp_hand):
        for letter in temp_answer:
            if letter in temp_hand:
                temp_hand.remove(letter)
            else:
                return False
        return True
    
    @Player.promted_play
    def play(self, sak, words):
        answer = input().upper()
        # 'p' means change hand
        if answer=='P':
            n = len(self.hand)
            temp = sak.getletters(n)
            if len(temp) != n:
                return "end"
            sak.putbackletters(self.hand)
            self.hand = temp
            self.end_message(sak)
            return True
        if answer=='Q':
            return "end"

        temp_answer = '' + answer
        temp_hand = self.hand.copy()

        if Human.check_hand(temp_answer, temp_hand):
            if answer in words:
                print(words[answer])
                self.score = self.score + words[answer]

                self.hand = self.hand + sak.getletters(len(answer))
                for letter in answer:
                    self.hand.remove(letter)
                self.end_message(sak)
                return True
            else:
                print("Δεν υπάρχει αυτή η λέξη!")      
        else:
            print("Δεν έχεις τα γράμματα για αυτήν την λέξη!")
        
class Computer(Player):
    def __repr__(self):
        return 'Computer instance'
    
    def set_mode(self, mode):
        self.mode = mode
        
    @Player.promted_play
    def play(self, sak, words):
        answer = self.mode(self.hand, words)
        if answer == False:
            n = len(self.hand)
            temp = sak.getletters(n)
            if len(temp) != n:
                return "end"
            sak.putbackletters(self.hand)
            self.hand = temp
        else:
            print(answer, end=" ")
            print(words[answer])
            self.score = self.score + words[answer]

            self.hand = self.hand + sak.getletters(len(answer))
            for letter in answer:
                self.hand.remove(letter)
            self.end_message(sak)
        return True
            
    @staticmethod        
    def min_letters(hand, words): 
        # finds all possible combinations of letters
        perms = []
        for x in range(2, 8):
            perms.append(list(itertools.permutations(hand, x)))
        for word in perms:
            for word2 in word:
                string = ''.join(word2)
                if string in words:
                    return string
        return False
    
    @staticmethod
    def max_letters(hand, words): 
        # finds all possible combinations of letters
        perms = []
        for x in range(7, 1, -1):
            perms.append(list(itertools.permutations(hand, x)))
        for word in perms:
            for word2 in word:
                string = ''.join(word2)
                if string in words:
                    return string
        return False
    
    @staticmethod
    def smart(hand, words):
        my_dict = {}
        # finds all possible combinations of letters
        perms = []
        for x in range(7, 1, -1):
            perms.append(list(itertools.permutations(hand, x)))
        for word in perms:
            for word2 in word:
                string = ''.join(word2)
                if string in words:
                    my_dict[string] = words[string]
        if my_dict:
            max_value = max(my_dict.values())
            max_keys = [k for k, v in my_dict.items() if v == max_value]
            return max_keys[0]
        else:
            return False