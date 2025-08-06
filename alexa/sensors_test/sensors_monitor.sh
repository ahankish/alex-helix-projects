#!/bin/bash

# runs the parser and sensors command for a predetermined (??) amount of time: 

TIME=$1 # How long to run the program
FILE=$2 # Name of the output file (for sensors)
SFILE=$3 # Name for the root file containing the parsed output

# create the .root output file and put the empty histogram(s) in it
#TH1D* h_fan = new TH1D("h_fan", "Fan Temp Histogram", 100, 0.0, 4.0);
#fan_gr->SetTitle("Fan Temp vs. Time");
#fan_gr->GetXaxis()->CenterTitle();
#fan_gr->SetName(“Fan Graph”);

root -l <<-EOF
std::unique_ptr<TFile> myFile( TFile::Open($SFILE, "RECREATE") );
myFile->cd();
auto fan_gr = new TGraph();
fan_gr->Write("FanGraph");
.q
EOF
#counter=0

# Loop over time: for every second, run sensors and the parser file once
#for (( timer=$SECONDS ; $timer < $TIME ; ));
  #do
    # run sensors and get a current reading 
    #sensors -j > $FILE

    # run the parser and add the parsed data to the output file
    #python3 parser.py $FILE $SFILE $counter ### add data to file here ==========================

    #while [ $SECONDS < $timer+1]
    #do
    	#continue
    #done
    #timer=$timer + 1
    #counter=$counter + 1
  #done

while [ $SECONDS < $TIME ];
do 
	sensors -j > $FILE
	
	#counter=$( echo " scale = 4; $SECONDS " | bc )
	# run the parser and add the parsed data to the output file
	#root -q parser.C( $FILE, $SFILE, $SECONDS )
	root -l -q parser.C($FILE. $SFILE, $SECONDS)
done
# Now, run the graphing file
#root -l grapher.C($FILE, $SFILE) # creates a .root file

EOF
