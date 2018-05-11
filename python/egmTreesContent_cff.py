import FWCore.ParameterSet.Config as cms

##########################################################################
## TREE CONTENT
#########################################################################
    
ZVariablesToStore = cms.PSet(
    eta = cms.string("eta"),
    abseta = cms.string("abs(eta)"),
    pt  = cms.string("pt"),
    mass  = cms.string("mass"),
    )   

SCProbeVariablesToStore = cms.PSet(
    sc_eta    = cms.string("eta"),
    sc_abseta = cms.string("abs(eta)"),
    sc_pt     = cms.string("pt"),
    sc_et     = cms.string("et"),
    sc_e      = cms.string("energy"),
    sc_tkIso  = cms.InputTag("recoEcalCandidateHelper:scTkIso"),
    )

EleProbeVariablesToStore = cms.PSet(
    probe_ele_eta       = cms.string("eta"),
    probe_ele_phi       = cms.string("phi"),
    probe_ele_abseta    = cms.string("abs(eta)"),
    probe_ele_pt        = cms.string("pt"),
    probe_ele_et        = cms.string("et"),
    probe_ele_e         = cms.string("energy"),
    probe_ele_q         = cms.string("charge"),

    ## super cluster quantities
    probe_sc_e          = cms.string("superCluster.energy"),
    probe_sc_eRaw       = cms.string("superCluster.rawEnergy"),
    probe_sc_ePres      = cms.string("superCluster.preshowerEnergy"),
    probe_sc_et         = cms.string("superCluster.energy*sin(superClusterPosition.theta)"),    
    #probe_sc_eta        = cms.string("superCluster.eta"),
    probe_sc_eta        = cms.string("-log(tan(superCluster.position.theta/2))"),
    #probe_sc_abseta     = cms.string("abs(superCluster.eta)"),
    probe_sc_abseta     = cms.string("abs(-log(tan(superCluster.position.theta/2)))"),
    probe_sc_etaW       = cms.string("superCluster.etaWidth"),
    probe_sc_phi        = cms.string("superCluster.phi"),
    probe_sc_phiW       = cms.string("superCluster.phiWidth"),

    ## id based
    probe_ele_dEtaIn    = cms.string("deltaEtaSuperClusterTrackAtVtx"),
    #probe_ele_dEtaOut   = cms.string("deltaEtaSuperClusterTrackAtVtx + superCluster.eta -superCluster.seed.position.eta"),
    probe_ele_dEtaOut   = cms.string("deltaEtaSuperClusterTrackAtVtx+log(tan(superCluster.position.theta/2))-log(tan(superCluster.seed.position.theta/2))"),
    probe_ele_dPhiIn    = cms.string("deltaPhiSuperClusterTrackAtVtx"),
    probe_ele_e1x5      = cms.string("e1x5"),
    probe_ele_e2x5      = cms.string("e2x5Max"),
    probe_ele_e5x5      = cms.string("e5x5"),
    probe_ele_r9        = cms.string("r9"),
    probe_ele_r9_5      = cms.string("full5x5_r9"),
    probe_ele_sieie     = cms.string("sigmaIetaIeta"),
    probe_ele_sieie5x5  = cms.string("full5x5_sigmaIetaIeta"),
    probe_ele_hoe       = cms.string("hadronicOverEm"),
    probe_ele_ooemoop   = cms.string("(1.0/ecalEnergy - eSuperClusterOverP/ecalEnergy)"),
    #probe_ele_chi2      = cms.InputTag("eleVarHelper:chi2"),
    #probe_ele_mHits     = cms.InputTag("eleVarHelper:missinghits"),
    #probe_ele_dz        = cms.InputTag("eleVarHelper:dz"),
    #probe_ele_dxy       = cms.InputTag("eleVarHelper:dxy"),
    probe_ele_mvaNTr    = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values"),
    probe_ele_mvaTr     = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15Trig25nsV1Values"),

    #isolation
    probe_ele_chIso     = cms.string("pfIsolationVariables().sumChargedHadronPt"),
    probe_ele_phoIso    = cms.string("pfIsolationVariables().sumPhotonEt"),
    probe_ele_neuIso    = cms.string("pfIsolationVariables().sumNeutralHadronEt"),
    probe_ele_ecalIso   = cms.string("ecalPFClusterIso"),
    probe_ele_hcalIso   = cms.string("hcalPFClusterIso"),
    probe_ele_trkIso    = cms.string("trackIso"),
    probe_ele_trkSum03  = cms.string("dr03TkSumPt"),

    # tracker
    probe_ele_trkPt     = cms.string("gsfTrack().ptMode"),

    # L1 info
    probe_l1_e          = cms.InputTag("eleVarHelper:l1e"),
    probe_l1_et         = cms.InputTag("eleVarHelper:l1et"),
    probe_l1_eta        = cms.InputTag("eleVarHelper:l1eta"),
    probe_l1_phi        = cms.InputTag("eleVarHelper:l1phi"),

    ## HLT info
    #hlt_rho            = cms.InputTag("hltVarHelper:hltrho"),
    #probe_hlt_e        = cms.InputTag("hltVarHelper:hlte"),
    #probe_hlt_et       = cms.InputTag("hltVarHelper:hltet"),
    #probe_hlt_eta      = cms.InputTag("hltVarHelper:hlteta"),
    #probe_hlt_phi      = cms.InputTag("hltVarHelper:hltphi"),
    #probe_hlt_sieie    = cms.InputTag("hltVarHelper:hltsieie"),
    #probe_hlt_hoe      = cms.InputTag("hltVarHelper:hlthoe"),
    #probe_hlt_ecalIso  = cms.InputTag("hltVarHelper:hltecaliso"),
    #probe_hlt_hcalIso  = cms.InputTag("hltVarHelper:hlthcaliso"),
    #probe_hlt_ps2      = cms.InputTag("hltVarHelper:hltps2"),
    #probe_hlt_ooemoop  = cms.InputTag("hltVarHelper:hlteop"),
    #probe_hlt_mHits    = cms.InputTag("hltVarHelper:hltmishits"),
    #probe_hlt_chi2     = cms.InputTag("hltVarHelper:hltchi2"),
    #probe_hlt_dEtaOut  = cms.InputTag("hltVarHelper:hltdetaseed"),
    #probe_hlt_dEtaIn   = cms.InputTag("hltVarHelper:hltdeta"),
    #probe_hlt_dPhiIn   = cms.InputTag("hltVarHelper:hltdphi"),
    #probe_hlt_trkIso   = cms.InputTag("hltVarHelper:hlttkiso"),
    
    )

