from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")
playerASentence = Symbol("Player's A sentence truth")


BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")
playerBSentence = Symbol("Player's B sentence truth")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")
playerCSentence = Symbol("Player's C sentence truth")


KNOWLEDGE_BASE = And(
    Or(AKnave, AKnight),
    Or(Not(AKnight),Not(AKnave)),
    Biconditional(AKnave, Not(playerASentence)),
    Biconditional(AKnight, playerASentence),

    Or(BKnave, BKnight),
    Or(Not(BKnight),Not(BKnave)),
    Biconditional(BKnave, Not(playerBSentence)),
    Biconditional(BKnight, playerBSentence),


    Or(CKnave, CKnight),
    Or(Not(CKnight),Not(CKnave)),
    Biconditional(CKnave, Not(playerCSentence)),
    Biconditional(CKnight, playerCSentence),
    
)


def checkQuery(knowledge, query):

    return model_check(knowledge, query)


def AddToKnowledge(truth: bool, knowledge: And, sentence: Symbol, query: Optional[Symbol] = None) -> None:
    """
    Update the knowledge base with new information based on the truth value of a given sentence and query.
    If the truth value is true, add the sentence and query to the knowledge base.
    If the truth value is false, add the negation of the sentence and query to the knowledge base.

    Args:
        truth (bool): The truth value of the query.
        knowledge (And): The knowledge base to be updated.
        sentence (Symbol): The sentence to be added to the knowledge base.
        query (Symbol, optional): The query to be added to the knowledge base. Defaults to None.

    Returns:
        None. The function updates the knowledge base in place.
    """
    if truth:
        knowledge.add(sentence)
        if query is not None:
            knowledge.add(query)
    else:
        knowledge.add(Not(sentence))
        if query is not None:
            knowledge.add(Not(query))

# Puzzle 0
# A says "I am both a knight and a knave."





knowledge0 = And()
knowledge0.add(KNOWLEDGE_BASE)


query0 = And(
    AKnave,
    AKnight
)
truthOrLie0= checkQuery(knowledge0,query0)
AddToKnowledge(truthOrLie0,knowledge0,playerASentence, query0)






# Puzzle 1
# A says "We are both knaves."
# B says nothing.



knowledge1 = And()
knowledge1.add(KNOWLEDGE_BASE)

query1A = And(
    AKnave,
    BKnave
)


truthOrLie1A = checkQuery(knowledge1, query1A)
AddToKnowledge(truthOrLie1A,knowledge1,playerASentence, query1A)




# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."



knowledge2 = And()
knowledge2.add(KNOWLEDGE_BASE)

query2A = Or(
    And(AKnave,BKnave),
    And(AKnight,BKnight)
)

query2B = Not(
    Or(
    And(AKnave,BKnave),
    And(AKnight,BKnight)
    )
)

truthOrLie2A = checkQuery(knowledge2, query2A)
AddToKnowledge(truthOrLie2A, knowledge2,playerASentence,query2A)

truthOrLie2B = checkQuery(knowledge2, query2B)
AddToKnowledge(truthOrLie2B, knowledge2,playerBSentence,query2B)



# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And()
knowledge3.add(KNOWLEDGE_BASE)

query3A = Or(
    AKnight,
    AKnave
)

query3B = And(
    AKnave,
    CKnave
)

query3C = AKnight

truthOrLie3A = checkQuery(knowledge3, query3A)
AddToKnowledge(truthOrLie3A, knowledge3,playerASentence,query3A)


truthOrLie3B = checkQuery(knowledge3, query3B)
AddToKnowledge(truthOrLie3B, knowledge3,playerBSentence,query3B)


truthOrLie3C = checkQuery(knowledge3, query3C)
AddToKnowledge(truthOrLie3C, knowledge3,playerCSentence,query3C)









def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
