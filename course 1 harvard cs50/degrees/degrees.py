import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}




def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"degrees/{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"degrees/{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"degrees/{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "small"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    keep_going = True
    isOk1 = False
    isOk2 = False
    while keep_going:
        while isOk1 == False:
            source = person_id_for_name(input("Name: "))
            if source is None:
                sys.exit("Person not found.")
            else:
                isOk1 = True

        while isOk2 == False:
            target = person_id_for_name(input("Name: "))
            if target is None:
                sys.exit("Person not found.")
            else:
                isOk2 = True

        path = shortest_path(source, target)

        if path is None:
            print("Not connected.")
        else:
            degrees = len(path)
            print(f"{degrees} degrees of separation.")
            path = [(None, source)] + path
            for i in range(degrees):
                person1 = people[path[i][1]]["name"]
                person2 = people[path[i + 1][1]]["name"]
                movie = movies[path[i + 1][0]]["title"]
                year = movies[path[i + 1][0]]["year"]
                print(f"{i + 1}: {person1} and {person2} starred in {movie}, {year}")

        user_input = input("Do you want to do another one?(y/n) ")
        if user_input.startswith("n") or user_input.startswith("N"):
            keep_going = False
        else:
            isOk1 = False
            isOk2 = False


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    frontier = QueueFrontier()
    start = Node(state= source,parent=None,action=None)
    frontier.add(start)
    explored = []
    movie_list = []
    i = 0
    while True:
        i+=1
       
        
        
        node = frontier.remove()
        
        explored.append(int(node.state))
        
        
        if node.state == target:
            # print(f"made it + {node.state} + {node.parent.state}")
            combined = []
            while node.parent != None:
                combined.append((node.action, node.state))
                node = node.parent

            
            combined = combined[::-1]
            print(combined)
            return combined
        

        
        stars = list(neighbors_for_person(node.state))
        for movie,star in stars:
            if int(star) == node.state:
                stars = stars.pop(stars.index(star))

           
                


        for movie,star in stars:
            
            if int(star) not in explored:
                new_star = Node(state=star,parent = node, action = movie)  
                frontier.add(new_star)
            
        if frontier.empty():
             return None
        print(i)
        


    # TODO
    raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
