from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'DY_M_50_120_HLT_Ele23_Ele12_mAOD_94X_mc2017_realistic_v10'
config.General.workArea = 'crab_DY_powheg_M_50_120_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_94X_mc2017_realistic_v10'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'TnP_Ele23_Ele12_MC_v2.py'

config.Data.inputDataset = '/ZToEE_NNPDF31_13TeV-powheg_M_50_120/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v2/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1

config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.outputDatasetTag = 'DY_powheg_M_50_120_MINIAODSIM_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_94X_mc2017_realistic_v10'
config.Site.storageSite = 'T2_KR_KNU'
