from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'DYToEE_M-50_NNPDF31_13TeV_DoubleElectronTriggers'
config.General.workArea = 'crab_DYToEE_M-50_NNPDF31_13TeV_DoubleElectronTriggers'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'TnP_2018Double.py'

config.Data.inputDataset = '/DYToEE_M-50_NNPDF31_13TeV-powheg-pythia8/RunIISpring18MiniAOD-100X_upgrade2018_realistic_v10-v1/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1

config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.outputDatasetTag = 'DYToEE_M-50_NNPDF31_13TeV_DoubleElectronTriggers'
config.Site.storageSite = 'T2_KR_KNU'
