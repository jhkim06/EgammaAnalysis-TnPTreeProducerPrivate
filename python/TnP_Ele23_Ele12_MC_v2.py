import FWCore.ParameterSet.Config as cms

process = cms.Process("tnpEGM")

process.load('FWCore.MessageService.MessageLogger_cfi')

options = dict()
options['useAOD']               = cms.bool( False )

options['HLTProcessName']       = "HLT"

### set input collections
options['ELECTRON_COLL']        = "slimmedElectrons"
options['PHOTON_COLL']          = "slimmedPhotons"
options['SUPERCLUSTER_COLL']    = "reducedEgamma:reducedSuperClusters" ### not used in AOD
if options['useAOD']:
    options['ELECTRON_COLL']    = "gedGsfElectrons"
    options['PHOTON_COLL'  ]    = "gedPhotons"

options['ELECTRON_CUTS']        = "ecalEnergy*sin(superClusterPosition.theta)>5.0 &&  (abs(-log(tan(superClusterPosition.theta/2)))<2.5)"
options['SUPERCLUSTER_CUTS']    = "abs(eta)<2.5 &&  et>5.0"
options['PHOTON_CUTS']          = "(abs(-log(tan(superCluster.position.theta/2)))<=2.5) && pt> 10"
options['ELECTRON_TAG_CUTS']    = "(abs(-log(tan(superCluster.position.theta/2)))<=2.1) && !(1.4442<=abs(-log(tan(superClusterPosition.theta/2)))<=1.566) && pt >= 35.0"

options['DoTrigger']            = cms.bool( True )
options['DoRECO']               = cms.bool( False )
options['DoEleID']              = cms.bool( False )
options['DoPhoID']              = cms.bool( False )

options['OUTPUT_FILE_NAME']     = 'tnp_data.root'
options['OUTPUTEDMFILENAME']    = 'edmFile.root'
options['DEBUG']                = cms.bool(False)
options['isMC']                 = cms.bool(True)
options['UseCalibEn']           = cms.bool(False)

options['addSUSY']               = cms.bool(False)
if options['useAOD']:
    options['addSUSY']               = cms.bool(False)

if options['isMC']:
    options['TnPPATHS']            = cms.vstring("HLT_Ele35_WPTight_Gsf_v7")
    options['TnPHLTTagFilters']    = cms.vstring("hltEle35noerWPTightGsfTrackIsoFilter")
    options['TnPHLTProbeFilters']  = cms.vstring("")
    options['HLTFILTERTOMEASURE']  = cms.vstring("")
    options['GLOBALTAG']           = '94X_mc2017_realistic_v10'
else:
    options['TnPPATHS']            = cms.vstring("HLT_Ele35_WPTight_Gsf_v*")
    options['TnPHLTTagFilters']    = cms.vstring("hltEle35noerWPTightGsfTrackIsoFilter")
    options['TnPHLTProbeFilters']  = cms.vstring("")
    options['HLTFILTERTOMEASURE']  = cms.vstring("")
    #options['GLOBALTAG']           = '92X_dataRun2_HLT_v7'
    options['GLOBALTAG']           = '94X_dataRun2_ReReco_EOY17_v2'

import EgammaAnalysis.TnPTreeProducer.egmTreesSetup_cff as tnpSetup
tnpSetup.setupTreeMaker(process,options)

###################################################################
## Init and Load
###################################################################
process.MessageLogger.cerr.threshold = ''
process.MessageLogger.cerr.FwkReport.reportEvery = 1

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
     'root://cms-xrd-global.cern.ch//store/mc/RunIIFall17MiniAOD/ZToEE_NNPDF31_13TeV-powheg_M_50_120/MINIAODSIM/94X_mc2017_realistic_v10-v2/20000/06E355FC-F70F-E811-9951-0CC47A706FF8.root'),
)

# limit the number of events to be processed
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(5000)
)

if options['DoTrigger'] : print "  -- Producing HLT (trigger ele) efficiency tree -- "
if options['DoRECO']    : print "  -- Producing RECO SF tree        -- "
if options['DoEleID']   : print "  -- Producing electron SF tree    -- "
if options['DoPhoID']   : print "  -- Producing photon SF tree      -- "

