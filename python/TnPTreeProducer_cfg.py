import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
import sys

process = cms.Process("tnpEGM")

###################################################################
## argument line options
###################################################################
varOptions = VarParsing('analysis')
varOptions.register(
    "isMC", True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Compute MC efficiencies"
    )

varOptions.register(
    "doEleID", False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Include tree for photon ID SF"
    )

varOptions.register(
    "doPhoID", False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Include tree for photon ID SF"
    )

varOptions.register(
    "doTrigger", True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Include tree for Trigger SF"
    )

varOptions.register(
    "doRECO", False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Include tree for Reco SF"
    )

varOptions.register(
    "calibEn", False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,

    "use EGM smearer to calibrate photon and electron energy"
    )

varOptions.register(
    "isAOD", False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "switch to run other AOD (for RECO SFs)"
    )

#### HLTname is HLT2 in reHLT samples
varOptions.register(
    "HLTname", "HLT",
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "HLT process name (default HLT)"
    )

varOptions.register(
    "GT","auto",
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Global Tag to be used"
    )



varOptions.parseArguments()


###################################################################
## Define TnP inputs 
###################################################################

options = dict()
options['useAOD']               = cms.bool(varOptions.isAOD)

options['HLTProcessName']       = varOptions.HLTname

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
options['ELECTRON_TAG_CUTS']    = "(abs(-log(tan(superCluster.position.theta/2)))<=2.1) && !(1.4442<=abs(-log(tan(superClusterPosition.theta/2)))<=1.566) && pt >= 30.0"

#options['MAXEVENTS']            = cms.untracked.int32(varOptions.maxEvents) 
options['MAXEVENTS']            = cms.untracked.int32(2000) 
options['DoTrigger']            = cms.bool( varOptions.doTrigger )
options['DoRECO']               = cms.bool( varOptions.doRECO    )
options['DoEleID']              = cms.bool( varOptions.doEleID   )
options['DoPhoID']              = cms.bool( varOptions.doPhoID   )

options['OUTPUTEDMFILENAME']    = 'edmFile.root'
options['DEBUG']                = cms.bool(False)
options['isMC']                 = cms.bool(False)
options['UseCalibEn']           = varOptions.calibEn

if (varOptions.isMC):
    options['isMC']                = cms.bool(True)
    options['OUTPUT_FILE_NAME']    = "TnPTree_mc.root"
    if varOptions.isAOD :  options['OUTPUT_FILE_NAME']    = "TnPTree_mc_aod.root"
#    options['TnPPATHS']            = cms.vstring("HLT*")
#    options['TnPHLTTagFilters']    = cms.vstring()
#    options['TnPHLTProbeFilters']  = cms.vstring()
#    options['HLTFILTERTOMEASURE']  = cms.vstring("")
    options['TnPPATHS']            = cms.vstring("HLT_Ele27_eta2p1_WPTight_Gsf_v*")
    options['TnPHLTTagFilters']    = cms.vstring("hltEle27erWPTightGsfTrackIsoFilter")
    options['TnPHLTProbeFilters']  = cms.vstring()
    options['HLTFILTERTOMEASURE']  = cms.vstring("hltEle27erWPTightGsfTrackIsoFilter")   
    options['GLOBALTAG']           = 'auto:run2_mc'
else:
    options['OUTPUT_FILE_NAME']    = "TnPTree_data.root"
    options['TnPPATHS']            = cms.vstring("HLT_Ele27_eta2p1_WPTight_Gsf_v*")
    options['TnPHLTTagFilters']    = cms.vstring("hltEle27erWPTightGsfTrackIsoFilter")
    options['TnPHLTProbeFilters']  = cms.vstring()
    options['HLTFILTERTOMEASURE']  = cms.vstring("hltEle27erWPTightGsfTrackIsoFilter")
    options['GLOBALTAG']           = 'auto:run2_data'

if varOptions.GT != "auto" :
    options['GLOBALTAG'] = varOptions.GT


