source("readData.R")

library(tidyverse)

library(bestNormalize)


# File to normalize the user inputted data in
# the wellness

wellnessData <- readWellnessData()


playerIds <-unique(wellnessData$PlayerID)
cat("Number of Players: ", length(playerIds), sep="")



normPlayerIDs <- c()
normDate <- c()


normFatigue <- c()
normSoreness <- c()
normDesire <- c()
normIrritability <- c()
normSleepHours <- c()
normSleepQuality <- c()


for(id in playerIds)
{
  wellnessDataT <- subset(wellnessData, PlayerID == id)
  if(length(wellnessDataT$Fatigue) > 0)
  {
    print(id)
    userTibble <- subset(wellnessData, PlayerID == id)
    print(length(userTibble$Fatigue))
    
    #fatigueNormalized <- bestNormalize(userTibble$Fatigue)
    fatigueNormalized <- bestNormalize(userTibble$Fatigue, standardize = TRUE)
    
    fatNorm <-predict(fatigueNormalized)
    
    print(fatigueNormalized)
    
    
    sleepNormalized <- bestNormalize(userTibble$SleepHours, standardize = TRUE)
    sleepNorm <-predict(fatigueNormalized)
    
    
    soreness <- bestNormalize(userTibble$Soreness, standardize = TRUE)
    sorenessNorm <- predict(soreness)
    
    
    desire <- bestNormalize(userTibble$Desire, standardize = TRUE)
    desireNorm <- predict(desire)
    
    irritability <- bestNormalize(userTibble$Irritability, standardize = TRUE)
    irritabilityNorm <- predict(irritability)
    
    
    sleepHours <- bestNormalize(userTibble$SleepHours, standardize = TRUE)
    sleepHoursNorm <- predict(sleepHours)
    
    sleepQuality <- bestNormalize(userTibble$SleepQuality, standardize = TRUE)
    sleepQualityNorm <- predict(sleepQuality)
    
    
    normPlayerIDs <- c(normPlayerIDs, userTibble$PlayerID)
    normDate <- c(normDate, userTibble$TimeSinceAugFirst)
    normSoreness <- c(normSoreness, sorenessNorm)
    normFatigue <- c(normFatigue, fatNorm)
    normDesire <- c(normDesire, desireNorm)
    normIrritability <- c(normIrritability, irritabilityNorm)
    normSleepHours <- c(normSleepHours, sleepHoursNorm)
    normSleepQuality <- c(normSleepQuality, sleepQualityNorm)
    
    #plot(density(userTibble$SleepHours))
    #plot(density(sleepNorm))
    
  }
}


normalWellnessData <- tibble(TimeSinceAugFirst = normDate, playerID = normPlayerIDs, normSoreness = normSoreness, 
                            normFatigue = normFatigue, normDesire = normDesire, normIrritability = normIrritability,
                            normSleepHours = normSleepHours, normSleepQuality = normSleepQuality)

write.csv(normalWellnessData, "cleaned/time_series_normalized_wellness.csv")


plot()

plot(normDesire, normSoreness)

print(fagigueNormalized)
