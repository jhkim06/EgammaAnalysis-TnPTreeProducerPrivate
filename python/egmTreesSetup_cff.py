import FWCore.ParameterSet.Config as cms


###################################################################################
################  --- TAG AND PROBE collections
###################################################################################
import EgammaAnalysis.TnPTreeProducer.egmGoodParticlesDef_cff as goodPartDef

def setTagsProbes(process, options):

    eleHLTProducer = 'PatElectronTriggerCandProducer'
    #eleHLTProducer = 'PatElectronhltTriggerCandProducer' # for rerun with minoaod
    gamHLTProducer = 'PatPhotonTriggerCandProducer'
    hltObjects     = 'slimmedPatTrigger'
    #hltObjects     = 'hltTriggerSummaryAOD' # for rerun with miniaod
    genParticles   = 'prunedGenParticles'
    SCEleMatcher   = 'PatElectronMatchedCandidateProducer' 
    if (options['useAOD']):
        eleHLTProducer = 'GsfElectronTriggerCandProducer'
        gamHLTProducer = 'PhotonTriggerCandProducer'
        hltObjects     = 'hltTriggerSummaryAOD'
        genParticles   = 'genParticles'
        SCEleMatcher   = 'GsfElectronMatchedCandidateProducer' 
        goodPartDef.setGoodParticlesAOD(  process, options )

    else:
        goodPartDef.setGoodParticlesMiniAOD( process, options )
        
        
    ####################### TAG ELECTRON ############################
    process.tagEle = cms.EDProducer(eleHLTProducer,
                                        filterNames = cms.vstring(options['TnPHLTTagFilters']),
                                        inputs      = cms.InputTag("tagEleCutBasedTight"),
                                        bits        = cms.InputTag('TriggerResults::' + options['HLTProcessName']),
                                        objects     = cms.InputTag(hltObjects),
                                        dR          = cms.double(0.1),
                                        isAND       = cms.bool(True)
                                    )

    ##################### PROBE ELECTRONs ###########################
    process.probeEle             = process.tagEle.clone()
    process.probeEle.inputs      = cms.InputTag("probeEleCutBasedTight94X")
    process.probeEle.filterNames = cms.vstring(options['TnPHLTProbeFilters'])

    ################# PROBE ELECTRONs passHLT #######################
    process.probeElePassHLT              = process.tagEle.clone()
    process.probeElePassHLT.inputs       = cms.InputTag("probeEle")  
    process.probeElePassHLT.isAND        = cms.bool(False)


    #### Ele32WPTight
    l1tFilt_Ele32WPTight = "hltEGL1SingleEGOrFilter"
    l1tEtFilt_Ele32WPTight = "hltEG32L1SingleEGOrEtFilter"

    FilterPre_Ele32WPTight = "hltEle32WPTight"

    process.probeElePassL1TEle32WPTight               = process.probeElePassHLT.clone()
    process.probeElePassL1TEle32WPTight.filterNames   = cms.vstring(l1tFilt_Ele32WPTight)
  
    process.probeElePassL1TEtEle32WPTight               = process.probeElePassHLT.clone()
    process.probeElePassL1TEtEle32WPTight.filterNames   = cms.vstring(l1tEtFilt_Ele32WPTight)

    process.probeElePassHcalIsoEle32WPTight               = process.probeElePassHLT.clone()
    process.probeElePassHcalIsoEle32WPTight.filterNames   = cms.vstring(FilterPre_Ele32WPTight+"HcalIsoFilter")
 
    process.probeElePassPixelMatchEle32WPTight               = process.probeElePassHLT.clone()
    process.probeElePassPixelMatchEle32WPTight.filterNames   = cms.vstring(FilterPre_Ele32WPTight+"PixelMatchFilter")

    process.probeElePassPMS2Ele32WPTight               = process.probeElePassHLT.clone()
    process.probeElePassPMS2Ele32WPTight.filterNames   = cms.vstring(FilterPre_Ele32WPTight+"PMS2Filter")

    process.probeElePassGsfTrackIsoEle32WPTight               = process.probeElePassHLT.clone()
    process.probeElePassGsfTrackIsoEle32WPTight.filterNames   = cms.vstring(FilterPre_Ele32WPTight+"GsfTrackIsoFilter")

    #process.probeElePass_Ele32WPTight               = process.probeElePassHLT.clone()
    #process.probeElePass_Ele32WPTight.filterNames   = cms.vstring(FilterPre_Ele32WPTight+"")

    #### Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v16 or v17
    l1tFilt = "hltEGL1SingleAndDoubleEGOrPairFilter" 

    #### Leg1
    FilterPre = "hltEle23Ele12CaloIdLTrackIdLIsoVL"
    Leg1Post = "Leg1Filter"
    EtLeg1Filter = FilterPre + "Et" + Leg1Post 
    ClusterShapeLeg1Filter = FilterPre + "ClusterShape" + Leg1Post 
    HELeg1Filter = FilterPre + "HE" + Leg1Post 
    EcalIsoLeg1Filter = FilterPre + "EcalIso" + Leg1Post 
    HcalIsoLeg1Filter = FilterPre + "HcalIso" + Leg1Post 
    PixelMatchLeg1Filter = FilterPre + "PixelMatch" + Leg1Post 
    OneOEMinusOneOPLeg1Filter = FilterPre + "OneOEMinusOneOP" + Leg1Post 
    DetaLeg1Filter = FilterPre + "Deta" + Leg1Post 
    DphiLeg1Filter = FilterPre + "Dphi" + Leg1Post 
    TrackIsoLeg1Filter = FilterPre + "TrackIso" + Leg1Post 

    process.probeElePassL1T               = process.probeElePassHLT.clone()
    process.probeElePassL1T.filterNames   = cms.vstring(l1tFilt)

    process.probeElePassEtLeg1               = process.probeElePassHLT.clone()
    process.probeElePassEtLeg1.filterNames   = cms.vstring(EtLeg1Filter)

    process.probeElePassClusterShapeLeg1               = process.probeElePassHLT.clone()
    process.probeElePassClusterShapeLeg1.filterNames   = cms.vstring(ClusterShapeLeg1Filter)

    process.probeElePassHELeg1               = process.probeElePassHLT.clone()
    process.probeElePassHELeg1.filterNames   = cms.vstring(HELeg1Filter)

    process.probeElePassEcalIsoLeg1               = process.probeElePassHLT.clone()
    process.probeElePassEcalIsoLeg1.filterNames   = cms.vstring(EcalIsoLeg1Filter)

    process.probeElePassHcalIsoLeg1               = process.probeElePassHLT.clone()
    process.probeElePassHcalIsoLeg1.filterNames   = cms.vstring(HcalIsoLeg1Filter)

    process.probeElePassPixelMatchLeg1               = process.probeElePassHLT.clone()
    process.probeElePassPixelMatchLeg1.filterNames   = cms.vstring(PixelMatchLeg1Filter)

    process.probeElePassOneOEMinusOneOPLeg1               = process.probeElePassHLT.clone()
    process.probeElePassOneOEMinusOneOPLeg1.filterNames   = cms.vstring(OneOEMinusOneOPLeg1Filter)

    process.probeElePassDetaLeg1               = process.probeElePassHLT.clone()
    process.probeElePassDetaLeg1.filterNames   = cms.vstring(DetaLeg1Filter)

    process.probeElePassDphiLeg1               = process.probeElePassHLT.clone()
    process.probeElePassDphiLeg1.filterNames   = cms.vstring(DphiLeg1Filter)

    process.probeElePassTrackIsoLeg1               = process.probeElePassHLT.clone()
    process.probeElePassTrackIsoLeg1.filterNames   = cms.vstring(TrackIsoLeg1Filter)

    Leg2Post = "Leg2Filter"
    EtLeg2Filter = FilterPre + "Et" + Leg2Post
    ClusterShapeLeg2Filter = FilterPre + "ClusterShape" + Leg2Post
    HELeg2Filter = FilterPre + "HE" + Leg2Post
    EcalIsoLeg2Filter = FilterPre + "EcalIso" + Leg2Post
    HcalIsoLeg2Filter = FilterPre + "HcalIso" + Leg2Post
    PixelMatchLeg2Filter = FilterPre + "PixelMatch" + Leg2Post
    OneOEMinusOneOPLeg2Filter = FilterPre + "OneOEMinusOneOP" + Leg2Post
    DetaLeg2Filter = FilterPre + "Deta" + Leg2Post
    DphiLeg2Filter = FilterPre + "Dphi" + Leg2Post
    TrackIsoLeg2Filter = FilterPre + "TrackIso" + Leg2Post

    process.probeElePassEtLeg2               = process.probeElePassHLT.clone()
    process.probeElePassEtLeg2.filterNames   = cms.vstring(EtLeg2Filter)

    process.probeElePassClusterShapeLeg2               = process.probeElePassHLT.clone()
    process.probeElePassClusterShapeLeg2.filterNames   = cms.vstring(ClusterShapeLeg2Filter)

    process.probeElePassHELeg2               = process.probeElePassHLT.clone()
    process.probeElePassHELeg2.filterNames   = cms.vstring(HELeg2Filter)

    process.probeElePassEcalIsoLeg2               = process.probeElePassHLT.clone()
    process.probeElePassEcalIsoLeg2.filterNames   = cms.vstring(EcalIsoLeg2Filter)

    process.probeElePassHcalIsoLeg2               = process.probeElePassHLT.clone()
    process.probeElePassHcalIsoLeg2.filterNames   = cms.vstring(HcalIsoLeg2Filter)

    process.probeElePassPixelMatchLeg2               = process.probeElePassHLT.clone()
    process.probeElePassPixelMatchLeg2.filterNames   = cms.vstring(PixelMatchLeg2Filter)

    process.probeElePassOneOEMinusOneOPLeg2               = process.probeElePassHLT.clone()
    process.probeElePassOneOEMinusOneOPLeg2.filterNames   = cms.vstring(OneOEMinusOneOPLeg2Filter)

    process.probeElePassDetaLeg2               = process.probeElePassHLT.clone()
    process.probeElePassDetaLeg2.filterNames   = cms.vstring(DetaLeg2Filter)

    process.probeElePassDphiLeg2               = process.probeElePassHLT.clone()
    process.probeElePassDphiLeg2.filterNames   = cms.vstring(DphiLeg2Filter)

    process.probeElePassTrackIsoLeg2               = process.probeElePassHLT.clone()
    process.probeElePassTrackIsoLeg2.filterNames   = cms.vstring(TrackIsoLeg2Filter)


    #### DoubleEle33
    process.probeElePassPMS2UnseededFilterDouble33         = process.probeElePassHLT.clone()
    process.probeElePassPMS2UnseededFilterDouble33.filterNames   = cms.vstring("hltDiEle33CaloIdLMWPMS2UnseededFilter")

    process.probeElePassPMS2SeededFilterDouble33         = process.probeElePassHLT.clone()
    process.probeElePassPMS2SeededFilterDouble33.filterNames   = cms.vstring("hltEle33CaloIdLMWPMS2Filter")

    ### To be adapted for AOD too
    #process.ele27erObj = cms.EDFilter('PATTriggerObjectStandAloneSelector',
    #                                  src = cms.InputTag('selectedPatTrigger'),
    #                                  cut = cms.string('abs(eta) < 2.17')
    #                                  )

    ###################### PROBE PHOTONs ############################
    process.probePho  = cms.EDProducer( gamHLTProducer,
                                        filterNames = options['TnPHLTProbeFilters'],
                                        inputs      = cms.InputTag("goodPhotons"),
                                        bits        = cms.InputTag('TriggerResults::' + options['HLTProcessName'] ),
                                        objects     = cms.InputTag(hltObjects),
                                        dR          = cms.double(0.3),
                                        isAND       = cms.bool(True)
                                        )
    if options['useAOD'] : process.probePho = process.goodPhotons.clone()
    
    ######################### PROBE SCs #############################    
    process.probeSC     = cms.EDProducer("RecoEcalCandidateTriggerCandProducer",
                                            filterNames  = cms.vstring(options['TnPHLTProbeFilters']),
                                             inputs       = cms.InputTag("goodSuperClusters"),
                                             bits         = cms.InputTag('TriggerResults::' + options['HLTProcessName']),
                                             objects      = cms.InputTag(hltObjects),
                                             dR           = cms.double(0.3),
                                             isAND        = cms.bool(True)
                                        )
       
    process.probeSCEle = cms.EDProducer( SCEleMatcher,
                                            src     = cms.InputTag("superClusterCands"),
                                            ReferenceElectronCollection = cms.untracked.InputTag("goodElectrons"),
                                            cut = cms.string(options['SUPERCLUSTER_CUTS'])
                                        )

    ########################## gen tag & probes ######################
    if options['isMC'] :
        cut_gen_standard = 'abs(pdgId) == 11 && pt > 3 && abs(eta) < 2.7 && isPromptFinalState'
        cut_gen_flashgg  = 'abs(pdgId) == 11 && pt > 3 && abs(eta) < 2.7 && ( isPromptFinalState || status == 23)'
        cut_gen_tau      = 'abs(pdgId) == 11 && pt > 3 && abs(eta) < 2.7 && ( isPromptFinalState || isDirectPromptTauDecayProductFinalState) '
        
        process.genEle   = cms.EDFilter( "GenParticleSelector",
                                          src = cms.InputTag(genParticles), 
                                          cut = cms.string(cut_gen_standard),
                                          )

        process.genTagEle = cms.EDProducer("MCMatcher",
                                            src      = cms.InputTag("tagEle"),
                                            matched  = cms.InputTag("genEle"),
                                            mcStatus = cms.vint32(),
                                            mcPdgId  = cms.vint32(),
                                            checkCharge = cms.bool(False),
                                            maxDeltaR   = cms.double(0.20),   # Minimum deltaR for the match
                                            maxDPtRel   = cms.double(50.0),    # Minimum deltaPt/Pt for the match
                                            resolveAmbiguities    = cms.bool(False), # Forbid two RECO objects to match to the same GEN objec
                                            resolveByMatchQuality = cms.bool(True),  # False = just match input in order; True = pick lowest deltaR pair first
                                            )        
        
        process.genProbeEle  = process.genTagEle.clone( src = cms.InputTag("probeEle") )
        process.genProbePho  = process.genTagEle.clone( src = cms.InputTag("probePho") )
        process.genProbeSC   = process.genTagEle.clone( src = cms.InputTag("probeSC")  )
    
        
    ########################### TnP pairs ############################
    masscut = cms.string("50<mass<130")         
    process.tnpPairingEleHLT   = cms.EDProducer("CandViewShallowCloneCombiner",
                                        decay = cms.string("tagEle@+ probeEle@-"), 
                                        checkCharge = cms.bool(True),
                                        cut = masscut,
                                        )
    
    process.tnpPairingEleRec             = process.tnpPairingEleHLT.clone()
    process.tnpPairingEleRec.decay       = cms.string("tagEle probeSC" ) 
    process.tnpPairingEleRec.checkCharge = cms.bool(False)
    
    process.tnpPairingEleIDs             = process.tnpPairingEleHLT.clone()
    process.tnpPairingEleIDs.decay       = cms.string("tagEle probeEle")
    process.tnpPairingEleIDs.checkCharge = cms.bool(False)

    process.tnpPairingPhoIDs             = process.tnpPairingEleHLT.clone()
    process.tnpPairingPhoIDs.decay       = cms.string("tagEle probePho")
    process.tnpPairingPhoIDs.checkCharge = cms.bool(False)

    ######################## probe passing ID ##########################
    import EgammaAnalysis.TnPTreeProducer.egmElectronIDModules_cff as egmEleID
    import EgammaAnalysis.TnPTreeProducer.egmPhotonIDModules_cff   as egmPhoID
    egmEleID.setIDs(process, options)
    egmPhoID.setIDs(process, options)

    
