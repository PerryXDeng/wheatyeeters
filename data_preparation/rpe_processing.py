import pandas as pd

csv = pd.read_csv("data/rpe.csv")
training = csv["Training"].unique()
session = csv["SessionType"].unique()
boms = csv["BestOutOfMyself"].unique()
print(training)
print(session)
print(boms)


# csv["SessionTypeMobilityRecovery"] = csv["SessionType"]
# csv.SessionTypeMobilityRecovery[csv.SessionType == 'Mobility/Recovery'] = 1
# csv.SessionTypeMobilityRecovery[csv.SessionType != 'Mobility/Recovery'] = 0
#
# csv["SessionTypeGame"] = csv["SessionTypeMobilityRecovery"]
# csv.SessionTypeGame[csv.SessionType == 'Game'] = 1
# csv.SessionTypeGame[csv.SessionType != 'Game'] = 0
#
# csv["SessionTypeSkills"] = csv["SessionTypeMobilityRecovery"]
# csv.SessionTypeSkills[csv.SessionType == 'Skills'] = 1
# csv.SessionTypeSkills[csv.SessionType != 'Skills'] = 0
#
# csv["SessionTypeConditioning"] = csv["SessionTypeMobilityRecovery"]
# csv.SessionTypeConditioning[csv.SessionType == 'Conditioning'] = 1
# csv.SessionTypeConditioning[csv.SessionType != 'Conditioning'] = 0
#
# csv["SessionTypeStrength"] = csv["SessionTypeMobilityRecovery"]
# csv.SessionTypeStrength[csv.SessionType == 'Strength'] = 1
# csv.SessionTypeStrength[csv.SessionType != 'Strength'] = 0
#
# csv["SessionTypeCombat"] = csv["SessionTypeMobilityRecovery"]
# csv.SessionTypeCombat[csv.SessionType == 'Combat'] = 1
# csv.SessionTypeCombat[csv.SessionType != 'Combat'] = 0
#
# csv["SessionTypeSpeed"] = csv["SessionTypeMobilityRecovery"]
# csv.SessionTypeSpeed[csv.SessionType == 'Speed'] = 1
# csv.SessionTypeSpeed[csv.SessionType != 'Speed'] = 0

print(csv.head())
