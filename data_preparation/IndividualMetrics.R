source("readData.R")

library(tidyverse)


RPEData <-readNArpeData()
wellnessData <- readWellnessData()
normalizedWellnessData <- readNormalizedMetrics()
RPEData


playerIDS <- playerIds <-unique(RPEData$PlayerID)


numDays <- max(RPEData$TimeSinceAugFirst)


dayList <- 0:numDays


dayCol <- c()
playerid <- c()

dailyLoadCol <- c()
acuteChronicRatioCol <- c()
trainDuration <- c()

sleepHoursCol <- c()
fatigueRawCol <- c()
sleepQualityCol <- c()
sorenessCol <- c()

normFatCol <-c()
normSoreCol <- c()
normSleepHours <- c()
normSleepQuality <- c()

notatAllCol <- c()
absCol <-c()
somewhatCol <- c()
unknownCol <- c()





for(day in dayList)
{
  for(id in playerIDS)
  {
    cat("Player:", id, "Day:", day, "\n", sep=" ")
    
    
    trainDay <- subset(RPEData, TimeSinceAugFirst == day & PlayerID == id)
    #workLoad <- c(workLoad, sum(daylyActivities$SessionLoad, na.rm = T))

    wellnessDay <- subset(wellnessData, TimeSinceAugFirst == day & PlayerID == id)

    
    normalizedDay <- subset(normalizedWellnessData, TimeSinceAugFirst == day & playerID == id)
    #if(length(normalizedDay$playerID) > 0)
    #{
    #  print("good")
    #}
    
    dayCol <- c(dayCol, day)
    playerid <- c(playerid, id)
    
    
    if(length(wellnessDay$SleepHours) > 0)
    {
      fatigueRawCol <- c(fatigueRawCol, mean(wellnessDay$Fatigue, na.rm =T))
      sleepQualityCol <- c(sleepQualityCol, mean(wellnessDay$SleepQuality, na.rm = T))
      sleepHoursCol <- c(sleepHoursCol, sum(wellnessDay$SleepHours, na.rm = T))
      sorenessCol <- c(sorenessCol, mean(wellnessDay$Soreness, na.rm = T))
    }
    else
    {
      sleepQualityCol <- c(sleepQualityCol, median(wellnessData$SleepQuality, na.rm = T))
      sleepHoursCol <- c(sleepHoursCol, median(wellnessData$SleepHours))
      fatigueRawCol <- c(fatigueRawCol, median(wellnessData$Fatigue))
      sorenessCol <- c(sorenessCol, median(wellnessData$Soreness))
    }

    
    if(length(normalizedDay$normSoreness) > 0)
    {
      normFatCol <- c(normFatCol, mean(normalizedDay$normFatigue, na.rm=T))
      normSoreCol <- c(normSoreCol, mean(normalizedDay$normSoreness, na.rm = T))
      normSleepHours <- c(normSleepHours, mean(normalizedDay$normSleepHours, na.rm =T))
      normSleepQuality <- c(normSleepQuality, mean(normalizedDay$normSleepQuality, na.rm=T))
    }
    else
    {
      normFatCol <- c(normFatCol, mean(normalizedWellnessData$normFatigue, na.rm=T))
      normSoreCol <- c(normSoreCol, mean(normalizedWellnessData$normSoreness, na.rm = T))
      normSleepHours <- c(normSleepHours, mean(normalizedWellnessData$normSleepHours, na.rm =T))
      normSleepQuality <- c(normSleepQuality, mean(normalizedWellnessData$normSleepQuality, na.rm=T))
    }
    
    if(length(trainDay$SessionLoad) > 0)
    {
      dailyLoadCol <- c(dailyLoadCol, mean(trainDay$DailyLoad,na.rm = T))
      acuteChronicRatioCol <- c(acuteChronicRatioCol, mean(trainDay$AcuteChronicRatio, na.rm =T))
      trainDuration <- c(trainDuration, sum(trainDay$Duration, na.rm = T))
      
      notatAllCol <- c(notatAllCol, max(trainDay$BestOutOfMyselfNotAtAll))
      absCol <- c(absCol, max(trainDay$BestOutOfMyselfAbsolutely))
      somewhatCol <- c(somewhatCol, max(trainDay$BestOutOfMyselfSomewhat))
      unknownCol <- c(unknownCol, max(trainDay$BestOutOfMyselfUnknown))
    }
    else
    {
      dailyLoadCol <- c(dailyLoadCol, 0)
      acuteChronicRatioCol <- c(acuteChronicRatioCol, 0)
      trainDuration <- c(trainDuration, 0)
      
      
      notatAllCol <- c(notatAllCol, 0)
      absCol <- c(absCol, 0)
      somewhatCol <- c(somewhatCol, 0)
      unknownCol <- c(unknownCol, 1)
    }
  }
  
}


dailyLoadCol[is.na(dailyLoadCol)] <- 0
acuteChronicRatioCol[is.na(acuteChronicRatioCol)] <- 0



massiveTibble <- tibble(day = dayCol,
                        playerID = playerid,
                        DailyLoad = dailyLoadCol,
                        acuteChronicRatio = acuteChronicRatioCol,
                        trainDuration = trainDuration,
                        sleepHours = sleepHoursCol,
                        fatigue = fatigueRawCol,
                        sleepQuality = sleepQualityCol,
                        soreness = sorenessCol,
                        fatigueNorm = normFatCol,
                        sorenessNorm = normSoreCol,
                        sleepHoursNorm = normSleepHours,
                        sleepQualityNorm = normSleepQuality,
                        BestOutOfMyselfNotAtAll = notatAllCol,
                        BestOutOfMyselfAbsolutely = absCol,
                        BestOutOfMyselfSomewhat = somewhatCol,
                        BestOutOfMyselfUnknown = unknownCol)

write.csv(massiveTibble, "cleaned/personal.csv")
