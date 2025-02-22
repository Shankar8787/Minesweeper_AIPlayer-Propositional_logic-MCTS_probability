from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


character_possibles = [(AKnight, AKnave), (BKnight, BKnave), (CKnight, CKnave)]
general_knowledge = {} # To store that any character is a either a Knight or a Knave

for index, character in enumerate(['A', 'B', 'C']):
    general_knowledge[character] = [
        Or(*character_possibles[index]), # Character is either be A knave or A knight, 
        Not(And(*character_possibles[index])) # but not both
        ]

# Puzzle 0
# A says "I am both a knight and a knave."
satement_A0 = And(AKnight, AKnave) # A is both a Knight and a Knave.

knowledge0 = And(
    Implication(AKnight, satement_A0), # if AKnight, then statement_A0 is true.
    Implication(AKnave, Not(satement_A0)), # if AKnave, then statement_A0 is false.
    *general_knowledge['A']
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
satement_A1 = And(AKnave, BKnave) # A and B are both Knaves
knowledge1 = And(
    Implication(AKnight, satement_A1), # If A is a knight, then statement_A1 is true.
    Implication(AKnave, Not(satement_A1)), # if A is a knave, then satement_A1 is false.
    *general_knowledge['A'], *general_knowledge['B']
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
statement_A2 = Or(And(AKnight, BKnight), And(AKnave, BKnave)) # A and B are of the same kind
statement_B2 = Or(And(AKnight, BKnave), And(AKnave, BKnight)) # A and B are of different kinds
knowledge2 = And(
    Implication(AKnight, statement_A2), # Look up puzzle 1 above to understand
    Implication(AKnave, Not(statement_A2)),
    Implication(BKnight, statement_B2),
    Implication(BKnave, Not(statement_B2)),
    *general_knowledge['A'], *general_knowledge['B']
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

# 

C_is_saying = And(Implication(CKnight, AKnight), Implication(CKnave, Not(AKnight)))
A_is_saying = Or(And( Implication(AKnight, AKnight), Implication(AKnave, Not(AKnight)) ),\
                 And( Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)) ))
A_says_according_to_B = And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))
B_is_saying1 = And(Implication(BKnight, A_says_according_to_B), Implication(BKnave, Not(A_says_according_to_B)))
B_is_saying2 = And(Implication(BKnight, CKnave), Implication(BKnave, Not(CKnave)))

knowledge3 = And(
    A_is_saying,
    B_is_saying1,
    B_is_saying2,
    C_is_saying,
    *general_knowledge['A'],
    *general_knowledge['B'],
    *general_knowledge['C']
    )



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
