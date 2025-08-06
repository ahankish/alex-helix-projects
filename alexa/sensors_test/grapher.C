#include <iostream>
#include <TH1D.h>
#include <TF1.h>
#include <TCanvas.h>
#include <TRandom.h>
#include <TStyle.h>
#include <TLegend.h>
#include <TROOT.h>
#include <TPaveText.h>
#include <string>
#include <TFile.h>
#include <TApplication.h>
#include <TMarker.h>
#include <TSystem.h> 
#include <TGraph>

void grapher(std::string filename){
  // do some graphing
  std::unique_ptr<TFile> monitor_file( TFile::Open(filename.c_str()) ); // opening the input file 

  if (!monitor_file || monitor_file->IsZombie()) { // checking if the file opened properly
   std::cerr << "Error opening file " << filename << std::endl;
   exit(-1);
  }

  // The opened file should contain data in a graph already
  // it just needs to be displayed 
  std::unique_ptr<TGraph> fan_graph(monitor_file->Get<TGraph>(“Fan Graph”));
  fan_graph->Draw();
}

