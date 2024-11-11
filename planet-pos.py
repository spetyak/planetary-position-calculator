import datetime
from math import floor, sin, cos, pi, sqrt
import csv

planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

monthToInt = {'January' : 1, 
              'February' : 2, 
              'March' : 3, 
              'April' : 4,
              'May' : 5, 
              'June' : 6, 
              'July' : 7, 
              'August' : 8,
              'September' : 9, 
              'October' : 10, 
              'November' : 11, 
              'December' : 12}

def sign(num):
    
    if num == abs(num):
        return 1
    else:
        return -1
    
def computeJulianDate(year, month, day, time):
    """
    Given a Gregorian date and time, converts the date to a Julian date.

    Args:
        year (int): _description_
        month (int): _description_
        day (int): _description_
        time (float): _description_

    Returns:
        float: _description_
    """
    
    # JD = 367K - <(7(K+<(M+9)/12>))/4> + <(275M)/9> + I + 1721013.5 + UT1/24 - 0.5sign(100K+M-190002.5) + 0.5
    # K is the year (1801 <= K <= 2099)
    # M is the month (1 <= M <= 12)
    # I is the day of the month (1 <= I <= 31)
    # UT is the universal time in hours ("<=" means "less than or equal to")
    # *** The last two terms in the formula add up to zero for all dates after 1900 February 28, so these two terms can be omitted for subsequent dates.
    # so: 
    # JD = 367K - <(7(K+<(M+9)/12>))/4> + <(275M)/9> + I + 1721013.5 + UT1/24
    
    
    return (367 * year) - floor((7 * (year + floor((month + 9) / 12))) / 4) + floor((275 * month) / 9) + day + 1721013.5 + (time / 24) - (0.5 * sign(100 * year + month - 190002.5)) + 0.5

def computeValue(i0, iDot, T):
    
    return i0 + (iDot * T)
    