###################################################################
## Define sequences and TnP pairs
###################################################################
process.cand_sequence = cms.Sequence( process.init_sequence + process.tag_sequence )
if options['DoEleID'] or options['DoTrigger'] : process.cand_sequence += process.ele_sequence
if options['DoPhoID']                         : process.cand_sequence += process.pho_sequence
if options['DoTrigger']                       : process.cand_sequence += process.hlt_sequence
if options['DoRECO']                          : process.cand_sequence += process.sc_sequence

process.tnpPairs_sequence = cms.Sequence()
if options['DoTrigger'] : process.tnpPairs_sequence *= process.tnpPairingEleHLT
if options['DoRECO']    : process.tnpPairs_sequence *= process.tnpPairingEleRec
if options['DoEleID']   : process.tnpPairs_sequence *= process.tnpPairingEleIDs
if options['DoPhoID']   : process.tnpPairs_sequence *= process.tnpPairingPhoIDs

##########################################################################
## TnP Trees
##########################################################################

###################################################################
## import TnP tree maker pythons and configure for AODs
###################################################################
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
#process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, options['GLOBALTAG'] , '')


import EgammaAnalysis.TnPTreeProducer.egmTreesContent_cff as tnpVars
if options['useAOD']: tnpVars.setupTnPVariablesForAOD()
tnpVars.mcTruthCommonStuff.isMC = options['isMC']

process.tnpEleTrig = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                    tnpVars.CommonStuffForGsfElectronProbe, tnpVars.mcTruthCommonStuff,
                                    tagProbePairs = cms.InputTag("tnpPairingEleHLT"),
                                    probeMatches  = cms.InputTag("genProbeEle"),
                                    allProbes     = cms.InputTag("probeEle"),
                                    flags = cms.PSet(
                                        passHLT        = cms.InputTag("probeElePassHLT"),

                                        passL1T        = cms.InputTag("probeElePassL1T"),
                                        passEtLeg1        = cms.InputTag("probeElePassEtLeg1"),
                                        passClusterShapeLeg1        = cms.InputTag("probeElePassClusterShapeLeg1"),
                                        passHELeg1        = cms.InputTag("probeElePassHELeg1"),
                                        passEcalIsoLeg1        = cms.InputTag("probeElePassHcalIsoLeg1"),
                                        passPixelMatchLeg1        = cms.InputTag("probeElePassPixelMatchLeg1"),
                                        passOneOEMinusOneOPLeg1        = cms.InputTag("probeElePassOneOEMinusOneOPLeg1"),
                                        passDetaLeg1        = cms.InputTag("probeElePassDetaLeg1"),
                                        passDphiLeg1        = cms.InputTag("probeElePassDphiLeg1"),
                                        passTrackIsoLeg1        = cms.InputTag("probeElePassTrackIsoLeg1"),

                                        passEtLeg2        = cms.InputTag("probeElePassEtLeg2"),
                                        passClusterShapeLeg2        = cms.InputTag("probeElePassClusterShapeLeg2"),
                                        passHELeg2        = cms.InputTag("probeElePassHELeg2"),
                                        passEcalIsoLeg2        = cms.InputTag("probeElePassHcalIsoLeg2"),
                                        passPixelMatchLeg2        = cms.InputTag("probeElePassPixelMatchLeg2"),
                                        passOneOEMinusOneOPLeg2        = cms.InputTag("probeElePassOneOEMinusOneOPLeg2"),
                                        passDetaLeg2        = cms.InputTag("probeElePassDetaLeg2"),
                                        passDphiLeg2        = cms.InputTag("probeElePassDphiLeg2"),
                                        passTrackIsoLeg2        = cms.InputTag("probeElePassTrackIsoLeg2"),

                                        ),
                                    )


process.tnpEleReco = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                    tnpVars.mcTruthCommonStuff, tnpVars.CommonStuffForSuperClusterProbe,
                                    tagProbePairs = cms.InputTag("tnpPairingEleRec"),
                                    probeMatches  = cms.InputTag("genProbeSC"),
                                    allProbes     = cms.InputTag("probeSC"),
                                    flags         = cms.PSet(passRECO   = cms.InputTag("probeSCEle", "superclusters") ),
                                    )