###################################################################################
################  --- SEQUENCES
###################################################################################      
def setSequences(process, options):

    process.init_sequence = cms.Sequence()
    if options['UseCalibEn'] and options['useAOD']:
        process.enCalib_sequence = cms.Sequence(
            process.selectElectronsBase    +
            process.selectPhotonsBase      +
            process.calibratedPatElectrons +
            process.calibratedPatPhotons   
            )
        process.init_sequence += process.enCalib_sequence

    process.sc_sequence  = cms.Sequence( )
    process.ele_sequence = cms.Sequence( )
    process.pho_sequence = cms.Sequence( )
    process.hlt_sequence = cms.Sequence( process.hltFilter )
    
    process.tag_sequence = cms.Sequence(
        process.goodElectrons             +
        process.egmGsfElectronIDSequence  +
        process.tagEleCutBasedTight       +
        process.tagEle 
        )
        
    if options['useAOD'] : process.sc_sequence += process.sc_sequenceAOD
    else :                 process.sc_sequence += process.sc_sequenceMiniAOD
    process.sc_sequence += process.probeSC
    process.sc_sequence += process.probeSCEle

    process.ele_sequence = cms.Sequence(
        process.probeEleCutBasedVeto      +
        process.probeEleCutBasedLoose     +
        process.probeEleCutBasedMedium    +
        process.probeEleCutBasedTight     +
        process.probeEleCutBasedVeto80X   +
        process.probeEleCutBasedLoose80X  +
        process.probeEleCutBasedMedium80X +
        process.probeEleCutBasedTight80X  +
        process.probeEleMVA80Xwp90        +
        process.probeEleMVA80Xwp80        +
        process.probeEleCutBasedVeto94X   +   
        process.probeEleCutBasedLoose94X  +
        process.probeEleCutBasedMedium94X +
        process.probeEleCutBasedTight94X  +
        process.probeEle 
        )
    if not options['useAOD'] : process.ele_sequence += process.probeEleHLTsafe

    process.pho_sequence = cms.Sequence(
        process.goodPhotons               +
        process.egmPhotonIDSequence       +
        process.probePhoCutBasedLoose     +
        process.probePhoCutBasedMedium    +
        process.probePhoCutBasedTight     +
        process.probePhoMVA               +
        #        process.probePhoCutBasedLoose80X  +
        #        process.probePhoCutBasedMedium80X +
        #        process.probePhoCutBasedTight80X  +
        #        process.probePhoMVA80Xwp90       +
        #        process.probePhoMVA80Xwp80       +
        process.probePho                
        )

    process.hlt_sequence = cms.Sequence( 
                                          process.probeElePassL1T                 
                                         + process.probeElePassEtLeg1              
                                         + process.probeElePassClusterShapeLeg1    
                                         + process.probeElePassHELeg1              
                                         + process.probeElePassEcalIsoLeg1         
                                         + process.probeElePassHcalIsoLeg1         
                                         + process.probeElePassPixelMatchLeg1      
                                         + process.probeElePassOneOEMinusOneOPLeg1 
                                         + process.probeElePassDetaLeg1            
                                         + process.probeElePassDphiLeg1            
                                         + process.probeElePassTrackIsoLeg1        

                                         + process.probeElePassEtLeg2
                                         + process.probeElePassClusterShapeLeg2
                                         + process.probeElePassHELeg2
                                         + process.probeElePassEcalIsoLeg2
                                         + process.probeElePassHcalIsoLeg2
                                         + process.probeElePassPixelMatchLeg2
                                         + process.probeElePassOneOEMinusOneOPLeg2
                                         + process.probeElePassDetaLeg2
                                         + process.probeElePassDphiLeg2
                                         + process.probeElePassTrackIsoLeg2

                                         + process.probeElePassPMS2SeededFilterDouble33
                                         + process.probeElePassPMS2UnseededFilterDouble33

                                         #process.probeElePassL1TEle32WPTight        
                                         #+process.probeElePassL1TEtEle32WPTight        
                                         #+process.probeElePassHcalIsoEle32WPTight    
                                         #+process.probeElePassPixelMatchEle32WPTight 
                                         #+process.probeElePassPMS2Ele32WPTight       
                                         #+process.probeElePassGsfTrackIsoEle32WPTight
                                        )

    if options['isMC'] :
        process.tag_sequence += process.genEle + process.genTagEle 
        process.ele_sequence += process.genProbeEle
        process.pho_sequence += process.genProbePho
        process.sc_sequence  += process.genProbeSC

    from EgammaAnalysis.TnPTreeProducer.pileupConfiguration_cfi import pileupProducer
    process.pileupReweightingProducer = pileupProducer.clone()
    if options['useAOD']: process.pileupReweightingProducer.pileupInfoTag = "addPileupInfo"

    process.mc_sequence = cms.Sequence()
    if options['isMC'] : process.mc_sequence = cms.Sequence( process.pileupReweightingProducer )
            
###################################################################################
################  --- tree Maker setup
###################################################################################
def setupTreeMaker(process, options) :
    from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
    process.hltFilter = hltHighLevel.clone()
    process.hltFilter.throw = cms.bool(True)
    process.hltFilter.HLTPaths = options['TnPPATHS']
    process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","",options['HLTProcessName'])
    
    setTagsProbes( process, options )
    setSequences(  process, options )

    
def customize( tnpTree, options ):
    tnpTree.arbitration = cms.string("HighestPt")
    if options['isMC'] :
        tnpTree.isMC = cms.bool( True ) 
        tnpTree.eventWeight = cms.InputTag("generator")
        tnpTree.PUWeightSrc = cms.InputTag("pileupReweightingProducer","pileupWeights")
    else:
        tnpTree.isMC = cms.bool( False ) 
 
