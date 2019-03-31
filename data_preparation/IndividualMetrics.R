source("readData.R")
source("exponentialSmoothing.R")

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



desireCol <- c()


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
      desireCol <- c(desireCol, wellnessDay$Desire)
      fatigueRawCol <- c(fatigueRawCol, mean(wellnessDay$Fatigue, na.rm =T))
      sleepQualityCol <- c(sleepQualityCol, mean(wellnessDay$SleepQuality, na.rm = T))
      sleepHoursCol <- c(sleepHoursCol, sum(wellnessDay$SleepHours, na.rm = T))
      sorenessCol <- c(sorenessCol, mean(wellnessDay$Soreness, na.rm = T))
    }
    else
    {
      desireCol <- c(desireCol, median(wellnessData$Desire))
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


accuteFatigueSliding <- slidingWindowSmooth(acuteChronicRatioCol)


massiveTibble <- tibble(day = dayCol,
                        playerID = playerid,
                        DailyLoad = dailyLoadCol,
                        DailyLoadSliding = slidingWindowSmooth(DailyLoad),
                        acuteChronicRatio = acuteChronicRatioCol,
                        acuteChronicRatioSliding = slidingWindowSmooth(acuteChronicRatioCol),
                        trainDuration = trainDuration,
                        trainDurationSliding = slidingWindowSmooth(trainDuration),
                        sleepHours = sleepHoursCol,
                        sleepHoursSliding = slidingWindowSmooth(sleepHours),
                        fatigue = fatigueRawCol,
                        fatigueSliding = slidingWindowSmooth(fatigue),
                        sleepQuality = sleepQualityCol,
                        soreness = sorenessCol,
                        sorenessSliding = slidingWindowSmooth(soreness),
                        fatigueNorm = normFatCol,
                        fatigueNormSliding = slidingWindowSmooth(fatigueNorm),
                        sorenessNorm = normSoreCol,
                        sleepHoursNorm = normSleepHours,
                        sleepQualityNorm = normSleepQuality,
                        BestOutOfMyselfNotAtAll = notatAllCol,
                        BestOutOfMyselfAbsolutely = absCol,
                        BestOutOfMyselfSomewhat = somewhatCol,
                        BestOutOfMyselfUnknown = unknownCol,
                        desire = desireCol)

write.csv(massiveTibble, "cleaned/personal.csv")


ggplot(data = massiveTibble) + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  ggtitle("Normalized Soreness Box Plots") + 
  geom_boxplot(na.rm = T, mapping = aes(y=sorenessNorm, group = playerID), outlier.colour = "red", outlier.shape = 1) + 
  labs(group = "Player ID", y = "Normalized Soreness Values") +
  coord_flip() +
  theme_bw()

ggplot(data = massiveTibble) + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  ggtitle("Normalized Sleep Quality Box Plots") + 
  geom_boxplot(na.rm = T, mapping = aes(y=sleepQualityNorm, group = playerID), outlier.colour = "red", outlier.shape = 1) + 
  labs(group = "Player ID", y = "Normalized Sleep Quality") +
  coord_flip() +
  theme_bw()


ggplot(data = massiveTibble) + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  ggtitle("Soreness Box Plots") + 
  geom_boxplot(na.rm = T, mapping = aes(y=sleepQuality, group = playerID), outlier.colour = "red", outlier.shape = 1) + 
  labs(group = "Player ID", y = "Sleep Quality") +
  coord_flip() +
  theme_bw()


ggplot(data = massiveTibble) + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  ggtitle("Team's Percieved Fatigue") + 
  geom_point(mapping = aes(x=day, y=fatigueNormSliding)) + 
  labs(x = "Days Since August First 2017", y = "Teams Fatigue")+ 
  theme_bw()


ggplot(data = massiveTibble) + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  ggtitle("Team's Percieved Fatigue") + 
  geom_point(mapping = aes(x=day, y=sorenessSliding)) + 
  labs(x = "Days Since August First 2017", y = "Accute Fatugue ")+ 
  theme_bw()


ggplot(data = massiveTibble) + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  ggtitle("Team's Percieved Fatigue") + 
  geom_point(mapping = aes(x=sleepQuality, y=fatigueNorm)) + 
  labs(x = "Days Since August First 2017", y = "Accute Fatugue ") + 
  theme_bw()
