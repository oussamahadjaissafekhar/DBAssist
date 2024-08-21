from Paritioning_system.PartitioningSchemaGenerator.semiClosedInterval import *
from typing import List
import pandas as pd
import sqlparse
from sqlparse.sql import Parenthesis, IdentifierList
from sqlparse.tokens import Whitespace, Punctuation

# functions for building intervals
def nextValue(value, attributeType , distinctValues): 
    value = int(value) if attributeType == "int" else value
    try: 
        if (distinctValues.index(value) < len(distinctValues) - 1):
            next = distinctValues[distinctValues.index(value)+1]
        else : 
            next = value + 1 if attributeType == "int" else value + "0"
    except Exception as e:
        distinctValues.append(value)
        distinctValues.sort()
        next = value if distinctValues.index(value) == len(distinctValues)-1 else distinctValues[distinctValues.index(value)+1]
        distinctValues.remove(value)
    return next

def valueOrMinimum(value, minimum):
    lowerBound = None
    if value < minimum:
        lowerBound = minimum
    else:
        lowerBound = value
    
    return lowerBound

def valueOrMaximum(value, maximum):
    upperBound = None
    if value > maximum:
        upperBound = maximum
    else:
        upperBound = value
    
    return upperBound

def INPredicateToEqualities(INPredicate: str, attributeType: str, attribute: str)-> List[str]:
    equalityPredicates = []
    values = extractValuesFromINPredicate(INPredicate, attributeType)
    for value in values:
        equality = attribute + " = " + str(value)
        equalityPredicates.append(equality)
    return equalityPredicates

#functions for manipulating intervals 
def findIntersectingIntervals(interval: SemiClosedInterval, rest: List[SemiClosedInterval])-> List[SemiClosedInterval]:

    intersectingIntervals =[]
    for i in rest: 
        if interval.intersects(i):
            intersectingIntervals.append(i)

    return intersectingIntervals
    
def extractNonIntersectingIntervals(first: SemiClosedInterval, second: SemiClosedInterval) -> List[SemiClosedInterval]:
    result = []
    if first.intersects(second):
        # If first interval starts before the second
        if first.lowerBound < second.lowerBound:
            result.append(SemiClosedInterval(first.lowerBound, second.lowerBound))
        
        # If second interval starts before the first or they start at the same point
        if second.lowerBound < first.lowerBound:
            result.append(SemiClosedInterval(second.lowerBound, first.lowerBound))
        
        # The overlapping part
        overlap_lower = max(first.lowerBound, second.lowerBound)
        overlap_upper = min(first.upperBound, second.upperBound)
        result.append(SemiClosedInterval(overlap_lower, overlap_upper))
        
        # If first interval ends after the second
        if first.upperBound > second.upperBound:
            result.append(SemiClosedInterval(second.upperBound, first.upperBound))
        
        # If second interval ends after the first
        if second.upperBound > first.upperBound:
            result.append(SemiClosedInterval(first.upperBound, second.upperBound))
    
    else:
        # No intersection, just return the two intervals
        result.append(first)
        result.append(second)
    
    # Remove zero-length intervals
    result = [interval for interval in result if interval.lowerBound != interval.upperBound]

    return result
    
def isAccessedRanges(partition: SemiClosedInterval, predicate: str, attributePredicateStats: pd.DataFrame)-> bool:
    lowerBound = attributePredicateStats.loc[attributePredicateStats["Predicate"]== predicate, "LowerBound"].values[0]
    upperBound = attributePredicateStats.loc[attributePredicateStats["Predicate"]== predicate, "UpperBound"].values[0]
    predicateInterval = SemiClosedInterval(lowerBound, upperBound)
    return predicateInterval.intersects(partition)


#functions for manipulating individual value ensembles
def isAccessedLists(partition: List, predicate: str, attributeType: str, attributePredicateStats: pd.DataFrame)-> bool:
    predicateAccessedValuesAsString = str(attributePredicateStats.loc[attributePredicateStats["Predicate"]== predicate, "AccessedValues"].values[0])
    predicateAccessedValues = predicateAccessedValuesAsString.split("+")
    if attributeType == "int":
        predicateAccessedValues = [int(value) for value in predicateAccessedValues]
    return bool(set(partition) & set(predicateAccessedValues))

def findIntersectingEnsembles(first : List, rest: List[List])->List[List]:
    intersectingEnsembles = []
    for e in rest:
        if bool(set(first) & set(e)):
            intersectingEnsembles.append(e)
    
    return intersectingEnsembles

def extractNonIntersectingEnsembles(first: List, second: List)->List[List]:
    result = []

    firstSet = set(first)
    secondSet = set(second)
    intersectionSet = firstSet & secondSet

    firstRemainder = sorted(list(firstSet-intersectionSet))
    secondRemainder = sorted(list(secondSet-intersectionSet))
    intersection = sorted(list(intersectionSet))

    if len(firstRemainder) > 0:
        result.append(firstRemainder)
    if len(secondRemainder) > 0:
        result.append(secondRemainder)
    if len(intersection) > 0:
        result.append(intersection)

    return result
    
def extractValuesFromINPredicate(predicate: str, attributeType: str, distinctValues: List) ->List[str]:
    # we take only the token that contains the list of values
    tokens = sqlparse.parse(predicate)[0].tokens
    parethesis = [token for token in tokens if isinstance(token, Parenthesis)][0]
    valueTokens = [token for token in parethesis.tokens if not (token.ttype in (Punctuation))]
    valueTokens = valueTokens[0]
    if isinstance(valueTokens, IdentifierList):
        # filtering the punctuations 
        valueTokens = [token for token in valueTokens.tokens if not token.ttype in (Punctuation, Whitespace)]
        values = [token.value.upper() for token in valueTokens]
    else: 
        values = [valueTokens.value.upper()]
    # removing quotes if attribute is int    
    if attributeType == "int":
        values = [value.strip("'") for value in values]
        
    # removing values that aren't in the distinctValues list
    if attributeType == "int":
        values = [value for value in values if value in distinctValues]
    else:
        values = [value for value in values if value.strip("'") in distinctValues]
    
    return values    