#!/usr/bin/env python3
'''
copyright (c) 2024, Kendell Chilton
All Rights Reserved
'''

import sys, argparse
from math import ceil,floor

bands = {'160': [ 1800000, 2000000], # band: f range in Hz
          '80': [ 3500000, 4000000], # using integers...
          '60': [ 5330500, 5406500], # it's a habit from
          '40': [ 7000000, 7300000], # working on too many
          '30': [10100000,10150000], # micros lately
          '20': [14000000,14350000],
          '17': [18068000,18168000],
          '15': [21000000,21450000],
          '12': [24890000,24990000],
          '10': [28000000,29700000],
           '6': [50000000,54000000],
         } 

def Evaluate(length,bandlist):
    '''
    Checks a length to see if it resonates inside a band of interest
    '''
    l = list(bands.keys())
    good = True
    bl = sorted(bandlist, key=lambda x:l.index(x))
    fun = 468000000.0/length
    print(f'Checking {length}ft, resonant 1/2 wave={fun/1000000:.2f}MHz') 
    if debug:
        print(f'Harmonics: ',end='')
        f=fun
        while f<bands['6'][1]:
            if f>fun: print(f', ',end='')
            print(f'{f/1000000:.1f}',end='')
            f+=fun
        print()
        
    for b in bl:
        top = bands[b][1]
        h = 1
        f = fun
        while f < top:
            if debug: print(f'#{b} {f:.0f} in {bands[b][0]} to {bands[b][1]}?')
            if ( f > bands[b][0] ) and ( f < bands[b][1] ):
                print(f'Harmonic {h}, {f/1000000.0:.2f}MHz, appears inside the {b}m band ({bands[b][0]/1000000.0} to {bands[b][1]/1000000.0}MHz)')
                good = False
            h += 1
            if level>=0 and h > level: break
            f = h * 468000000.0/length
    if good:
        print(f'Wire length of {length}ft does not have 1/2 wave harmonics ')
        if level>1: print(f'up to an order of {level}')
        print(f'on bands: {bandlist}')
        return 0
    return 1

def FindGaps(bandlist):
    '''
    The main use of the program: to find suitable wire lengths for the bands of interest
    '''
    # Create a list of frequency ranges
    rangelist = []
    for b in bandlist:
        rangelist.append(bands[b])
    rangelist.sort(key=lambda x: x[0])
    bottom = rangelist[0][0] / 2

    # Add disqualified ranges: ranges that will have harmonics within desired bands
    disqualified = []
    for r in rangelist:
        i = 2
        while(r[1]/i > bottom):
            disqualified.append([ floor(r[0]/i), ceil(r[1]/i) ])
            i += 1
            if (level>=0) and (i > level): break
    rangelist += disqualified
            
    # Combine overlaps
    newlist = []
    rangelist.sort(key=lambda x: x[0])
    if debug:
        print(16*'#')
        for r in rangelist:
            print(r)
    for i,r in enumerate(rangelist):
        if r[0]<0: continue
        for j,s in enumerate(rangelist[i+1:]):
            if s[0] < 0: continue            
            if (( (r[0] <= s[0]) and (r[1] >= s[0]) ) or  # s[0] is within r range
                ( (r[0] >= s[0]) and (r[0] <= s[1]) ) or  # r[0] is within s range
                ( (r[1] >= s[0]) and (r[1] <= s[1]) ) or  # r[1] is within s range
                ( (r[0] <= s[1]) and (r[1] >= s[1]) )):   # s[1] is within r range
                n =  [ min(r[0],s[0]) , max(r[1],s[1]) ]
                r = n.copy()
                rangelist[i] = r
                if debug: print(f'#Overlap: {r} + {s} -> {n}  {i} changed {j+i+1} deleted')
                rangelist[j+i+1] = [-1,-1]
        newlist.append(r)

    # Convert to gaps
    gaps = []
    n = -1
    for r in newlist:
        if n>0:
            if debug or (r[0]-n)/n >= tol:  # reject small gaps
                gaps.append([n,r[0]])
        n = r[1]
    return gaps

