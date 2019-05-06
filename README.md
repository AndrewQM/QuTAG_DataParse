A note on FQNETDAQ.c: Recompile the code with a reasonable trigger level after looking at SNSPD pulse output on an oscilliscope. (currently set ot 0.35V in line 108-111 of FQNETDAQ.c)


# FQNETDAQ and QuTAG_DataParse

****************************************

Run QuTAG_Dataparse with the following command:

    $python QuTAG_Dataparse.py "datafile.txt" g

`datafile.txt` should be the output from the `FQNETDAQ` program. The optional `g` tag loads the GUI for entering data analysis parameters. Without the tag, `QuTAG_Dataparse.py` pulls parmeters from `dataparse_params.txt`. For manual entry, the GUI is preferable because slight formatting changes to `dataparse_params.txt` may corrupt it. `dataparse_params.txt` is intended to be modifierd by other programs through a network connection.


## QuTAG_DataParse functionality
****************************************

The data file directed to `dataparse_params.txt` has a format like:

```
1821818207390494 1821818209645169 -666 -666                   
1821818217390470 1821818219645174 -666 1821818219645194  
1821818227390492 1821818229645153 -666 -666                     
1821818237390479 -666             -666 1821818239645186
1821818247390489 1821818249645186 -666 -666
1821818257390485 1821818259645173 -666 -666
1821818267390490 1821818269645168 -666 1821818269645168
1821818277390492 1821818279645187 -666 -666
1821818287390501 -666             -666 1821818269645168
```

*Note: the time tags shown are for illustrative purposes only and are not representative of an actual data stream. TABS have also been added to make the formal more clear.*

The pseudo-data above implies the clock is on channel 1, a semi-often event is on channel 2, and a rarer even is on channel 4. Channel 3 is unused.

With the data formatted this way, a line corresponds to a 'detection event'. `dataparse_params.txt` applies to each detection event a series of accept/reject operations or *Masks* based on specified coincidence window and offset parameters between any two channels. Masks are combined with logical AND or OR operations allowing the overall coincidence detection process involving all four channels to be quite complex.

The following shows corresponding values of 3 masks to the right of the timetag data:

```
1821818207390494 1821818209645169 -666 -666                     1   0   1
1821818217390470 1821818219645174 -666 1821818219645194         1   1   1
1821818227390492 1821818229645153 -666 -666                     1   0   1
1821818237390479 -666             -666 1821818239645186         0   0   1
1821818247390489 1821818249645186 -666 -666                     1   0   1
1821818257390485 1821818259645173 -666 -666                     1   0   1
1821818267390490 1821818269645168 -666 1821818269645192         1   1   1
1821818277390492 1821818279645187 -666 -666                     1   0   1
1821818287390501 -666             -666 1821818269645168         0   0   1
```

Parameters that would generate the first mask values given the input values could be:
```
    ChannelA: 1
    ChannelB: 2
    Offset: 0
    Window:3000000
```
In this case, the 1st mask accepts a coincidence event if the clock channel and channel 2 timestamps for that event are within 3µs of each other.
The second mask could be generated with Channel A as 2, and Channel B as 4. Notice how masks can be generated with two channels neither of which are the clock channel.

The offset value is subtracted from the Channel B timestamp before checking if the timestamps of Channel A and B fall within the window time.

If the Channel A, Channel B, or Window parameters of a mask are left blank, the mask is deactivated and does not infuence the final calculation.

## QuTAG_DataParse integration method
****************************************

### by time
This mode is intended to be used when data is collected over some period during which a degree of freedom of the experimental apparatus changes smoothly. For example, the optical delay line could be scanning though it's full range as FQNETDAQ collects data.

For example, say data is continuously collected with FQNETDAQ for 1 minute. The Integration Bins parameter specifies how many chunks of time will be integrated over to generate coincidence data points. If the Integration Bins value is 60, then the number of events matching the coincidnece criteria in 1-second intervals will be added together to generate coincidence sum data points.

### by files
This mode is intended for when FQNETDAQ is run multiple times generating multiple files, each time while the experimental apparatus is static (no degrees of freedom like polarization or time delay are being actively changed). Data files should be numbered so that they end with an underscore followed by a file number. For example, the following files could be automatically found in the current directory and processed by QuTAGDataparse if the first argument passed to the program during execution was "testdata_1.txt".

    testdata_1.txt
    testdata_2.txt
    testdata_3.txt
    testdata_4.txt
    ...

Working with files in a directory other than QuTAGDataparse is not yet supported. There is more work to be done on clarifying the form of output data from the by-time and by-files methods (e.g. specifying the bin number and corresponding time for coincidence counts generated in by-time mode). For now, the array generated with either method is saved as a file named `ParseOutput.txt` in the current directory. 