###################################################################
## Define input files for test local run
###################################################################
from EgammaAnalysis.TnPTreeProducer.etc.tnpInputTestFiles_cff import filesMiniAOD_23Sep2016 as inputs
if options['useAOD'] : from EgammaAnalysis.TnPTreeProducer.etc.tnpInputTestFiles_cff import filesAOD_23Sep2016 as inputs
    
options['INPUT_FILE_NAME'] = inputs['data']
if varOptions.isMC:  options['INPUT_FILE_NAME'] =  inputs['mc']


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

import EgammaAnalysis.TnPTreeProducer.egmTreesSetup_cff as tnpSetup
tnpSetup.setupTreeMaker(process,options)



###################################################################
## Init and Load
###################################################################
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

process.MessageLogger.cerr.threshold = ''
process.MessageLogger.cerr.FwkReport.reportEvery = 1

process.source = cms.Source("PoolSource",
                            fileNames = options['INPUT_FILE_NAME'],
                            )
process.maxEvents = cms.untracked.PSet( input = options['MAXEVENTS'])

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
import EgammaAnalysis.TnPTreeProducer.egmTreesContent_cff as tnpVars
if options['useAOD']: tnpVars.setupTnPVariablesForAOD()
tnpVars.mcTruthCommonStuff.isMC = cms.bool(varOptions.isMC)

process.tnpEleTrig = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                    tnpVars.CommonStuffForGsfElectronProbe, tnpVars.mcTruthCommonStuff,
                                    tagProbePairs = cms.InputTag("tnpPairingEleHLT"),
                                    probeMatches  = cms.InputTag("genProbeEle"),
                                    allProbes     = cms.InputTag("probeEle"),
                                    flags = cms.PSet(
                                        #passingHLT        = cms.InputTag("probeElePassHLT"),
                                        #passingL1seed = cms.InputTag("probeElePassL1seed"),
                                        passingHLTEle23Ele12leg1   = cms.InputTag("probeElePassHLTEle23Ele12leg1" ),
                                        #passingHLTEle23Ele12leg2   = cms.InputTag("probeElePassHLTEle23Ele12leg2" ),
                                        #passingHLTEle23Ele12DZ   = cms.InputTag("probeElePassHLTEle23Ele12DZ" ),
                                        ),
                                    )

process.tnpEleReco = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                    tnpVars.mcTruthCommonStuff, tnpVars.CommonStuffForSuperClusterProbe, 
                                    tagProbePairs = cms.InputTag("tnpPairingEleRec"),
                                    probeMatches  = cms.InputTag("genProbeSC"),
                                    allProbes     = cms.InputTag("probeSC"),
                                    flags         = cms.PSet(passingRECO   = cms.InputTag("probeSCEle", "superclusters") ),
                                    )

process.tnpEleIDs = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                    tnpVars.mcTruthCommonStuff, tnpVars.CommonStuffForGsfElectronProbe,
                                    tagProbePairs = cms.InputTag("tnpPairingEleIDs"),
                                    probeMatches  = cms.InputTag("genProbeEle"),
                                    allProbes     = cms.InputTag("probeEle"),
                                    flags         = cms.PSet(
                                        passingVeto       = cms.InputTag("probeEleCutBasedVeto"  ),
                                        passingLoose      = cms.InputTag("probeEleCutBasedLoose" ),
                                        passingMedium     = cms.InputTag("probeEleCutBasedMedium"),
                                        passingTight      = cms.InputTag("probeEleCutBasedTight" ),
                                        passingVeto80X    = cms.InputTag("probeEleCutBasedVeto80X"  ),
                                        passingLoose80X   = cms.InputTag("probeEleCutBasedLoose80X" ),
                                        passingMedium80X  = cms.InputTag("probeEleCutBasedMedium80X"),
                                        passingTight80X   = cms.InputTag("probeEleCutBasedTight80X" ),
                                        passingMVA80Xwp90 = cms.InputTag("probeEleMVA80Xwp90" ),
                                        passingMVA80Xwp80 = cms.InputTag("probeEleMVA80Xwp80" ),
                                        )
                                    )