def main():
    
    # get user input
    planetStr   = input("Planet: ")                         # check if planet is valid
    dayStr      = input("Target day (ex. 13): ")            # check if 1 <= day <= 31
    monthStr    = input("Target month (ex. February): ")    # check if valid month
    yearStr     = input("Target year (ex. 2012): ")         # check if year < 2050
    timeStr     = input("Target time (ex. hh:mm): ")        # check if valid time
    
    # read keplerian elements from file and store in dictionary for each planet
    keplerianElems = {}
    with open('keplerian-elements.txt', 'r') as file:
        line1 = file.readline().split()
        line2 = file.readline().split()
        while line1 and line2:
            keplerianElems[line1[0]] = {'a':float(line1[1]), 'e':float(line1[2]), 'I':float(line1[3]), 'L':float(line1[4]), 'varpi':float(line1[5]), 'omega':float(line1[6])}
            keplerianElems[line1[0]].update({'aDot':float(line2[0]), 'eDot':float(line2[1]), 'IDot':float(line2[2]), 'LDot':float(line2[3]), 'varpiDot':float(line2[4]), 'omegaDot':float(line2[5])})
            line1 = file.readline().split()
            line2 = file.readline().split()
    file.close()
    
    # read additional mean anomaly terms for planets that need them
    additionalTerms = {}
    with open('mean-anomaly-add-terms.txt', 'r') as file:
        line = file.readline().split()
        while line:
            additionalTerms[line[0]] = {'b':float(line[1]), 'c':float(line[2]), 's':float(line[3]), 'f':float(line[4])}
            line = file.readline().split()
    file.close()

    # convert given information into numbers that can be used to derive the Julian date
    day     = int(dayStr)
    month   = monthToInt[monthStr]
    year    = int(yearStr)
    time    = datetime.datetime.strptime(timeStr, "%H:%M").time()
    
    time    = time.hour + (time.minute / 60)

    julianDate = computeJulianDate(year, month, day, time)
    
    print(f"Julian date: {julianDate}")
    
    T = (julianDate - 2451545.0) / 36525
    
    print(f"T (cent. past J2000): {T}")
    
    # compute Keplerian elements
    axis            = computeValue(keplerianElems[planetStr]['a'], keplerianElems[planetStr]['aDot'], T)
    eccentricity    = computeValue(keplerianElems[planetStr]['e'], keplerianElems[planetStr]['eDot'], T)
    inclination     = computeValue(keplerianElems[planetStr]['I'], keplerianElems[planetStr]['IDot'], T)
    meanLong        = computeValue(keplerianElems[planetStr]['L'], keplerianElems[planetStr]['LDot'], T)
    longPeri        = computeValue(keplerianElems[planetStr]['varpi'], keplerianElems[planetStr]['varpiDot'], T)
    longAscNode     = computeValue(keplerianElems[planetStr]['omega'], keplerianElems[planetStr]['omegaDot'], T)
    
    print(f"axis:           {axis}")
    print(f"eccentricity:   {eccentricity}")
    print(f"inclination:    {inclination}")
    print(f"meanLong:       {meanLong}")
    print(f"longPeri:       {longPeri}")
    print(f"longAscNode:    {longAscNode}")
    
    
    perihelion = longPeri - longAscNode
    
    if planetStr == 'Jupiter' or planetStr == 'Saturn' or planetStr == 'Uranus' or planetStr == 'Neptune':
        
        b = additionalTerms[planetStr]['b']
        c = additionalTerms[planetStr]['c']
        s = additionalTerms[planetStr]['s']
        f = additionalTerms[planetStr]['f']
        
        # compute mean anomaly with additional terms
        meanAnomaly = meanLong - longPeri + (b * pow(T, 2)) + (c * cos(f * T)) + (s * sin(f * T))
        
    else:
        
        meanAnomaly = meanLong - longPeri
    
    # print(f"Perihelion: {perihelion}")
    
    meanAnomaly %= 360
    
    # if (meanAnomaly > 180):
        
    #     meanAnomaly = -180 + (meanAnomaly - 180)
        
    print(f"Mean Anomaly: {meanAnomaly}")
    
    eStar = (180 / pi) * eccentricity
    
    print(f"eStar: {eStar}")
    
    tol = 10E-6
    
    E = meanAnomaly + (eStar * sin(meanAnomaly))
    deltaE = 1
    
    while abs(deltaE) > tol:
        
        deltaM = meanAnomaly - (E - (eStar * sin(E)))
        deltaE = deltaM / (1 - (eccentricity * cos(E)))
        E = E + deltaE
    
    print(f"final eccentric anomaly (E): {E}")
    
    planarXcoord = axis * (cos(E) - eccentricity)
    planarYcoord = axis * (sqrt(1 - pow(eccentricity, 2))) * sin(E)
    planarZcoord = 0
    
    print(f"planar X coordinate: {planarXcoord}")
    print(f"planar Y coordinate: {planarYcoord}")
    print(f"planar Z coordinate: {planarZcoord}")
    
    # eclipticXcoord = ((cos(perihelion) * cos(longAscNode)) - (sin(perihelion) * sin(longAscNode) * cos(inclination))) * planarXcoord + ((-sin(perihelion) * cos(longAscNode)) - (cos(perihelion) * sin(longAscNode) * cos(inclination))) * planarYcoord
    # eclipticYcoord = ((cos(perihelion) * sin(longAscNode)) - (sin(perihelion) * cos(longAscNode) * cos(inclination))) * planarXcoord + ((-sin(perihelion) * sin(longAscNode)) - (cos(perihelion) * cos(longAscNode) * cos(inclination))) * planarYcoord
    # eclipticZcoord = (sin(perihelion) * sin(inclination)) * planarXcoord + (cos(perihelion) * sin(inclination)) * planarYcoord
    
    # print(f"ecliptic X coordinate: {eclipticXcoord}")
    # print(f"ecliptic Y coordinate: {eclipticYcoord}")
    # print(f"ecliptic Z coordinate: {eclipticZcoord}")
    
    # epsilon = 23.43928
    
    # equatorialXcoord = eclipticXcoord
    # equatorialYcoord = (cos(epsilon) * eclipticYcoord) - (sin(epsilon) * eclipticZcoord)
    # equatorialZcoord = (sin(epsilon) * eclipticYcoord) + (cos(epsilon) * eclipticZcoord)
    
    # print(f"equatorial X coordinate: {equatorialXcoord}")
    # print(f"equatorial Y coordinate: {equatorialYcoord}")
    # print(f"equatorial Z coordinate: {equatorialZcoord}")
    


    return

if __name__ == "__main__":
    main()
