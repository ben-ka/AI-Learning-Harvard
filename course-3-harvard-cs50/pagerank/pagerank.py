import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10_000_000
MARGIN = 0.0001


def main():
    for arg in sys.argv:
        print(arg)
    if len(sys.argv) < 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


    ranks = iterate_pagerank(corpus, DAMPING, MARGIN)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")




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
    results = dict()
    
    for key in corpus:
        results[key] = 0
        if key == page:
            pass
        elif key in corpus[page]:
           results[key] += damping_factor / (len(corpus[page]))

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
    Page = random.choice(list(corpus.keys()))
    counterDict = dict()
    prob_dict = dict()
    for key in corpus:
        counterDict[key] = 0

    for _ in range(n):
        choises = list(corpus.keys())
        
        probabilities = transition_model(corpus, Page, damping_factor)
        weights = list(probabilities.values())
        Page = random.choices(population=choises,weights=weights, k = 1)
        Page = Page[0]
        counterDict[Page] += 1

    for key, value in counterDict.items():
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
    
    
    start_prob_dict = {}
    updated_prob_dict = {}
    pages_that_link_with_dict = {}
    length = len(list(corpus.keys()))
    gains_from_loop = 0
    for page in corpus:

        start_prob_dict[page] = 1 / length + (1 - damping_factor) / length
        pages_that_link_with_dict[page] = set()
        updated_prob_dict[page] = 1 / length
    
    isGoing = True

    for page in corpus:
        for possiblePage in corpus:
            if page in corpus[possiblePage]:
                pages_that_link_with_dict[page].add(possiblePage)
    count = 0
    while isGoing:
        old_prob_dict = updated_prob_dict.copy()
        maxChange = 0.0
        for page in pages_that_link_with_dict:
            for linkedPages in pages_that_link_with_dict[page]:
                gains_from_loop += updated_prob_dict[linkedPages] / len(corpus[linkedPages])
                
            # sum_of_pageranks = sum(updated_prob_dict.values())
            updated_prob_dict[page] = start_prob_dict[page] + damping_factor * gains_from_loop
            maxChange = max(maxChange, abs(updated_prob_dict[page] - old_prob_dict[page]))

            # if (count == 6000):
                
            #     isGoing = False
                  
            if maxChange <= margin:
                isGoing = False

            gains_from_loop = 0
            count += 1

 
    sum_of_pageranks = sum(updated_prob_dict.values())

    if sum_of_pageranks == 0:   
        raise NotImplementedError  

    # Normalize the PageRank values
    for page in updated_prob_dict:
        updated_prob_dict[page] /= sum_of_pageranks

    return updated_prob_dict



        
    

        

    

     


    
# iterate_pagerank(corpus=crawl(sys.argv[1]), damping_factor= DAMPING)



main()