process.tnpEleIDs = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                    tnpVars.mcTruthCommonStuff, tnpVars.CommonStuffForGsfElectronProbe,
                                    tagProbePairs = cms.InputTag("tnpPairingEleIDs"),
                                    probeMatches  = cms.InputTag("genProbeEle"),
                                    allProbes     = cms.InputTag("probeEle"),
                                    flags         = cms.PSet(
                                        passVeto       = cms.InputTag("probeEleCutBasedVeto"  ),
                                        passLoose      = cms.InputTag("probeEleCutBasedLoose" ),
                                        passMedium     = cms.InputTag("probeEleCutBasedMedium"),
                                        passTight      = cms.InputTag("probeEleCutBasedTight" ),
                                        passVeto80X    = cms.InputTag("probeEleCutBasedVeto80X"  ),
                                        passLoose80X   = cms.InputTag("probeEleCutBasedLoose80X" ),
                                        passMedium80X  = cms.InputTag("probeEleCutBasedMedium80X"),
                                        passTight80X   = cms.InputTag("probeEleCutBasedTight80X" ),
                                        passMVA80Xwp90 = cms.InputTag("probeEleMVA80Xwp90" ),
                                        passMVA80Xwp80 = cms.InputTag("probeEleMVA80Xwp80" ),
                                        )
                                    )


process.tnpPhoIDs = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                    tnpVars.mcTruthCommonStuff, tnpVars.CommonStuffForPhotonProbe,
                                    tagProbePairs = cms.InputTag("tnpPairingPhoIDs"),
                                    probeMatches  = cms.InputTag("genProbePho"),
                                    allProbes     = cms.InputTag("probePho"),
                                    flags         = cms.PSet(
                                        passLoose      = cms.InputTag("probePhoCutBasedLoose"),
                                        passMedium     = cms.InputTag("probePhoCutBasedMedium"),
                                        passTight      = cms.InputTag("probePhoCutBasedTight"),
                                        passMVA        = cms.InputTag("probePhoMVA"),
                                        # passLoose80X   = cms.InputTag("probePhoCutBasedLoose80X"),
                                        # passMedium80X  = cms.InputTag("probePhoCutBasedMedium80X"),
                                        # passTight80X   = cms.InputTag("probePhoCutBasedTight80X"),
                                        # passMVA80Xwp90 = cms.InputTag("probePhoMVA80Xwp90"),
                                        # passMVA80Xwp80 = cms.InputTag("probePhoMVA80Xwp80"),
                                        )
                                    )

## add pass HLT-safe flag, available for miniAOD only
if not options['useAOD'] :
    setattr( process.tnpEleTrig.flags, 'passHLTsafe', cms.InputTag("probeEleHLTsafe" ) )
    setattr( process.tnpEleIDs.flags , 'passHLTsafe', cms.InputTag("probeEleHLTsafe" ) )

tnpSetup.customize( process.tnpEleTrig , options )
tnpSetup.customize( process.tnpEleIDs  , options )
tnpSetup.customize( process.tnpPhoIDs  , options )
tnpSetup.customize( process.tnpEleReco , options )

process.tree_sequence = cms.Sequence()
if (options['DoTrigger']): process.tree_sequence *= process.tnpEleTrig
if (options['DoRECO'])   : process.tree_sequence *= process.tnpEleReco
if (options['DoEleID'])  : process.tree_sequence *= process.tnpEleIDs
if (options['DoPhoID'])  : process.tree_sequence *= process.tnpPhoIDs

##########################################################################
## PATHS
##########################################################################
process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string(options['OUTPUTEDMFILENAME']),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("p"))
                               )
process.outpath = cms.EndPath(process.out)
if (not options['DEBUG']):
    process.outpath.remove(process.out)



process.tnp = cms.Path(
#        process.hltFilter         +
        process.cand_sequence     +
        process.tnpPairs_sequence +
        process.mc_sequence       +
        #process.eleVarHelper      +
        #process.hltVarHelper      +
        process.tree_sequence
        )


process.TFileService = cms.Service(
    "TFileService", fileName = cms.string(options['OUTPUT_FILE_NAME']),
    closeFileFast = cms.untracked.bool(True)
    )

process.sched = cms.Schedule( process.tnp )

