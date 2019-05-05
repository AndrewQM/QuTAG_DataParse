

# FQNETDAQ and QuTAG_DataParse

****************************************

Run QuTAG_Dataparse with teh following command

    $python QuTAG_Dataparse.py "datafile.txt" g

`datafile.txt` should be the output from the `FQNETDAQ` program. THe optional `g` tag loads the GUI for entering data analysis parameters. Without the tag, `QuTAG_Dataparse.py` pulls parmeters from `dataparse_params.txt`. For manual entry, the GUI is preferable because slight formatting changes to `dataparse_params.txt` may corrupt it. `dataparse_params.txt` is intended to be easily modifiable by other programs through a network connection.


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

With the data formatted this way, a line corresponds to a 'detection event'. `dataparse_params.txt` applies to each detection even a series of accept/reject or operations or *Masks* based on specified coincidence window and offset between two channels. Masks are combined with logical AND or OR operations allowing the overall coincidence detection process involving all four channels to be quite complex.

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
