#include "rapidjson/document.h"
#include <fstream>
#include <iostream>
#include <TFile>
#include <TGraph>

using namespace rapidjson;

// file for parsing the temperature output by time
// made to use with a script that runs lm-sensors and parses the json output
// made to run many time over a specific span of time 


int main(const char* fname, const char* out_fname, float time) {
	// parse .json file
	// fname = name of the .json file
	// out_fname = name of the .root file containing the graph
	// the time variable is in seconds
	
	std::string fname(argv[1]); 
	std::string out_fname(argv[2]);
	float time = argv[3];

	FILE* jsonFile = fopen(fname.c_str(), "r");

    	// Use a FileReadStream to
      	  // read the data from the file
    	char readBuffer[65536];
    	FileReadStream is(jsonFile, readBuffer,
       	                             sizeof(readBuffer));

    	// Parse the JSON data
      	  // using a Document object
    	Document senseDoc;
    	senseDoc.ParseStream(is);

    	// Close the file
    	fclose(jsonFile);

    	// Access the data in the JSON document
    	//std::cout << d["name"].GetString() << std::endl;
    	//std::cout << d["age"].GetInt() << std::endl;
	
	double fanOut = senseDoc["nct6796-isa-0290"]["fan2"]["fan2_input"];

	// Opening the .root file 
	std::unique_ptr<TFile> myFile( TFile::Open("file.root", "UPDATE") );
	std::unique_ptr<TGraph> fanGraph(myFile->Get<TGraph>("FanGraph"));

	fanGraph->AddPoint(time, output);
}

// should i delete all the info in the .json file for the next run of sensors? 
// or should i append the new data and parse it that way?
// the data would need to be appended in the dictionary/json format
