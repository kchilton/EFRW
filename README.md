# EFRW
End Fed Random Wire, aka Long Wire, antenna projects

# Background
Many antenna projects have a drop of theory, a foundation in experimentation, and an overwhelming degree of misinformation.

When researching Long Wire antennas recently, I found that much of the "art" of this design has been confused.  The design has a foundation in the Zepp antenna.  Where the Zepp typically matched the antenna with a section of ladder line, the modern Long Wire or EFRW will use an UnUn transformer to match the wire to a coax.  Long Wire antennas were very popular in the early days of radio, but that popularity waned as newer designs took hold.  However, in recent years, the End-Fed Half-Wave (EFHW) has opened the door once again to the concept.

The difference between an EFHW and a Long Wire is that the EFHW expects the attached wire forming the antenna to be a multiple of the half-wavelength for the frequency of interest.  This is often calculated as:
> length (feet) = 468/_f_, where _f_ is the frequency in MHz

A Long Wire does not expect the wire to be resonant on the frequency of interest.  Rather, it purposely avoids it.  An EFHW is designed to provide the highest voltage point of the antenna at the connection to the UnUn.  The Long Wire prefers a lower impedance feed point that  strikes a balance between current and voltage.  As such, the Long Wire wants to be non-resonant at all frequencies of interest.

This project begins with some code.  The Python executable is provided to calculate lengths which do not resonate within the frequency bands of interest.  Later, the project may include evaluations of wire lengths, additional calculations that will drive design, and solutions for the UnUn.

# The code
This program calculates suitable wire lengths (in feet) for Long Wire antennas.
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

# Results
Some interesting results come from the program.  One is that a single wire length to cover 160m through 6m has the
side-effect that it must be significantly shorter than a resonant wire for 160m.  An end-fed antenna typically
becomes rapidly less effective as it becomes significantly shorter than 1/2 wavelength.  Two solutions are most
obvious: compromise the performance on 6m by allowing a 202.7' wire to resonate on 6m, or compromise the performance
on 160m and limit the length to 85.4'.  These are the tradeoffs that this program is intended to identify so
field testing can determine the most practical solution.  The extent and nature of the compromises of a shortened antenna 
versus resonating at a 25 harmonic, as well as other effects, can be incorporated into the program to build this into
a more comprehensive length recommendation engine.
```
./efrw.py 160 80 60 40 30 20 17 15 12 10 6         
Beginning     End       Gap     Center   Wavelength       Cut
  5.41MHz   5.56MHz   0.15MHz   5.48MHz    85.39     85.4 ± 1.2 ft
  6.06MHz   6.22MHz   0.17MHz   6.14MHz    76.23     76.2 ± 1.0 ft
  6.75MHz   7.00MHz   0.25MHz   6.88MHz    68.07     68.1 ± 1.2 ft
  7.71MHz   8.30MHz   0.58MHz   8.01MHz    58.46     58.5 ± 2.1 ft
  9.08MHz   9.33MHz   0.25MHz   9.21MHz    50.82     50.8 ± 0.7 ft
  9.90MHz  10.00MHz   0.10MHz   9.95MHz    47.04     47.0 ± 0.2 ft
 10.80MHz  12.45MHz   1.65MHz  11.62MHz    40.27     40.5 ± 2.9 ft
 13.50MHz  14.00MHz   0.50MHz  13.75MHz    34.04     34.0 ± 0.6 ft
 14.85MHz  16.67MHz   1.82MHz  15.76MHz    29.70     29.8 ± 1.7 ft
 18.17MHz  21.00MHz   2.83MHz  19.58MHz    23.90     24.0 ± 1.7 ft
 21.45MHz  24.89MHz   3.44MHz  23.17MHz    20.20     20.3 ± 1.5 ft
 27.00MHz  28.00MHz   1.00MHz  27.50MHz    17.02     17.0 ± 0.3 ft
 29.70MHz  50.00MHz  20.30MHz  39.85MHz    11.74     12.6 ± 3.2 ft
```

```
 ./efrw.py 160 80 60 40 30 20 17 15 12 10 6 -l 20
Beginning     End       Gap     Center   Wavelength       Cut
  1.14MHz   1.17MHz   0.03MHz   1.15MHz   406.57    406.6 ± 5.5 ft
  1.35MHz   1.38MHz   0.03MHz   1.37MHz   342.31    342.3 ± 3.9 ft
  2.28MHz   2.33MHz   0.05MHz   2.31MHz   202.69    202.7 ± 2.1 ft
  5.41MHz   5.56MHz   0.15MHz   5.48MHz    85.39     85.4 ± 1.2 ft
  6.06MHz   6.22MHz   0.17MHz   6.14MHz    76.23     76.2 ± 1.0 ft
  6.75MHz   7.00MHz   0.25MHz   6.88MHz    68.07     68.1 ± 1.2 ft
  7.71MHz   8.30MHz   0.58MHz   8.01MHz    58.46     58.5 ± 2.1 ft
  9.08MHz   9.33MHz   0.25MHz   9.21MHz    50.82     50.8 ± 0.7 ft
  9.90MHz  10.00MHz   0.10MHz   9.95MHz    47.04     47.0 ± 0.2 ft
 10.80MHz  12.45MHz   1.65MHz  11.62MHz    40.27     40.5 ± 2.9 ft
 13.50MHz  14.00MHz   0.50MHz  13.75MHz    34.04     34.0 ± 0.6 ft
 14.85MHz  16.67MHz   1.82MHz  15.76MHz    29.70     29.8 ± 1.7 ft
 18.17MHz  21.00MHz   2.83MHz  19.58MHz    23.90     24.0 ± 1.7 ft
 21.45MHz  24.89MHz   3.44MHz  23.17MHz    20.20     20.3 ± 1.5 ft
 27.00MHz  28.00MHz   1.00MHz  27.50MHz    17.02     17.0 ± 0.3 ft
 29.70MHz  50.00MHz  20.30MHz  39.85MHz    11.74     12.6 ± 3.2 ft
 ```
