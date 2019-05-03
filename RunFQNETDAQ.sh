export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/daisy

#####################################################################
#Configuration Parameters
#####################################################################

#Sets the coincidence window in [ps]. If you want the program to
#calculate the appropriate coincidence window automatically, set
#it to -1
CoincidenceWindow=-1
#219610
#Don't change this
MasterRate=1

#Number of [us] for each readout cycle.
#This number times the signal rate should be below the
#max buffer size, or else you will lose data
CollectTime=10000

#Total time that you want to collect data for in [s]
DAQTotalTime=1


#####################################################################
#Internal Calculations
#####################################################################
#Calculate number of readout cycles to take data for DAQTotalTime
CollectRounds=$(($DAQTotalTime*1000000/$CollectTime))

#echo $CoincidenceWindow $MasterRate $CollectTime $CollectRounds

echo $HOME"/daisy/userlib/QuTagDAQ/FQNETDAQ signal "$CoincidenceWindow $MasterRate $CollectTime $CollectRounds
~/daisy/userlib/QuTagDAQ/FQNETDAQ signal $CoincidenceWindow $MasterRate $CollectTime $CollectRounds
