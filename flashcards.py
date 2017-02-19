import random
import json


class Flashcards(object):

    def __init__(self, collections={}):
        # Format of collections
        # {'title':{'q':'a', 'q2':'a2'}, 'title2':{...} }
        self.collections = collections
        self.loaded = {}
        self.loaded_titles = []

    # Flashcard file operations
    def readFlashcards(self, filename):
        f = open(filename, 'r')
        self.collections = json.loads(f.read())
        f.close()

    def writeFlashcards(self, filename):
        f = open(filename, 'w')
        f.write(json.dumps(self.collections))
        f.close()
        print('Flashcards saved to file.')

    def createBackup(self): #unused
        print('Flashcards.createBackup not yet coded.')


    # Collection editing
    def addCards(self, title):
        new_cards = {}
        while True:
            q = input('\nPrompt: ')
            a = input('Answer: ')
            if q:
                new_cards[q] = a # implement collision control (or maybe it's a feature: edit cards)
            else:
                if new_cards:
                    self.collections[title] = {**self.collections[title], **new_cards}
                    print('\nFinished adding flashcards to', title, '.')
                    print('Cards added:')
                    print(new_cards)
                break

    def deleteCards(self, title):
        #title = input('Delete cards from: ')
        while True:
            card = input('Delete card: ')
            if card:
                if card in collections[title]:
                    self.collections[title].pop(card)
                else:
                    print(card, 'not in', title, '. Please try again')
            else:
                print('Done deleting cards from', title)

    def newCollection(self, title): 
        try:
            if self.collections[title]: # Prevents collisions
                i = input('\n' + title + ' already exists. Are you sure you want to\noverwrite ' + title + '? (y/n) ')
                if i.lower() == 'y':
                    self.collections[title] = {}
                    print('Add cards to', title)
                    self.addCards(title)
                else:
                    print('Aborted.')
        except KeyError:
            self.collections[title] = {}
            print('Add cards to', title)
            self.addCards(title)

    def mergeCollections(self, title):
        print('Flashcards.mergeCollections not yet coded.')

    def deleteCollection(self, title):
        #print('Current collections: ')
        #print( [i for i in list(self.collections.keys())] )
        #title = input('Delete collection: ')
        r = input('Are you sure you want to delete ' + title + '? (y/n) ')
        if r.lower() == 'y':
            self.collections.pop(title)
            print('Removed', title, 'from collections.')
        else:
            print(title, 'not deleted.')

    
    # Other functions
    def loadCollections(self): 
        print('\nAvailable collections:\n' + '\n'.join(list(flashcards.collections.keys())) + '\n')
        titles = input('Load collections (separated by spaces): ').split()
        if not titles:
            titles = list(self.collections.keys()) # Default to load all collections.
        for title in titles:
            try:
                self.loaded = {**self.loaded, **self.collections[title]}
                self.loaded_titles.append(title)
            except KeyError:
                print('Collection "' + title + '" not recognized; Not loaded.') 

    def viewLoaded(self):
        print('Currently loaded collections:')
        for title in self.loaded_titles:
            print(title)


    # Main functionality
    def quiz(self):
        if not self.loaded:
            self.loadCollections()

        while True:
            q = random.choice(list(self.loaded.keys()))
            ans = input('\n' + q + ': ')
            if ans.casefold() == '#menu':
                print('Exiting quiz and returning to main menu')
                break
            elif  ans == self.loaded[q]:
                print('Correct!')
            else:
                print('Wrong,', self.loaded[q])

    def viewFlashcards(self): # format better
        for q in list(self.loaded.keys()):
            print(q.ljust(15), self.loaded[q].ljust(15))

    def editFlashcardsLoop(self):
        print('\n_______________________________________')
        print('         Now editing flashcards        ')
        print('_______________________________________\n')
        while True:
            print('\n(N)ew collection, (D)elete collection, (M)erge two collections,')
            i = input('(A)dd cards to a collection, (R)emove cards from a collection or (#menu): ').lower()
            edit_switch = {'n': self.newCollection,
                           'd': self.deleteCollection,
                           'm': self.mergeCollections,
                           'a': self.addCards,
                           'r': self.deleteCards}
            if i == '#menu':
                break
            try:
                title = input('Name of collection: ')
                edit_switch[i](title)
            except KeyError:
                print(i, ': Option not recognized.')
                print('Did you want to go the Main #menu?')

            self.writeFlashcards('flashcards.json')

    def viewStats(self):
        print('Flashcards.viewStats not yet coded.')


# --- MAIN LOOP ---
flashcards = Flashcards()
flashcards.readFlashcards('flashcards.json')

while True:
    if not flashcards.loaded:
        print('No flashcards loaded yet.')
        flashcards.loadCollections()

    print('\n_______________________________________')
    print('               Main Menu               ')
    print('_______________________________________')
    print('At any time you can type "#menu" to return to this prompt.')
    
    i = input('(S)tart, (V)iew flashcards, \n(E)dit flashcards, view (P)rogress, (Q)uit: ').lower()
    
    control_switch = {'s': flashcards.quiz,
                      'v': flashcards.viewFlashcards,
                      'e': flashcards.editFlashcardsLoop,
                      'p': flashcards.viewStats}
    if i == 'q':
        print('Goodbye!')
        break
    try:
        control_switch[i]()
    except KeyError:
        print('Command not recognized. Please try again')

# ADD FEATURES
# - create backup file of flashcards.json at beginning of each session
# - implement error resilience
# - timed quizzing
# - history
# - focus on questions that are gotten wrong more often
# - multiple answers to a prompt (i.e {'question':['ans1', 'ans2']})
# - ncurses
# - ordered flashcard list
