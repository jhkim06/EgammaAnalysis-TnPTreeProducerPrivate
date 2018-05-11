from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'SingleElectron_Run2017E_17Nov2017_HLT_Ele32WPT_performances'
config.General.workArea = 'crab_HLT_Ele32WPT_data_tnpNtuple'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'TnP_2017_HLT_Ele32WPT.py'

config.Data.inputDataset = '/SingleElectron/Run2017E-17Nov2017-v1/MINIAOD'
config.Data.splitting = 'LumiBased'
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/PromptReco/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
config.Data.unitsPerJob = 100
config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.outputDatasetTag = 'SingleElectron_Run2017E_17Nov2017_HLT_Ele32WPT_tnpNtuple'
config.Site.storageSite = 'T2_KR_KNU'
