#include "MiniAODL1CandProducerV2.h"
  
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Photon.h"

typedef MiniAODL1CandProducerV2<pat::Electron> PatElectronL1CandProducerV2;
DEFINE_FWK_MODULE(PatElectronL1CandProducerV2);

typedef MiniAODL1CandProducerV2<pat::Photon> PatPhotonL1CandProducerV2;
DEFINE_FWK_MODULE(PatPhotonL1CandProducerV2);