PhoProbeVariablesToStore = cms.PSet(
    ph_eta    = cms.string("eta"),
    ph_abseta = cms.string("abs(eta)"),
    ph_et     = cms.string("et"),
    ph_e      = cms.string("energy"),

## super cluster quantities
    ph_sc_energy = cms.string("superCluster.energy"),
    ph_sc_et     = cms.string("superCluster.energy*sin(superCluster.position.theta)"),    
    ph_sc_eta    = cms.string("-log(tan(superCluster.position.theta/2))"),
    phsc_abseta = cms.string("abs(-log(tan(superCluster.position.theta/2)))"),


#id based
    ph_full5x5x_r9   = cms.string("full5x5_r9"),
    ph_r9            = cms.string("r9"),
    ph_sieie         = cms.string("full5x5_sigmaIetaIeta"),
    ph_sieip         = cms.InputTag("photonIDValueMapProducer:phoFull5x5SigmaIEtaIPhi"),
    ph_ESsigma       = cms.InputTag("photonIDValueMapProducer:phoESEffSigmaRR"),
    ph_hoe           = cms.string("hadronicOverEm"),

#iso
    ph_chIso    = cms.InputTag("photonIDValueMapProducer:phoChargedIsolation"),
    ph_neuIso   = cms.InputTag("photonIDValueMapProducer:phoNeutralHadronIsolation"),
    ph_phoIso   = cms.InputTag("photonIDValueMapProducer:phoPhotonIsolation"),
    ph_chWorIso = cms.InputTag("photonIDValueMapProducer:phoWorstChargedIsolation"), 

#pho mva
    ph_mva          = cms.InputTag("photonMVAValueMapProducer:PhotonMVAEstimatorRun2Spring15NonTrig25nsV2p1Values"),
    ph_mva80X       = cms.InputTag("photonMVAValueMapProducer:PhotonMVAEstimatorRun2Spring16NonTrigV1Values"),
)