def main(args):
    global debug
    global level
    global tol

    def usage(name):
        print(f'Usage: {name} [-d] [-h] [-u] [bands]\nOptions:\n'+
              '    -d, --debug          Provide debug information on stdout.\n'+
              '    -h, --help           Print a brief help message.\n'+
              '    -l, --level          Maximum harmonic to rule out, default is to use all.\n'+
              '    -m, --min            Percentage of frequency to consider the minimum \n'+
              '                         practical be build, default is 1%.\n'+
              '    -t, --test           Test a particular length and explain why it does not work.\n'+
              '    -u, --usage          Print this usage info.\n'+
              f'Valid bands are: {list(bands.keys())}\n'+
              'To calculate the possible EFRW lengths for the 80, 40, 20, 15, and 10m bands, use:\n'+
              f'    {name} 80 40 20 15 10\n'+
              'To calculate the possible EFRW lengths for all the valid bands listed, you can simply use:\n'+
              f'    {name}\n'+
              'The output will list the gaps, including the beginning and end frequencies\n'+
              'of the gap, the frequency width of the gap, and the wire length to use that gap.\n'+
              'All gaps are only considered within the range beginning from half the lowest band frequency\n'+
              'to the top of the highest band considered in the run.\n\n'+
              'It is generally recommended to choose one of the longest wire lengths within a large gap.\n\n'+
              'It is also possible that there is no solution, in which case this is reported.\n\n'+
              'To evaluate a suggested length, there is a -t option.  To test a 407.1 foot wire, run:\n'+
              f'    {name} -t 407.1\n'+
              'The output will only report the bands and harmonics that will resonate in that length')

    parser = argparse.ArgumentParser(description='Random Wave Long Wire calculator', epilog='Without supplying {bands}, the result is all HF bands, 160m-6m.')
    parser.add_argument('bands',             nargs='*',           help='These are the bands that the antenna will use')
    parser.add_argument('-d', '--debug',     action='store_true', help='Provide additional debug output')
    parser.add_argument('-l', '--level',     action='store',      help='maximum harmonic, default=all', default=-1, type=int)
    parser.add_argument('-m', '--min',       action='store',      help='minimum frequency width percentage for build, default=1%', default=1.0, type=float)
    parser.add_argument('-t', '--test',      action='store',      help='test a wire length (in feet) instead of making suggestions', default=-1.0, type=float)
    parser.add_argument('-u', '--usage',     action='store_true', help='Provides additional information about the command line format')
    arg = parser.parse_args()

    debug = arg.debug
    tol = arg.min / 100.0
    level = arg.level
    
    if arg.usage:
        usage(args[0])
        return 0

    if arg.bands:
        bandlist = arg.bands
        for b in bandlist:
            if not b in bands.keys():
                print(f'Invalid band {b}')
                return 2
    else:
        bandlist = bands.keys()

    if arg.test > 0:
        return Evaluate(arg.test,bandlist)
        
    result = FindGaps(bandlist)
    if not result:
        print('no solution')
        return 1
    
    print('Beginning     End       Gap     Center   Wavelength       Cut')
    for gap in result:
        print(f'{gap[0]/1000000.0:>6.2f}MHz {gap[1]/1000000.0:>6.2f}MHz {(gap[1]-gap[0])/1000000.0:>6.2f}MHz '+
              f'{(gap[1]+gap[0])/2000000.0:>6.2f}MHz {936000000.0/(gap[1]+gap[0]):>8.2f} '+
              f'{(468000000.0/gap[1]+468000000.0/gap[0])/2:>8.1f} ± {(234000000.0/gap[0])-(234000000.0/gap[1]):>3.1f} ft')

if __name__ == '__main__':
    main(sys.argv)
