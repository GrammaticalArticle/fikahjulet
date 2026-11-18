from common import *

print("This is a program for testing.")
if input("Press Enter to continue, or anything else to quit...") != "":
    quit()

def test_extend_taken_when_too_short():
    print(":::test_extend_taken_when_too_short")
    data = {}
    people = ["Anna", "Lisa", "Erik"]
    taken = [False]
    taken, people, data = format_json(taken, people, data)
    assert taken == [False, False, False]

def test_generate_default_people():
    print(":::test_generate_default_people")
    data = {}
    people = []
    taken = []
    taken, people, data = format_json(taken, people, data)
    assert len(people) == 10
    assert len(taken) == 10

test_extend_taken_when_too_short()
test_generate_default_people()
