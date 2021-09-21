############################################################
# CIS 521: Homework 4
############################################################

student_name = "Sean McGeehan" ## grouped with Luis and Shuai

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import string
import random
import math
############################################################
# Section 1: Markov Models
############################################################

def tokenize(text):
    # first remove the left and right spaces
    text.strip()
    # based on the string.punctuation module to split the string
    separatedPunctuation = ""
    for character in text:
        if character in string.punctuation:
            outputCharacter = " %s " % character
        else:
            outputCharacter = character

        separatedPunctuation += outputCharacter

    return separatedPunctuation.split()


def ngrams(n, tokens):
    if n == 1: # if n is 1
        return_list = list()
        for i in tokens:
            return_list.append(((), i)) # append the tuple with the element at the index
            # as well as blank tuple
       
        return_list.append(((), '<END>')) # if the index is the n-1, then we append the <end> tag
        return return_list
   
    elif n > 1:
        return_list = list()
        index = 0
        for i in tokens:
            if index == 0: # if the index is the first
                start_string = '<START> '* (n - 1)
                return_list.append((tuple(start_string.split()), tokens[index]))
            elif index != 0 and index - (n - 1) < 0: # if the index is not the first one but we have to append the start tag
                diff = index - (n - 1)
                start_string = '<START> '* abs(diff)
                start_str = start_string.split()
                return_list.append((tuple(start_str + tokens[:index]), tokens[index]))
            else:
                return_list.append((tuple(tokens[index - (n-1): index]), tokens[index]))
           
            index += 1
        return_list.append((tuple(tokens[index - (n-1): index]), '<END>')) # we have to append the end tag at the last element
       
        return return_list


class NgramModel(object):

    def __init__(self, n):
        self.order = n
        self.count_dict = dict()
        self.context_dict = dict()
        return

    def update(self, sentence):
        for context, token in ngrams(self.order, tokenize(sentence)):
            if context in self.count_dict: # count the context appearance
                self.count_dict[context] += 1
            else:
                self.count_dict[context] = 1

            if context in self.context_dict: # count the token associated with the context appearance
                token_dict = self.context_dict[context]
                if token in token_dict:
                    token_dict[token] += 1
                else:
                    token_dict[token] = 1

            else:
                self.context_dict[context] = {token: 1}

        return

    def prob(self, context, token): # divide the token with the total # of context
        if context in self.context_dict and token in self.context_dict[context]:
            token_dict = self.context_dict[context]
            return (token_dict[token]) / self.count_dict[context]
        else:
            return 0 # if not appear in one of the dictionary, return 0
         
    def random_token(self, context):
        r = random.random()
        if context in self.context_dict:
            token_dict = self.context_dict[context]
            sorted_tokens = sorted(token_dict.keys())
       
            for idx, token in enumerate(sorted_tokens):
                sum_tokens_without_i = sum([self.prob(context, sorted_token) for sorted_token in sorted_tokens[:idx]])
                sum_tokens_with_i = sum_tokens_without_i + self.prob(context, token)
                if sum_tokens_without_i <= r and r < sum_tokens_with_i:
                    return token
           
        else:
            return None
           
    def random_text(self, token_count):
        list = ["<START>" for i in range(self.order-1)]
        returnList = []
        
        for i in range(token_count):
            if self.order == 1:
                returnList.append(self.random_token(()))
            else:
                x = str(self.random_token(tuple(list[(self.order-1)*-1:])))
                list.append(x)
                returnList.append(x)
                if x == "<END>":
                    list = ["<START>" for i in range(self.order-1)]
            

        space = " "
        return space.join(returnList)
        #return space.join(list[self.order-1:])

    def perplexity(self, sentence):
        tok = tokenize(sentence)
        retlist = ngrams(self.order ,tok)
        log_sum = 0.0
        prob = 1.0

        for (context, token) in retlist:
            newprob = self.prob(context, token)
            ##log_sum += 1.0*math.log(self.prob(context, token),len(tok))
            prob = prob * newprob

        return 1/prob ** (1./ (len(tok)+1))


def create_ngram_model(n, path):
    ngram_model = NgramModel(n)

    with open(path, 'r') as f:
        for line in f:
            ngram_model.update(line)

    return ngram_model

m = NgramModel(1)
m.update("a b c d")
m.update("a b a b")
random.seed(1)
random.seed(1)
m.random_token(())  
#print(m.random_text(13) ) 
m = NgramModel(2)
m.update("a b c d")
m.update("a b a b")
random.seed(2)

m = NgramModel(1)
m.update("a b c d")
m.update("a b a b")
#print(m.perplexity("a b"))
#print(m.random_text(15))
#for i in range(25)]
#['<END>', 'c', 'b', 'a', 'a', 'a', 'b', 'b', '<END>', '<END>', 'c', 'a', 'b', '<END>', 'a', 'b', 'a', 'd', 'd', '<END>', '<END>', 'b', 'd', 'a', 'a']



m  = create_ngram_model(3, "Hunter.txt")

print(m.random_text(1000)[0:])

