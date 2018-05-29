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

options['OUTPUTEDMFILENAME']    = 'edmFile.root'
options['DEBUG']                = cms.bool(False)
options['isMC']                 = cms.bool(True)
options['UseCalibEn']           = cms.bool(False)

options['addSUSY']               = cms.bool(False)
if options['useAOD']:
    options['addSUSY']               = cms.bool(False)

if options['isMC']:
    options['OUTPUT_FILE_NAME']     = 'tnp_mc.root'
    options['TnPPATHS']            = cms.vstring("HLT_Ele35_WPTight_Gsf_v*")
    options['TnPHLTTagFilters']    = cms.vstring("hltEle35noerWPTightGsfTrackIsoFilter")
    options['TnPHLTProbeFilters']  = cms.vstring()
    options['HLTFILTERTOMEASURE']  = cms.vstring()
    options['GLOBALTAG']           = '100X_upgrade2018_realistic_v10'
else:
    options['OUTPUT_FILE_NAME']     = 'tnp_data.root'
    options['TnPPATHS']            = cms.vstring("HLT_Ele35_WPTight_Gsf_v*")
    options['TnPHLTTagFilters']    = cms.vstring("hltEle35noerWPTightGsfTrackIsoFilter")
    options['TnPHLTProbeFilters']  = cms.vstring()
    options['HLTFILTERTOMEASURE']  = cms.vstring()
    options['GLOBALTAG']           = '101X_dataRun2_Prompt_v9'

import EgammaAnalysis.TnPTreeProducer.egmTreesSetup_cff as tnpSetup
tnpSetup.setupTreeMaker(process,options)

###################################################################
## Init and Load
###################################################################
process.MessageLogger.cerr.threshold = ''
process.MessageLogger.cerr.FwkReport.reportEvery = 1

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
                                      #'root://cms-xrd-global.cern.ch//store/data/Run2018A/EGamma/MINIAOD/PromptReco-v1/000/315/488/00000/00ADBC28-B74E-E811-829C-FA163EE52637.root',
                                      #'root://cms-xrd-global.cern.ch//store/data/Run2018A/EGamma/MINIAOD/PromptReco-v1/000/315/488/00000/020847B9-DA4E-E811-AF5B-FA163EA984DF.root',
                                      'root://cms-xrd-global.cern.ch//store/mc/RunIISpring18MiniAOD/DYToEE_M-50_NNPDF31_13TeV-powheg-pythia8/MINIAODSIM/100X_upgrade2018_realistic_v10-v1/60000/40B6A18F-482D-E811-8552-EC0D9A0B3180.root',
  ),
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
                                        passHcalIsoLeg1        = cms.InputTag("probeElePassHcalIsoLeg1"),
                                        passPixelMatchLeg1        = cms.InputTag("probeElePassPixelMatchLeg1"),
                                        passTrackIsoLeg1        = cms.InputTag("probeElePassTrackIsoLeg1"),

                                        passHcalIsoLeg2        = cms.InputTag("probeElePassHcalIsoLeg2"),
                                        passPixelMatchLeg2        = cms.InputTag("probeElePassPixelMatchLeg2"),
                                        passTrackIsoLeg2        = cms.InputTag("probeElePassTrackIsoLeg2"),

                                        passPMS2SeededFilterDouble33 = cms.InputTag("probeElePassPMS2SeededFilterDouble33"),
                                        passPMS2UnseededFilterDouble33 = cms.InputTag("probeElePassPMS2UnseededFilterDouble33"),

                                        ),
                                    )

## add pass HLT-safe flag, available for miniAOD only
if not options['useAOD'] :
    setattr( process.tnpEleTrig.flags, 'passHLTsafe', cms.InputTag("probeEleHLTsafe" ) )

tnpSetup.customize( process.tnpEleTrig , options )

process.tree_sequence = cms.Sequence()
if (options['DoTrigger']): process.tree_sequence *= process.tnpEleTrig

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
#       process.hltFilter         +
        process.cand_sequence     +
        process.tnpPairs_sequence +
        process.mc_sequence       +
        process.eleVarHelper      +
        #process.hltVarHelper      +
        process.tree_sequence
        )


process.TFileService = cms.Service(
    "TFileService", fileName = cms.string(options['OUTPUT_FILE_NAME']),
    closeFileFast = cms.untracked.bool(True)
    )

process.sched = cms.Schedule( process.tnp )

