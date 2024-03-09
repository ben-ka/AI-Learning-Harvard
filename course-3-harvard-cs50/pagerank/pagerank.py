import os
import random
import re
import sys
from time import time

# ----- constants --------------------------------
DAMPING = 0.85
SAMPLES = int(8e6)
MARGIN = 0.0001

## ! The PageRank algorithm

def main():

    # checks if the enough arguments are provided

    if len(sys.argv) < 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])

    # handles the slow sample approach
    
    now = time()
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    time_diff_sampling = time() - now
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    

    # handles the fast iteration approach
    
    now = time()
    ranks = iterate_pagerank(corpus, DAMPING, MARGIN)
    time_diff_iteration = time() - now
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
        

    # printed time taken for each metric
    print(f"Time taken for sampling: {time_diff_sampling:.4f} seconds")
    print(f"Time taken for iteration: {time_diff_iteration:.15f} seconds")

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # creates a dictionary of the pages names as keys and the probabilities of going into that specific page as values (from the page taken as input from the function)
    results = dict()
    
    # loops through every page in the corpus and resets it's value to 0
    for key in corpus:
        results[key] = 0
        if key == page: 
            pass
        # checks if the page has a link to the key that we are looping with
        elif key in corpus[page]:
           results[key] += damping_factor / (len(corpus[page]))

        # adds the damping factor probability to every page
        results[key] += (1 - damping_factor) / (len(corpus))

    return results   

   
def sample_pagerank(corpus : dict, damping_factor : float, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    global Page

    # chooses a random page to start with
    Page = random.choice(list(corpus.keys()))

    
    counterDict = dict() #creates a dictionary that counts the number of times each page has been visited 
    prob_dict = dict()

    for key in corpus:
        counterDict[key] = 0

    for _ in range(n): # loops n time over the process to make n samples of page transitions

        choises = list(corpus.keys())
        
        probabilities = transition_model(corpus, Page, damping_factor) # gets the probability to get to every page from the current page using transition_model
        weights = list(probabilities.values())
        Page = random.choices(population=choises,weights=weights, k = 1) # chooses a page at random with the weight that we got using the transition model
        Page = Page[0]
        counterDict[Page] += 1 # adds 1 to the count of times the bot visited that specific page chosen

    for key, value in counterDict.items(): # normalizes the results to match the sample size
        prob_dict[key] =  counterDict[key] /SAMPLES
    
    return prob_dict
    
def iterate_pagerank(corpus : dict, damping_factor : float, margin : float = 0.001):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    
    start_prob_dict = {} # added a start prob dictionary that gives every page the starting probabilities
    updated_prob_dict = {} # the probability dictionary that constantly changes
    pages_that_link_with_dict = {} # added a new dictionary based on the corpus that gives for each page(key) the pages that link to it
    length = len(list(corpus.keys()))
    gains_from_loop = 0 #how much did the specific page gain from iterating through every page that links to the page
    for page in corpus: # gives start values for every dictionary

        start_prob_dict[page] = 1 / length + (1 - damping_factor) / length
        pages_that_link_with_dict[page] = set()
        updated_prob_dict[page] = 1 / length
    
    

    for page in corpus: #fills the pages_that_link_with_dict dictionary
        for possiblePage in corpus:
            if page in corpus[possiblePage]:
                pages_that_link_with_dict[page].add(possiblePage)

    isGoing = True # a boolean variable that keeps the loop going until the changes done to a page's values is so minute that it doesn't matter to us.
    count = 0

    while isGoing:
        old_prob_dict = updated_prob_dict.copy() #copies the updated dictionary for later use for comparison of the values
        maxChange = 0.0 # a float variable that checks the maximum change through all the pages in the corpus using the old probability dictionary and the updated one

        for page in pages_that_link_with_dict: #a nested loop that iterates over every page in the corpus and for every page iterates over every page that links to it
            for linkedPages in pages_that_link_with_dict[page]:
                gains_from_loop += updated_prob_dict[linkedPages] / len(corpus[linkedPages]) # adds the values of the perspective page's Page rank divided by how many links they have
                
            
            updated_prob_dict[page] = start_prob_dict[page] + damping_factor * gains_from_loop # gains the new updated probability for the page
            maxChange = max(maxChange, abs(updated_prob_dict[page] - old_prob_dict[page])) #checks if the new change of values is larger that all the previous ones

            
                  
            if maxChange <= margin: #stops the while loop in case the maximum change is very small(smaller than the margin given to the function)
                isGoing = False

            gains_from_loop = 0 # resets the variable for the next run of the loop

        count += 1

    
    #checks the sum of the values of the probability dictionary and normalizes it's values
    sum_of_pageranks = sum(updated_prob_dict.values()) 
    if sum_of_pageranks == 0:   
        raise ValueError("There are no ranks")  

    # Normalize the PageRank values
    for page in updated_prob_dict:
        updated_prob_dict[page] /= sum_of_pageranks
    
    print(f"amount of loops:  {count}" )

    return updated_prob_dict



        
    

        

    

     


    
# iterate_pagerank(corpus=crawl(sys.argv[1]), damping_factor= DAMPING)


if __name__ == '__main__':
    main()