process.tnpPhoIDs = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                    tnpVars.mcTruthCommonStuff, tnpVars.CommonStuffForPhotonProbe,
                                    tagProbePairs = cms.InputTag("tnpPairingPhoIDs"),                                                                                         
                                    probeMatches  = cms.InputTag("genProbePho"),
                                    allProbes     = cms.InputTag("probePho"),
                                    flags         = cms.PSet(
                                        passingLoose      = cms.InputTag("probePhoCutBasedLoose"),
                                        passingMedium     = cms.InputTag("probePhoCutBasedMedium"),
                                        passingTight      = cms.InputTag("probePhoCutBasedTight"),
                                        passingMVA        = cms.InputTag("probePhoMVA"),
                                        # passingLoose80X   = cms.InputTag("probePhoCutBasedLoose80X"),
                                        # passingMedium80X  = cms.InputTag("probePhoCutBasedMedium80X"),
                                        # passingTight80X   = cms.InputTag("probePhoCutBasedTight80X"),
                                        # passingMVA80Xwp90 = cms.InputTag("probePhoMVA80Xwp90"),
                                        # passingMVA80Xwp80 = cms.InputTag("probePhoMVA80Xwp80"),
                                        )
                                    )

## add pass HLT-safe flag, available for miniAOD only
if not options['useAOD'] :
    setattr( process.tnpEleTrig.flags, 'passingHLTsafe', cms.InputTag("probeEleHLTsafe" ) )
    setattr( process.tnpEleIDs.flags , 'passingHLTsafe', cms.InputTag("probeEleHLTsafe" ) )

tnpSetup.customize( process.tnpEleTrig , options )
tnpSetup.customize( process.tnpEleIDs  , options )
tnpSetup.customize( process.tnpPhoIDs  , options )
tnpSetup.customize( process.tnpEleReco , options )


process.tree_sequence = cms.Sequence()
if (options['DoTrigger']): process.tree_sequence *= process.tnpEleTrig
if (options['DoRECO'])   : process.tree_sequence *= process.tnpEleReco
if (options['DoEleID'])  : process.tree_sequence *= process.tnpEleIDs
if (options['DoPhoID'])  : process.tree_sequence *= process.tnpPhoIDs


process.hltGetConditions = cms.EDAnalyzer( "EventSetupRecordDataGetter",
    toGet = cms.VPSet(
    ),
    verbose = cms.untracked.bool( False )
)
process.hltGetRaw = cms.EDAnalyzer( "HLTGetRaw",
    RawDataCollection = cms.InputTag( "rawDataCollector" )
)

process.hltBoolFalse = cms.EDFilter( "HLTBool",
    result = cms.bool( False )
)

process.hltL1sSingleEGtest = cms.EDFilter( "HLTL1TSeed",
    L1SeedsLogicalExpression = cms.string( "L1_SingleEG24 OR L1_SingleEG26 " ),
    L1EGammaInputTag = cms.InputTag( 'hltGtStage2Digis','EGamma' ),
    L1JetInputTag = cms.InputTag( 'hltGtStage2Digis','Jet' ),
    saveTags = cms.bool( True ),
    L1ObjectMapInputTag = cms.InputTag( "hltGtStage2ObjectMap" ),
    L1EtSumInputTag = cms.InputTag( 'hltGtStage2Digis','EtSum' ),
    L1TauInputTag = cms.InputTag( 'hltGtStage2Digis','Tau' ),
    L1MuonInputTag = cms.InputTag( 'hltGtStage2Digis','Muon' ),
    L1GlobalInputTag = cms.InputTag( "hltGtStage2Digis" )
)

