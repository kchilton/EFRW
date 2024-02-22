# EFRW
End Fed Random Wire, aka Long Wire, antenna projects

This program calculates suitable wire lengths for Long Wire antennas.
```
Usage: ./efrw.py [-d] [-h] [-u] [bands]
Options:
    -d, --debug          Provide debug information on stdout.
    -h, --help           Print a brief help message.
    -l, --level          Maximum harmonic to rule out, default is to use all.
    -m, --min            Percentage of frequency to consider the minimum 
                         practical be build, default is 1%.
    -t, --test           Test a particular length and explain why it does not work.
    -u, --usage          Print this usage info.
```
Valid bands are: 160, 80, 60, 40, 30, 20, 17, 15, 12, 10, 6

To calculate the possible EFRW lengths for the 80, 40, 20, 15, and 10m bands, use:
>    ./efrw.py 80 40 20 15 10

To calculate the possible EFRW lengths for all the valid bands listed, you can simply use:
>    ./efrw.py

The output will list the gaps, including the beginning and end frequencies
of the gap, the frequency width of the gap, and the wire length to use that gap.
All gaps are only considered within the range beginning from half the lowest band frequency
to the top of the highest band considered in the run.

It is generally recommended to choose one of the longest wire lengths within a large gap.

It is also possible that there is no solution, in which case this is reported.

To evaluate a suggested length, there is a -t option.  To test a 407.1 foot wire, run:
>    ./efrw.py -t 407.1
> 
The output will only report the bands and harmonics that will resonate in that length
