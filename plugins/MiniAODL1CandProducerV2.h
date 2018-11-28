#ifndef _MINIADOL1CANDPRODUCER_H_
#define _MINIADOL1CANDPRODUCER_H_

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/L1Trigger/interface/L1EmParticle.h"
#include "DataFormats/L1Trigger/interface/L1EmParticleFwd.h"

#include <DataFormats/Math/interface/deltaR.h>

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/HLTReco/interface/TriggerFilterObjectWithRefs.h"
#include "DataFormats/L1Trigger/interface/EGamma.h"

#include <string>
#include <vector>

template <class T>
class MiniAODL1CandProducerV2 : public edm::EDProducer {

  typedef std::vector<T> TCollection;
  typedef edm::Ref<TCollection> TRef;
  typedef edm::RefVector<TCollection> TRefVector;

public:
  MiniAODL1CandProducerV2(const edm::ParameterSet&);
  ~MiniAODL1CandProducerV2();

  bool l1OfflineMatching(const std::vector<l1t::EGammaRef>& triggerObjects, 
			 math::XYZTLorentzVector refP4, float dRmin, int& index);

 private:
  /// compare two l1Extra in et

  virtual void produce(edm::Event&, const edm::EventSetup&) override;
  
  edm::EDGetTokenT<TRefVector> inputs_;
  //edm::EDGetTokenT<l1extra::L1EmParticleCollection> l1IsoObjectsToken_;
  //edm::EDGetTokenT<l1extra::L1EmParticleCollection> l1NonIsoObjectsToken_;
  edm::EDGetTokenT<trigger::TriggerFilterObjectWithRefs> L1SeedFilterToken_;
  float minET_;
  float dRMatch_;
};

template <class T>
MiniAODL1CandProducerV2<T>::MiniAODL1CandProducerV2(const edm::ParameterSet& iConfig ) :
  inputs_(consumes<TRefVector>(iConfig.getParameter<edm::InputTag>("inputs"))),
  //l1IsoObjectsToken_(consumes<l1extra::L1EmParticleCollection>(iConfig.getParameter<edm::InputTag>("isoObjects"))),
  L1SeedFilterToken_(consumes<trigger::TriggerFilterObjectWithRefs>(iConfig.getParameter< edm::InputTag > ("L1SeedFilterTag"))),
  //l1NonIsoObjectsToken_(consumes<l1extra::L1EmParticleCollection>(iConfig.getParameter<edm::InputTag>("nonIsoObjects"))),
  minET_(iConfig.getParameter<double>("minET")),		
  dRMatch_(iConfig.getParameter<double>("dRmatch")) {

  produces<TRefVector>();
}

template <class T>
MiniAODL1CandProducerV2<T>::~MiniAODL1CandProducerV2()
{}

template <class T>
void MiniAODL1CandProducerV2<T>::produce(edm::Event &iEvent, const edm::EventSetup &eventSetup) {

  edm::Handle<TRefVector> inputs;
  edm::Handle<trigger::TriggerFilterObjectWithRefs> L1SeedOutput;

  iEvent.getByToken(inputs_, inputs);
  iEvent.getByToken (L1SeedFilterToken_,L1SeedOutput);

  std::vector<l1t::EGammaRef>  l1EGs;
  L1SeedOutput->getObjects(trigger::TriggerL1EG, l1EGs);


  // Create the output collection
  std::unique_ptr<TRefVector> outColRef(new TRefVector);

  for (size_t i=0; i<inputs->size(); i++) {
    TRef ref = (*inputs)[i];
    int index = -1;

    if (l1OfflineMatching(l1EGs, ref->p4(), dRMatch_, index)) {
      outColRef->push_back(ref);
    }
  }	  

  iEvent.put(std::move(outColRef));
}

template <class T>
bool MiniAODL1CandProducerV2<T>::l1OfflineMatching(const std::vector<l1t::EGammaRef>& l1Objects, 
						 math::XYZTLorentzVector refP4, float dRmin, int& index) {
  
  index = 0;
  for (unsigned int i=0; i<l1Objects.size(); i++){
  //for (auto::const_iterator it=l1Objects.begin(); it != l1Objects.end(); it++) {
    if (l1Objects[i]->pt() < minET_)
      continue;

  //float dR = deltaR(refP4, l1Objects[i]->p4());
  //  if (dR < dRmin)
  //    return true;
    
    index++;
  }

  return false;
}


#endif
