__author__ = 'maxomdal'

import math
import csv

#Max Omdal
#Slope One Item-Based Collaborative Filtering Algorithm
#Gives the predicted ratings of items based on other users' ratings
with open("Ratings.csv", 'rU') as p:
    users = [list(map(int,rec)) for rec in csv.reader(p, delimiter=',')]

with open("restaurants.txt") as f:
    restaurants = f.readlines()

allRatings = []

def normalize(users): #take data and subtract the average rating per user from each rating
    normalUsers = []
    for user in users:
        if sum(i for i in user) == 0:
            del users[users.index(user)]
            break
        def avg(): #find the aveage rating of a user
            average = float(0)
            for i in range(len(user)):
                if i != 0:
                    average += float(user[i-1])
            average = average/(float(len(user) - user.count(0)))
            return average
        average = avg()
        def subtract(x):
            if x != 0: return float(x) - average
            else: return 0
        normalUsers.append(map(subtract,user))
    return normalUsers

def cosineDistance(main,user): # takes two items and calculates the cosine distance between them and returns it to the compare function
    dotProduct = sum( [main[i]*user[i] for i in range(len(user))] )
    length = math.sqrt(sum([main[i]**2 for i in range(len(main))]))*math.sqrt(sum([user[i]**2 for i in range(len(user))]))
    return dotProduct/length

def compare(main,users): # calls the cosine distance function and returns the user most similar to user A
    topSimilarities = []
    for user in users:
        distance = cosineDistance(main, user)
        topSimilarities.append((distance, user)) # holds the cosine distance between each user and the main, and the user's ratings
    def getKey(item):
        return item[0]
    topSimilarities.sort(key=getKey, reverse=True)
    relevantUsers = [x[1] for x in topSimilarities] # ignores the cosine distance when going into the recommend function
    recommend(main, relevantUsers[:3])

def recommend(main, topUsers): # takes the most similar user and gives recommendations based off them
    unratedVals = []
    for i, j in enumerate(main):
        if j == 0:
            unratedVals.append(i)
    def union(a):
        count = 0
        for user in topUsers:
            if user[a] != 0 and user[a+1] != 0:
                count += 1
        return count
    def linear(unrated): #returns the values of y for the function y = x + b
        yVals = []
        fullUser = [main] + topUsers
        def calcB(pos): #find b for function y = x + b
            totalVals = []
            noCount = 0
            b = 1
            while b < len(main):
                total = 0
                for z in range(len(fullUser)):
                    if fullUser[z][pos] != 0 and fullUser[z][b] != 0:
                        difference1 = fullUser[z][pos]
                        difference2 = fullUser[z][b]
                        total += (difference1 - difference2)
                    else:
                        noCount += 1
                b+=1
                totalVals.append(total)
            def division(x):
                if float(unionVals[totalVals.index(x)]) != 0:
                    return float(x)/float(unionVals[totalVals.index(x)])
                else:
                    return 0
            return map(division, totalVals)
        b = calcB(unrated)
        for i in range(1,len(main)):
            x = float(main[i]) #finds value of x, where x is the value of the next item beyond the unknown rating
            y = x + b[i-1]
            yVals.append(y)
        return yVals
    print unratedVals
    for unrated in unratedVals:
        unionVals = []
        for a in range(len(topUsers[0]) - 1):
            unionVals.append(union(a))
        if len(unionVals) != 0:
            yVals = linear(unrated)
            rating = 0
            for j,i in enumerate(yVals):
                rating += i*unionVals[j]
            rating = rating/(sum(i for i in unionVals))
            allRatings.append(rating)
    print "The top rating was given a predicted normalized rating of:"
    print max(allRatings)
    print allRatings
    print restaurants[unratedVals[int(allRatings.index(max(allRatings)))]]

normalizedUsers = normalize(users)
compare(normalizedUsers[0], normalizedUsers[1:])