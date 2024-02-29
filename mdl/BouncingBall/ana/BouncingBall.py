#!/usr/bin/env python

# Analytical Solution of BouncingBall.mo Model for Comparison

# Notes
#  This is analytical between impacts but impact states are stored
#   in floats so over time this becomes less precise
#  g = 9.80665 m/s^2 is used
#  e = 0.8 is used as the coefficient of restitution
#  With h0, v0, and t0 at the last impact the equations are:
#   v = v0 - g * ( t - t0 )
#   h = h0 + v0 * ( t - t0 ) - 1/2 * g * ( t - t0 )^2
#  Ball starts at 1 m with 0 velocity: h = 1 - 1/2 * g * t^2
#   So first impact (h=0): ti = sqrt( 2 / g ) = 0.451600756
#  After first impact all bounces start with h0 = 0 so
#   h = v0 * ( t - t0 ) - 1/2 * g * ( t - t0 )^2
#   giving the next impact at ti = t0 + 2 * v0 / g

import math

# Constants
g = 9.80665
e = 0.8
dtOut = 1e-4
tStop = 3.0

# Variables
i = 0 # Loop count
t = t0 = 0.0
h = h0 = 1.0
v = v0 = 0.0
ti = math.sqrt( 2 / g ) # First impact time

# Solution
print( 'Time' + '\t' + 'Height' )
print( 's' + '\t' + 'm' )
while t <= tStop:
    if t >= ti: # Impact
        print( "%.15f" % ti + '\t' + '0.0' )
        h0 = 0.0
        v0 = abs( e * ( v0 - g * ( ti - t0 ) ) )
        t0 = ti
        t = ti # Reset steps from impact time
        ti_next = t0 + ( 2 * v0 / g )
        if ti_next <= ti:
            t = 3.0
            print( "%.15f" % t + '\t' + '0.0' )
        else:
            ti = ti_next
    else: # Parabolic trajectory
        h = h0 + ( v0 * ( t - t0 ) ) - ( 0.5 * g * ( t - t0 )**2 )
        print( "%.15f" % t + '\t' + "%.15f" % h )
    i += 1
    t = i * dtOut # Avoid potential drift of t += dtOut
