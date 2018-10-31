import itertools
import random
import googlemaps
import csv

# gmaps = googlemaps.Client(key="")

# Geocoding an address
# geocode_result = gmaps.distance_matrix('Anuradhapura', 'Gampaha')
# print(geocode_result)


def getDemandSupplylist(condemdic, randomchoice):
    temp = []
    for item in randomchoice:
        temp.append(condemdic[item])
    return temp


def getbestsolution(randomchoicedict, randomChoiceDemand):
    solutions = []
    tempDict = randomchoicedict.copy()
    solutions.append(tempDict)
    print(f"tempDict : {tempDict}")
    print(f"solutions : {solutions}")
    print(f"randomChoiceDemand : {randomChoiceDemand}")
    print(f"list(tempDict.values()) : {list(tempDict.values())}")
    maxValue = getproducerlist(randomChoiceDemand, list(tempDict.values()))
    print(f"maxValue : {maxValue}")

    if len(tempDict) > 1:
        for x in range(2, len(tempDict) + 1):
            print(f"x : {x}")
            for item in list(itertools.permutations(list(tempDict.keys()), x)):
                print(f"item : {item}")
                tempValues = list(item)
                tempDict = randomchoicedict.copy()
                for key in tempValues[:-1]:
                    print(f"key : {key}")
                    tempDict[tempValues[-1]] = tempDict[tempValues[-1]] + tempDict[key]
                    tempDict[key] = 0
                print(f"final -----------------------------> {list(tempDict.values())}")
                getValue = getproducerlist(randomChoiceDemand, list(tempDict.values()))
                print(f"getValue : {getValue}")
                if (maxValue == getValue):
                    solutions.append(tempDict)
                if (maxValue < getValue):
                    maxValue = getValue
                    solutions.clear()
                    solutions.append(tempDict)

    print(f"solutions : {solutions}")
    randomSolution = random.choice(solutions)

    for cons in consumer:
        print(f"\t\t\t\t {cons}", end='')

    print("\nDemand", end='')

    for dem in demand:
        print(f"\t\t\t\t {dem}", end='')

    print(f"\nSolution", end='')

    for cons in consumer:
        print(f"\t\t\t\t {randomSolution[cons]}", end='')

    print(f"\nFitness Value : {maxValue}")


def getproducerlist(demand, randomChoiceSupply):
    temp = 0.0
    for x in range(len(supply)):
        if (demand[x] == randomChoiceSupply[x]):
            temp = temp + 1
        if (demand[x] < randomChoiceSupply[x]):
            temp = temp + 0.5
        if (demand[x] > randomChoiceSupply[x]):
            temp = temp + 0
    return temp


def getproducermoisture(moisture):
    initMmistureValue, temp = 13, 0.0
    for item in moisture:
        if (item == initMmistureValue):
            temp = temp + 1.0
        if (item < initMmistureValue):
            temp = temp + 0.5
        if (item > initMmistureValue):
            temp = temp + 0.0
    return temp


# details according to district
producer, consumer, supply, demand = [], [], [], []
csvCount = 0
with open('db.csv', mode='r') as db:
    for row in csv.reader(db):
        if csvCount != 0:
            producer.append(row[1])
            supply.append(float(row[2]))
            consumer.append(row[3])
            demand.append(float(row[4]))
        csvCount += 1

conSupDict = dict(zip(consumer, supply))
conDemDict = dict(zip(consumer, demand))
print(f"conSupDict : {conSupDict}")
print(f"conDemDict : {conDemDict}")
# get all the possibilities from the consumer list
allPossibilities = [list(row) for row in itertools.permutations(consumer)]
print(f"allPossibilities : {allPossibilities}")
# select one random choice from the all possibilities
randomChoice = random.choice(allPossibilities)
print(f"randomChoice : {randomChoice}")
# get demand for randomly choice district
randomChoiceSupply = getDemandSupplylist(conSupDict, randomChoice)
print(f"randomChoiceSupply : {randomChoiceSupply}")
randomChoiceDemand = getDemandSupplylist(conDemDict, randomChoice)
print(f"randomChoiceDemand : {randomChoiceDemand}")
randomChoiceDict = dict(zip(randomChoice, randomChoiceSupply))
print(f"randomChoiceDict : {randomChoiceDict}")
getbestsolution(randomChoiceDict, randomChoiceDemand)

# getProducerList(supply, randomChoiceSupply)

# print(list(itertools.combinations(consumer, 2)))
