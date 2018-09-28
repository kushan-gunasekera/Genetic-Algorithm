import itertools
import csv
import googlemaps

# gmaps = googlemaps.Client(key="")

# Geocoding an address
# geocode_result = gmaps.distance_matrix('Anuradhapura', 'Gampaha')
# print(geocode_result)


def getDemandSupplylist(condemdic, randomchoice):
    temp = []
    for item in randomchoice:
        temp.append(condemdic[item])
    return temp


def getBestFits(solutions):
    firstFit, firstFitValue, secondFit, secondFitValue, count = [], 0.0, [], 0.0, 0
    for c in solutions:
        if count == 0:
            firstFit, firstFitValue = c["district"], c["maxValue"]
        elif firstFitValue < c["maxValue"]:
            secondFit, secondFitValue, firstFit, firstFitValue = firstFit, firstFitValue, c["district"], c["maxValue"]
        elif secondFitValue < c["maxValue"]:
            secondFitValue, secondFit = c["maxValue"], c["district"]
        count = count + 1
    return firstFit, firstFitValue, secondFit, secondFitValue


def crossOver(ffSupply, ffDemand, ff, sfSupply, sfDemand, sf):
    tempFFSupply= ffSupply[:dividePoint] + sfSupply[dividePoint:]
    tempFFDemand = ffDemand[:dividePoint] + sfDemand[dividePoint:]
    tempFF = ff[:dividePoint] + sf[dividePoint:]
    tempSFSupply = sfSupply[:dividePoint] + ffSupply[dividePoint:]
    tempSFDemand = sfDemand[:dividePoint] + ffDemand[dividePoint:]
    tempSF = sf[:dividePoint] + ff[dividePoint:]
    return tempFFSupply, tempFFDemand, tempFF, tempSFSupply, tempSFDemand, tempSF


def getBestSolutions(randomchoicedict, randomChoiceDemand):
    maxValue = getProducerList(randomChoiceDemand, list(randomchoicedict.values()))
    solutions.append({"district": list(randomChoiceDict.keys()), "maxValue": maxValue})


def finalSolution(solution, ffValue, ffList, conSupDict, conDemDict):
    for sol in solution:
        if sol["maxValue"] > ffValue:
            ffValue = sol["maxValue"]
            ffList = sol["district"]
    print("First Fitness Value : " + str(ffValue))
    print("First Fitness Disctricts : ")
    print(list(distr for distr in ffList))
    print("Supply : ")
    print(list(conSupDict[distr] for distr in ffList))
    print("Demand : ")
    print(list(conDemDict[distr] for distr in ffList))


def getProducerList(randomDemandValue, randomchoice):
    temp = 0.0
    for x in range(len(randomchoice)):
        if (randomDemandValue[x] == randomchoice[x]):
            temp = temp + 1.0
        if (randomDemandValue[x] < randomchoice[x]):
            temp = temp + 0.0
        if (randomDemandValue[x] > randomchoice[x]):
            temp = temp + 0.5
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
solutions = []
dividePoint = 1

# get all the possibilities from the consumer list
allPossibilities = [list(row) for row in itertools.permutations(consumer)]

for oneByOnePosibilities in allPossibilities:
    randomChoiceSupply = getDemandSupplylist(conSupDict, oneByOnePosibilities)
    randomChoiceDemand = getDemandSupplylist(conDemDict, oneByOnePosibilities)
    randomChoiceDict = dict(zip(oneByOnePosibilities, randomChoiceSupply))
    getBestSolutions(randomChoiceDict, randomChoiceDemand)


firstFit, firstFitValue, secondFit, secondFitValue = getBestFits(solutions)
solutions.clear()
firstFitSupply, firstFitDemand = getDemandSupplylist(conSupDict, firstFit), getDemandSupplylist(conDemDict, firstFit)
secondFitSupply, secondFitDemand = getDemandSupplylist(conSupDict, secondFit), getDemandSupplylist(conDemDict, secondFit)
fFSupply, fFDemand, fF, sFSupply, sFDemand, sF = crossOver(firstFitSupply, firstFitDemand, firstFit, secondFitSupply, secondFitDemand, secondFit)
firstDict, secondDict = dict(zip(fF, fFSupply)), dict(zip(sF, sFSupply))
getBestSolutions(firstDict, firstFitDemand)
getBestSolutions(secondDict, secondFitDemand)
finalSolution(solutions, firstFitValue, firstFit, conSupDict, conDemDict)