import csv
import itertools
import sys
import random
import pandas as pd

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")

    people = load_data(sys.argv[1])
    probabilities = create_genes_dictionary_for_people(people)

    data = []
    for name, person_info in people.items():
        gene_probs = probabilities[name]['gene']
        trait_probs = probabilities[name]['trait']
        father = person_info['father']
        mother = person_info['mother']
        row = {
            "Name": name,
            "0 Genes": gene_probs[0],
            "1 Gene": gene_probs[1],
            "2 Genes": gene_probs[2],
            "Has trait": trait_probs[True],
            "No trait": trait_probs[False],
            "Father": father,
            "Mother": mother
        }
        data.append(row)

    columns = ["Name", "0 Genes", "1 Gene", "2 Genes", "Has trait", "No trait", "Father", "Mother"]
    df = pd.DataFrame(data, columns=columns)

    last_slash_index = sys.argv[1].rfind("\\")
    if last_slash_index != -1:
        stripped_path = sys.argv[1][last_slash_index + 1:].replace(".csv", "")
    else:
        print("No '/' found in the path.")

    file_path = f"data-results/{stripped_path}-results.xlsx"
    df.to_excel(file_path, index=False)
    



def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people : dict, one_gene: set, two_genes: set, have_trait: set) -> float :
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """


    final_genes_probability_dictionary = create_genes_dictionary_for_people(people)





    cumulative_probability = 1 # final cumulative probability

    for name in have_trait:
        if people[name]["trait"] == True:
            cumulative_probability *= 1
        elif people[name]["trait"] == False:
            return 0.0
        else:
            genes = final_genes_probability_dictionary[name]
            cumulative_probability *= has_trait_based_probabilities(genes)
    
    for name in people:
        if name not in one_gene and name not in two_genes:
            cumulative_probability *= final_genes_probability_dictionary[name][0]
        elif name in one_gene:
            cumulative_probability *= final_genes_probability_dictionary[name][1]
        else:
            cumulative_probability *= final_genes_probability_dictionary[name][2]



    return cumulative_probability




    

def create_genes_dictionary_for_people(people : dict) -> dict:

    full_dictionary = {}
    gene_dictionary = {}

    for name in people:       # looping over all the people with no parents so it will be easier to know the probabilities
        if people[name]['father'] is None:  
            if people[name]['trait'] == True:
                names_dict = bayes_given_trait(True)
                gene_dictionary[name] = names_dict

            elif people[name]['trait'] == False:
                gene_dictionary[name] = bayes_given_trait(False)
            else:
                gene_dictionary[name] = PROBS["gene"]
    

    isGoing = True
    while isGoing:
        isGoing = False
        for name in people: 
            if people[name]['father'] is not None:
                if gene_dictionary[people[name]['father']] and gene_dictionary[people[name]['mother']]:
                    gene_dictionary[name] = calculate_children_gene_probabilities(gene_dictionary[people[name]['father']] , gene_dictionary[people[name]['mother']], people[name]['trait'])
                else:
                    isGoing = True
    for person in gene_dictionary:
        if people[person]['trait'] is None:
            trait_dictionary = create_traits_dictionary(gene_dictionary[person])
            full_dictionary[person] = {"gene": gene_dictionary[person], "trait": trait_dictionary}
        else:
            if people[person]['trait'] == True:
                full_dictionary[person] = {"gene": gene_dictionary[person], "trait" : {True : 1, False : 0}}
            else:
                full_dictionary[person] = {"gene": gene_dictionary[person], "trait" : {True : 0, False : 1}}

    return full_dictionary





def create_traits_dictionary(genes):
    trait_prob = {
        True: 0,
        False : 0
    }
    for i in range(3):
        trait_prob[True] += genes[i] * PROBS["trait"][i][True]
    trait_prob[False] =  1 - trait_prob[True] 

    return trait_prob



def bayes_given_trait(does_have_trait : bool):
       # givens one has a trait checks the probabilities that he has how many genes
    probability_genes_known_trait = {
        0: 0,
        1: 0,
        2: 0       
    }
    
    #using bayes theoram to calculate opposite probability dependency (how likely it is that someone has N genes if they have/ dont have a trait)
    
    probability_of_trait = 0
    for i in range(3):
        probability_of_trait += PROBS["gene"][i] * PROBS["trait"][i][does_have_trait]
        



    for i in range(3):
        bayesProbability = (PROBS["trait"][i][does_have_trait] * PROBS["gene"][i]) / probability_of_trait
        probability_genes_known_trait[i] = bayesProbability

    return probability_genes_known_trait



def calculate_children_gene_probabilities(father_gene : dict, mother_gene : dict, isTrait) -> dict:
    child_genes = {
        0 :0,
        1: 0,
        2 : 0
    }

    prob_not_mutation = 1 - PROBS["mutation"]
# calculates the probability for the child to have 0 genes
    child_genes[0] += father_gene[0] *  prob_not_mutation * mother_gene[0] * prob_not_mutation
    child_genes[0] += father_gene[2] * PROBS["mutation"] * mother_gene[2] * PROBS["mutation"]
    child_genes[0] += 0.5 * father_gene[1] * 0.5 * mother_gene[1]
    child_genes[0] += father_gene[0] * prob_not_mutation * 0.5 * mother_gene[1] + mother_gene[0] * prob_not_mutation * 0.5 * father_gene[1]
    child_genes[0] += 0.5 * father_gene[1] * mother_gene[2] * PROBS["mutation"] + 0.5 * mother_gene[1] * father_gene[2] * PROBS["mutation"]
    child_genes[0] += father_gene[0] * prob_not_mutation * mother_gene[2] * PROBS["mutation"] + mother_gene[0] * prob_not_mutation * father_gene[2] * PROBS["mutation"]



# calculates the probability for the child to have 2 genes
    child_genes[2] += father_gene[2] * prob_not_mutation * mother_gene[2] * prob_not_mutation
    child_genes[2] += father_gene[0] * PROBS["mutation"] * mother_gene[2] * PROBS["mutation"] + mother_gene[0] * PROBS["mutation"] * father_gene[2] * PROBS["mutation"]
    child_genes[2] += mother_gene[2] * prob_not_mutation * 0.5 * father_gene[1] + father_gene[2] * prob_not_mutation * 0.5 * mother_gene[1]
    child_genes[2] += 0.5 * father_gene[1] * 0.5 * mother_gene[1]
    child_genes[2] += father_gene[0] * PROBS["mutation"] * 0.5 * mother_gene[1] + mother_gene[0] * PROBS["mutation"] * 0.5 * father_gene[1] 
    child_genes[2] += father_gene[0] * PROBS["mutation"] * mother_gene[0] * PROBS["mutation"]




    child_genes[1] = 1 - (child_genes[0] + child_genes[2])
    

    # checks the kid's trait and adjust the probabilities accordingly

    if isTrait is not None:
        bayes_probabilities = bayes_given_trait(isTrait)
        total = 0
        for i in range(3):
            total += bayes_probabilities[i] * child_genes[i]
        
        for i in range(3):
            child_genes[i] = (child_genes[i] * bayes_probabilities[i]) / total


    return child_genes



def has_trait_based_probabilities(prob) -> float:
    total = 0
    for i in range(3):
        total += prob[i] * PROBS["trait"][i][True]
    return total

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    raise NotImplementedError


father_gene = {
    0 : 0.5,
    1: 0.3,
    2 : 0.2
}
mother_gene = {
    0 : 0.5,
    1 : 0.3,
    2 : 0.2
}

# print(calculate_children_gene_probabilities(PROBS["gene"],PROBS["gene"]))
# print(calculate_children_gene_probabilities(father_gene, mother_gene))
# print(f"bayes:    {bayes_given_trait(True)}" )
# print(f"bayes:    {bayes_given_trait(False)}" )



if __name__ == "__main__":
    main()
