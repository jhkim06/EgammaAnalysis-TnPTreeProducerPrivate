import FWCore.ParameterSet.Config as cms



def calibrateEGM(process, options ):
    process.selectElectronsBase = cms.EDFilter("PATElectronSelector",
                                               src = cms.InputTag( options['ELECTRON_COLL'] ),
                                               cut = cms.string(options['ELECTRON_CUTS']),
                                               filter = cms.bool(True),
                                               )

    process.selectPhotonsBase   = cms.EDFilter("PATPhotonSelector",
                                               src = cms.InputTag( options['PHOTON_COLL'] ),
                                               cut = cms.string(options['PHOTON_CUTS']),
                                               filter = cms.bool(True),
                                               )


    process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
                                                       calibratedPatElectrons  = cms.PSet( initialSeed = cms.untracked.uint32(81),
                                                                                           engineName = cms.untracked.string('TRandom3'),
                                                                                           ),
                                                       calibratedPatPhotons    = cms.PSet( initialSeed = cms.untracked.uint32(81),
                                                                                           engineName = cms.untracked.string('TRandom3'),
                                                                                           ),
                                                       )
    process.load('EgammaAnalysis.ElectronTools.calibratedElectronsRun2_cfi')
    process.load('EgammaAnalysis.ElectronTools.calibratedPhotonsRun2_cfi')


    process.calibratedPatElectrons.electrons = cms.InputTag('selectElectronsBase')
    process.calibratedPatPhotons.photons     = cms.InputTag('selectPhotonsBase')
    if options['isMC']:
        process.calibratedPatElectrons.isMC = cms.bool(True)
        process.calibratedPatPhotons.isMC   = cms.bool(True)

    ### change the input collection to be the calibrated energy one for all other modules from now on
    options['ELECTRON_COLL'] = 'calibratedPatElectrons'
    options['PHOTON_COLL']   = 'calibratedPatPhotons'

###################################################################################
################  --- GOOD particles MiniAOD
################################################################################### 
def setGoodParticlesMiniAOD(process, options):

    ### need rerun ?
    process.eleVarHelper = cms.EDProducer("PatElectronVariableHelper",
                                          probes      = cms.InputTag(options['ELECTRON_COLL']),
                                          vertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices"),
                                          #l1EGColl    = cms.InputTag("caloStage2Digis:EGamma"),
                                          l1EGColl    = cms.InputTag("hltGtStage2Digis:EGamma"),
                                          #pfCandColl  = cms.InputTag("particleFlow"),
                                          )

    ### Needs to rerun HLT menu to work
    process.hltVarHelper = cms.EDProducer("PatElectronHLTVariableHelper",
                                          probes = cms.InputTag(options['ELECTRON_COLL']),
                                          hltCandidateCollection = cms.InputTag("hltEgammaCandidates"),
                                          rhoInputTag = cms.InputTag("hltFixedGridRhoFastjetAllCaloForMuons"),
                                          mapOutputNames = cms.vstring("hltsieie",
                                                                       "hltecaliso",
                                                                       "hlthcaliso",
                                                                       "hlthoe",
                                                                       "hlttkiso",
                                                                       "hltps2",
                                                                       "hltdeta",
                                                                       "hltdetaseed",
                                                                       "hltdphi",
                                                                       "hlteop",
                                                                       "hltchi2",
                                                                       "hltmishits"),
                                          mapInputTags = cms.VInputTag("hltEgammaClusterShape:sigmaIEtaIEta5x5",
                                                                       "hltEgammaEcalPFClusterIso",
                                                                       "hltEgammaHcalPFClusterIso",
                                                                       "hltEgammaHoverE", 
                                                                       "hltEgammaEleGsfTrackIso",
                                                                       "hltEgammaPixelMatchVars:s2",
                                                                       "hltEgammaGsfTrackVars:Deta",
                                                                       "hltEgammaGsfTrackVars:DetaSeed",
                                                                       "hltEgammaGsfTrackVars:Dphi",
                                                                       "hltEgammaGsfTrackVars:OneOESuperMinusOneOP",
                                                                       "hltEgammaGsfTrackVars:Chi2",
                                                                       "hltEgammaGsfTrackVars:MissingHits")
                                          )

    if options['UseCalibEn']:  calibrateEGM( process, options )
        
    ####################  Electron collection
    process.goodElectrons = cms.EDFilter("PATElectronRefSelector",
                                         src = cms.InputTag( options['ELECTRON_COLL'] ),
                                         cut = cms.string(   options['ELECTRON_CUTS'] )
                                         )
    
    ####################  Photon collection
    process.goodPhotons   =  cms.EDFilter("PATPhotonRefSelector",
                                            src = cms.InputTag( options['PHOTON_COLL'] ),
                                            cut = cms.string(   options['PHOTON_CUTS'] )
                                            )

    
    #################### SUPERCLUSTER collections                                                                 
    process.superClusterCands = cms.EDProducer("ConcreteEcalCandidateProducer",
                                               src = cms.InputTag(options['SUPERCLUSTER_COLL']),
                                               particleType = cms.int32(11),
                                               )
    
    process.goodSuperClusters = cms.EDFilter("RecoEcalCandidateRefSelector",
                                             src = cms.InputTag("superClusterCands"),
                                             cut = cms.string(options['SUPERCLUSTER_CUTS']),
                                             filter = cms.bool(True)
                                             )


    process.sc_sequenceMiniAOD = cms.Sequence(
        process.superClusterCands +
        process.goodSuperClusters 
        )
    