TagVariablesToStore = cms.PSet(
    ele_eta    = cms.string("eta"),
    ele_phi    = cms.string("phi"),
    ele_abseta = cms.string("abs(eta)"),
    ele_pt     = cms.string("pt"),
    ele_et     = cms.string("et"),
    ele_e      = cms.string("energy"),
    ele_q      = cms.string("charge"),
    
    ## super cluster quantities
    sc_e      = cms.string("superCluster.energy"),
    sc_et     = cms.string("superCluster.energy*sin(superClusterPosition.theta)"),    
    sc_eta    = cms.string("-log(tan(superClusterPosition.theta/2))"),
    sc_abseta = cms.string("abs(-log(tan(superCluster.position.theta/2)))"),

    #ele_mHits         = cms.InputTag("eleVarHelper:missinghits"),
    #ele_dz            = cms.InputTag("eleVarHelper:dz"),
    #ele_dxy           = cms.InputTag("eleVarHelper:dxy"),
    ele_nonTrigMVA    = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values"),
    ele_trigMVA       = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15Trig25nsV1Values"),

    )

CommonStuffForGsfElectronProbe = cms.PSet(
    addEventVariablesInfo   =  cms.bool(True),

    variables        = cms.PSet(EleProbeVariablesToStore),
    pairVariables    =  cms.PSet(ZVariablesToStore),
    tagVariables     =  cms.PSet(TagVariablesToStore),

    ignoreExceptions = cms.bool (True),
    addRunLumiInfo   = cms.bool (True),
    pileupInfoTag    = cms.InputTag("slimmedAddPileupInfo"),
    vertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices"),    
    beamSpot         = cms.InputTag("offlineBeamSpot"),
    addCaloMet       = cms.bool(False),
    pfMet            = cms.InputTag("slimmedMETsPuppi"),
    rho              = cms.InputTag("fixedGridRhoFastjetAll"),
    #    pfMet = cms.InputTag("slimmedMETsNoHF"),

    pairFlags     =  cms.PSet(
        mass60to120 = cms.string("60. < mass < 120."),
        mass70to110 = cms.string("70. < mass < 110."),
        mass80to100 = cms.string("80. < mass < 100.")
        ),
    tagFlags       =  cms.PSet(),    
    
    )

CommonStuffForPhotonProbe = CommonStuffForGsfElectronProbe.clone()
CommonStuffForPhotonProbe.variables = cms.PSet(PhoProbeVariablesToStore)

CommonStuffForSuperClusterProbe = CommonStuffForGsfElectronProbe.clone()
CommonStuffForSuperClusterProbe.variables = cms.PSet(SCProbeVariablesToStore)

mcTruthCommonStuff = cms.PSet(
    isMC = cms.bool(True),
    tagMatches   = cms.InputTag("genTagEle"),
    motherPdgId = cms.vint32(),
    #motherPdgId = cms.vint32(22,23),
    #motherPdgId = cms.vint32(443), # JPsi
    #motherPdgId = cms.vint32(553), # Yupsilon
    makeMCUnbiasTree = cms.bool(False),
    #checkMotherInUnbiasEff = cms.bool(False),
    mcVariables = cms.PSet(
        probe_eta    = cms.string("eta"),
        probe_phi    = cms.string("phi"),
        probe_et     = cms.string("et"),
        probe_e      = cms.string("energy"),
        ),
    mcFlags     =  cms.PSet(
        probe_flag = cms.string("pt>0")
        ),      
    )



def setupTnPVariablesForAOD():
    CommonStuffForSuperClusterProbe.pileupInfoTag    = cms.InputTag("addPileupInfo")
    CommonStuffForSuperClusterProbe.vertexCollection = cms.InputTag("offlinePrimaryVerticesWithBS")
    CommonStuffForSuperClusterProbe.pfMet            = cms.InputTag("pfMet")

    CommonStuffForGsfElectronProbe.pileupInfoTag     = cms.InputTag("addPileupInfo")
    CommonStuffForGsfElectronProbe.vertexCollection  = cms.InputTag("offlinePrimaryVerticesWithBS")
    CommonStuffForGsfElectronProbe.pfMet             = cms.InputTag("pfMet")

    CommonStuffForPhotonProbe.pileupInfoTag          = cms.InputTag("addPileupInfo")
    CommonStuffForPhotonProbe.vertexCollection       = cms.InputTag("offlinePrimaryVerticesWithBS")
    CommonStuffForPhotonProbe.pfMet                  = cms.InputTag("pfMet")
   
    del CommonStuffForGsfElectronProbe.variables.probe_ele_ecalIso
    del CommonStuffForGsfElectronProbe.variables.probe_ele_hcalIso
    del CommonStuffForGsfElectronProbe.variables.probe_ele_trkIso