process.hltL1sSingleAndDoubleEG = cms.EDFilter( "HLTL1TSeed",
    L1SeedsLogicalExpression = cms.string( "L1_SingleEG24 OR L1_SingleEG26 OR L1_SingleEG30 OR L1_SingleEG32 OR L1_SingleEG34 OR L1_SingleEG36 OR L1_SingleEG38 OR L1_SingleEG40 OR L1_SingleEG42  OR L1_SingleEG45  OR L1_SingleEG50 OR L1_SingleEG34er2p1 OR L1_SingleEG36er2p1 OR L1_SingleEG38er2p1 OR L1_SingleIsoEG24er2p1 OR L1_SingleIsoEG26er2p1 OR L1_SingleIsoEG28er2p1 OR L1_SingleIsoEG30er2p1 OR L1_SingleIsoEG32er2p1 OR L1_SingleIsoEG34er2p1 OR L1_SingleIsoEG36er2p1 OR L1_SingleIsoEG24 OR L1_SingleIsoEG26 OR L1_SingleIsoEG28 OR L1_SingleIsoEG30 OR L1_SingleIsoEG32 OR L1_SingleIsoEG34 OR L1_SingleIsoEG36 OR L1_SingleIsoEG38 OR L1_DoubleEG_18_17 OR L1_DoubleEG_20_18 OR L1_DoubleEG_22_10 OR L1_DoubleEG_22_12 OR L1_DoubleEG_22_12 OR L1_DoubleEG_22_15 OR L1_DoubleEG_23_10 OR L1_DoubleEG_24_17 OR L1_DoubleEG_25_12 OR L1_DoubleEG_25_14" ),
    L1EGammaInputTag = cms.InputTag( 'hltGtStage2Digis','EGamma' ),
    L1JetInputTag = cms.InputTag( 'hltGtStage2Digis','Jet' ),
    saveTags = cms.bool( True ),
    L1ObjectMapInputTag = cms.InputTag( "hltGtStage2ObjectMap" ),
    L1EtSumInputTag = cms.InputTag( 'hltGtStage2Digis','EtSum' ),
    L1TauInputTag = cms.InputTag( 'hltGtStage2Digis','Tau' ),
    L1MuonInputTag = cms.InputTag( 'hltGtStage2Digis','Muon' ),
    L1GlobalInputTag = cms.InputTag( "hltGtStage2Digis" )
)

process.hltEGL1SingleEGOrFilter = cms.EDFilter( "HLTEgammaL1TMatchFilterRegional",
    doIsolated = cms.bool( False ),
    endcap_end = cms.double( 2.65 ),
    region_phi_size = cms.double( 1.044 ),
    saveTags = cms.bool( True ),
    region_eta_size_ecap = cms.double( 1.0 ),
    barrel_end = cms.double( 1.4791 ),
    l1IsolatedTag = cms.InputTag( 'hltGtStage2Digis','EGamma' ),
    candIsolatedTag = cms.InputTag( "hltEgammaCandidates" ),
    l1CenJetsTag = cms.InputTag( 'hltGtStage2Digis','Jet' ),
    region_eta_size = cms.double( 0.522 ),
    L1SeedFilterTag = cms.InputTag( "hltL1sSingleEGtest" ),
    candNonIsolatedTag = cms.InputTag( "" ),
    l1NonIsolatedTag = cms.InputTag( 'hltGtStage2Digis','EGamma' ),
    ncandcut = cms.int32( 1 ),
    l1TausTag = cms.InputTag( 'hltGtStage2Digis','Tau' )
)

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

process.p = cms.Path(
        cms.ignore(process.hltGetConditions) +
        cms.ignore(process.hltGetRaw) +
        cms.ignore(process.hltBoolFalse) +
        cms.ignore(process.hltL1sSingleAndDoubleEG) +
        process.hltFilter         +
        process.cand_sequence     + 
        process.tnpPairs_sequence +
        process.mc_sequence       +
        process.eleVarHelper      +
        process.tree_sequence 
        )

process.TFileService = cms.Service(
    "TFileService", fileName = cms.string(options['OUTPUT_FILE_NAME']),
    closeFileFast = cms.untracked.bool(True)
    )
