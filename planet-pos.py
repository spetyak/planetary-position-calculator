import datetime
from math import floor, sin, cos, pi, sqrt, atan2

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


    

def main():

    planet = input("Planet: ")
    day = int(input("Day: "))
    month = monthToInt[(input("Month: "))]
    year = int(input("Year: "))
    time = datetime.datetime.strptime(input("Time: "), "%H:%M").time()



    """
    TIME SCALE
    """
    
    # calculate julian day number
    d = 367 * year - 7 * (year + (month + 9) // 12) // 4 + 275 * month // 9 + day - 730530

    # convert time to decimal

    d += time.hour + (time.minute / 60)



    """
    ORBITAL ELEMENTS
    """

    N = 0 # longitude of ascending node
    i = 0 # inclination the ecliptic (plane of Earth's orbit)
    w = 0 # argument of perihelion
    a = 0 # semi-major axis, mean distance from Sun
    e = 0 # eccentricity (0=circle, 0-1=ellipse, 1=parabola)
    M = 0 # mean anomaly (0 at perihelion, increases uniformly with time)

    w1  = N + w                     # longitude of perihelion
    L   = M + w1                    # mean longitude
    q   = a * (1 - e)               # perihelion distance
    Q   = a * (1 + e)               # aphelion distance
    P   = pow(a, 1.5)               # orbital period (years)
    T   = Epoch_of_M - (M/360) / P  # time of perihelion
    v   = 0                         # true anomaly (angle between position and perihelion)
    E   = 0                         # eccentric anomaly

    ecl = 23.4393 - 3.563E-7 * d # obliquity of the ecliptic (tilt of the Earth's axis of rotation)

    # compute orbital elements of planet of interest

    E = M + e * (180/pi) * sin(M) * (1 + e * cos(M)) # first approximation of E (result is in degrees)

    if e > 0.05:

        while deltaE > 0.001:

            E1 = E - (E - e * (180/pi) * sin(E) - M) / (1 - e * cos(E))
            deltaE = E - E1
            E = E1

    xv = a * (cos(E) - e)
    yv = a * (sqrt(1 - e * e) * sin(E))

    v = atan2(yv, xv)
    r = sqrt(xv*xv + yv*yv)


    return

if __name__ == "__main__":
    main()
