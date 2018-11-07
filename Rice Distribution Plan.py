import itertools
import random
import googlemaps
import csv

# gmaps = googlemaps.Client(key="")

# Geocoding an address
# geocode_result = gmaps.distance_matrix('Anuradhapura', 'Gampaha')
# print(geocode_result)


def getDemandList(demand, randomchoice):
    temp = []
    for item in randomchoice:
        temp.append(demand[item])
    return temp


def getSupplyList(supply, district, randomChoice):
    temp = []
    for item in randomChoice:
        temp.append(supply[district[item]])
    return temp


def getValuesDict(randomDict, randomDemand):
    temp = {}
    for key in randomDemand.keys():
        pass



def getBestSolution(randomChoiceDict, randomChoiceDemand, districtDict):
    print("*****************************************************************************************")
    solutions = []
    print(f"randomChoiceDict : {randomChoiceDict}")
    print(f"randomChoiceDemand : {randomChoiceDemand}")
    print(f"districtDict : {districtDict}")
    print(f"list(randomChoiceDemand.values()) : {list(randomChoiceDemand.values())}")
    print(f"list(randomChoiceDict.values()) : {list(randomChoiceDict.values())}")
    maxValue = getProducerList(list(randomChoiceDemand.values()), list(randomChoiceDict.values()))
    print(f"maxValue : {maxValue}")

    # demandTempList = []
    # for key in randomChoiceDemand.keys():
    #     demandTempList.append(randomChoiceDict[districtDict[key]])

    demandTempDict = dict(zip(list(randomChoiceDemand.keys()), list(randomChoiceDict.values())))
    solutions.append(demandTempDict)
    print(f"solutions : {solutions}")

    if len(randomChoiceDict) > 1:
        for x in range(2, len(randomChoiceDict) + 1):
            print(f"x : {x}")
            for item in list(itertools.permutations(list(randomChoiceDemand.keys()), x)):
                print(f"item : {item}")
                tempValues = list(item)
                tempDict = dict(zip(list(randomChoiceDemand.keys()), list(randomChoiceDict.values())))
                print(f"tempDict : {tempDict}")
                print(f"tempValues : {tempValues}")
                print(f"randomChoiceDemand : {randomChoiceDemand}")
                print(f"randomChoiceDict : {randomChoiceDict}")
                for key in tempValues[:-1]:
                    print(f"key : {key}")
                    tempDict[tempValues[-1]] = tempDict[tempValues[-1]] + tempDict[key]
                    tempDict[key] = 0
                print(f"final -----------------------------> {tempDict}")
                getValue = getProducerList(list(randomChoiceDemand.values()), list(tempDict.values()))
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


def getProducerList(demand, randomChoiceSupply):
    print("=============================================")
    print(f"demand : {demand}")
    print(f"randomChoiceSupply : {randomChoiceSupply}")
    temp = 0.0
    for x in range(len(supply)):
        if (demand[x] == randomChoiceSupply[x]):
            temp = temp + 1
        if (demand[x] < randomChoiceSupply[x]):
            temp = temp + 0.5
        if (demand[x] > randomChoiceSupply[x]):
            temp = temp + 0
    print(f"temp : {temp}")
    print("=============================================")
    return temp


# def getproducermoisture(moisture):
#     initMmistureValue, temp = 13, 0.0
#     for item in moisture:
#         if (item == initMmistureValue):
#             temp = temp + 1.0
#         if (item < initMmistureValue):
#             temp = temp + 0.5
#         if (item > initMmistureValue):
#             temp = temp + 0.0
#     return temp


# details according to district
producer, consumer, supply, demand = [], [], [], []
csvCount = 0
with open('db.csv', mode='r') as db:
    for row in csv.reader(db):
        if csvCount != 0 and row != []:
            producer.append(row[1])
            supply.append(float(row[2]))
            consumer.append(row[3])
            demand.append(float(row[4]))
        csvCount += 1

conSupDict = dict(zip(producer, supply))
conDemDict = dict(zip(consumer, demand))
districtDict = dict(zip(consumer, producer))
print(f"conSupDict : {conSupDict}")
print(f"conDemDict : {conDemDict}")
print(f"districtDict : {districtDict}")
# get all the possibilities from the consumer list
allPossibilities = [list(row) for row in itertools.permutations(consumer)]
print(f"allPossibilities : {allPossibilities}")

# select one random choice from the all possibilities
randomChoice = random.choice(allPossibilities)
print(f"randomChoice : {randomChoice}")

# get demand for randomly choice district
randomChoiceSupply = getSupplyList(conSupDict, districtDict, randomChoice)
print(f"randomChoiceSupply : {randomChoiceSupply}")

randomChoiceDemand = getDemandList(conDemDict, randomChoice)
print(f"randomChoiceDemand : {randomChoiceDemand}")

producer.clear()
for key in randomChoice:
    producer.append(districtDict[key])

randomChoiceDict = dict(zip(producer, randomChoiceSupply))
print(f"randomChoiceDict : {randomChoiceDict}")

randomChoiceDemandDict = dict(zip(randomChoice, randomChoiceDemand))
print(f"randomChoiceDemandDict : {randomChoiceDemandDict}")

getBestSolution(randomChoiceDict, randomChoiceDemandDict, districtDict)