###################################################################################
################  --- GOOD particles AOD
################################################################################### 
def setGoodParticlesAOD(process, options):


    process.eleVarHelper = cms.EDProducer("GsfElectronVariableHelper",
                                          probes      = cms.InputTag(options['ELECTRON_COLL']),
                                          vertexCollection = cms.InputTag("offlinePrimaryVertices"),
                                          #l1EGColl    = cms.InputTag("caloStage2Digis:EGamma"),
                                          l1EGColl    = cms.InputTag("hltGtStage2Digis:EGamma"),
                                          #pfCandColl  = cms.InputTag("particleFlow"),
                                          )

    ### Needs to rerun HLT menu to work
    process.hltVarHelper = cms.EDProducer("GsfElectronHLTVariableHelper",
                                          probes = cms.InputTag(options['ELECTRON_COLL']),
                                          hltCandidateCollection = cms.InputTag("hltEgammaCandidates"),
                                          rhoInputTag = cms.InputTag("hltFixedGridRhoFastjetAllCaloForMuons"),
                                          mapOutputNames = cms.vstring("hltsieie",
                                                                       "hltecaliso",
                                                                       "hlthcaliso",
                                                                       "hlthoe",
                                                                       "hlttkiso",
                                                                       "hltps2",
                                                                       "hltdeta",
                                                                       "hltdetaseed",
                                                                       "hltdphi",
                                                                       "hlteop",
                                                                       "hltchi2",
                                                                       "hltmishits"),
                                          mapInputTags = cms.VInputTag("hltEgammaClusterShape:sigmaIEtaIEta5x5",
                                                                       "hltEgammaEcalPFClusterIso",
                                                                       "hltEgammaHcalPFClusterIso",
                                                                       "hltEgammaHoverE", 
                                                                       "hltEgammaEleGsfTrackIso",
                                                                       "hltEgammaPixelMatchVars:s2",
                                                                       "hltEgammaGsfTrackVars:Deta",
                                                                       "hltEgammaGsfTrackVars:DetaSeed",
                                                                       "hltEgammaGsfTrackVars:Dphi",
                                                                       "hltEgammaGsfTrackVars:OneOESuperMinusOneOP",
                                                                       "hltEgammaGsfTrackVars:Chi2",
                                                                       "hltEgammaGsfTrackVars:MissingHits")
                                          )

    ####################  Electron collection
    process.goodElectrons = cms.EDFilter("GsfElectronRefSelector",
                                         src = cms.InputTag(options['ELECTRON_COLL']),
                                         cut = cms.string(options['ELECTRON_CUTS'])
                                         )

    ####################  Photon collection
    ### dummy in AOD (use miniAOD for photons)
    process.goodPhotons    =  cms.EDFilter("PhotonRefSelector",
                                            src = cms.InputTag( options['PHOTON_COLL'] ),
                                            cut = cms.string(   options['PHOTON_CUTS'] )
                                            )
    
    #################### SUPERCLUSTER collections                                                                 
    process.superClusterMerger =  cms.EDProducer("EgammaSuperClusterMerger",
                                                 src = cms.VInputTag(cms.InputTag("particleFlowSuperClusterECAL:particleFlowSuperClusterECALBarrel"),
                                                                     cms.InputTag("particleFlowSuperClusterECAL:particleFlowSuperClusterECALEndcapWithPreshower"),
#                                                                     cms.InputTag("particleFlowEGamma"),
                                                                     ),
                                                 )
    
    
    process.superClusterCands = cms.EDProducer("ConcreteEcalCandidateProducer",
                                               src = cms.InputTag("superClusterMerger"),
                                               particleType = cms.int32(11),
                                               )
    
    process.goodSuperClusters = cms.EDFilter("RecoEcalCandidateRefSelector",
                                             src = cms.InputTag("superClusterCands"),
                                             cut = cms.string(options['SUPERCLUSTER_CUTS']),
                                             filter = cms.bool(True)
                                             )


    process.recoEcalCandidateHelper = cms.EDProducer("RecoEcalCandidateVariableHelper",
                                                     probes = cms.InputTag("superClusterCands"),
                                                     countTracks = cms.bool( False ),
                                                     trkIsoPtMin = cms.double( 0.5 ),
                                                     trkIsoStripEndcap = cms.double( 0.03 ),
                                                     trackProducer = cms.InputTag( "generalTracks" ),
                                                     trkIsoStripBarrel = cms.double( 0.03 ),
                                                     trkIsoConeSize = cms.double( 0.4 ),
                                                     trkIsoVetoConeSize = cms.double( 0.06 ),
                                                     trkIsoRSpan = cms.double( 999999.0 ),
                                                     trkIsoZSpan = cms.double( 999999. )
                                                     )
    process.sc_sequenceAOD = cms.Sequence(
        process.superClusterMerger      +
        process.superClusterCands       +
        process.recoEcalCandidateHelper +
        process.goodSuperClusters     
        )
