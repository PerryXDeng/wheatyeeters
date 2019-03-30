source("readData.R")

library(tidyverse)


# file to replace NA values with the median for thet column


trainingData <- readRPEData()

#duration
trainingData$Duration[is.na(trainingData$Duration)] <- median(trainingData$Duration, na.rm=TRUE)


#RPE
trainingData$RPE[is.na(trainingData$RPE)] <- median(trainingData$RPE, na.rm=TRUE)

# acute load
trainingData$AcuteLoad[is.na(trainingData$AcuteLoad)] <- median(trainingData$AcuteLoad, na.rm=TRUE)

# chronic load
trainingData$ChronicLoad[is.na(trainingData$ChronicLoad)] <- median(trainingData$ChronicLoad, na.rm=TRUE)

# ratio
trainingData$AcuteChronicRatio[is.na(trainingData$AcuteChronicRatio)] <- median(trainingData$AcuteChronicRatio, na.rm=TRUE)

# objective rating
trainingData$ObjectiveRating[is.na(trainingData$ObjectiveRating)] <- median(trainingData$ObjectiveRating, na.rm=TRUE)


# focus rating
trainingData$FocusRating[is.na(trainingData$FocusRating)] <- median(trainingData$FocusRating, na.rm=TRUE)


trainingData$RPE[is.na(trainingData$RPE)] <- median(trainingData$RPE, na.rm=TRUE)

write.csv(as.data.frame(trainingData), "cleaned/time_series_rpw_naReplacedWithMedian.csv")


head(as.data.frame(trainingData), 100)




trainingData
