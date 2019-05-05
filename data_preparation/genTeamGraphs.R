source("readData.R")

library(tidyverse)


RPEData <-readNArpeData()

games <- readGameRandChanges


numDays <- max(RPEData$TimeSinceAugFirst)


dayList <- 0:numDays
workLoad <- c()
averageWorkLoad <- c()


for(day in dayList)
{
  daylyActivities <- subset(RPEData, TimeSinceAugFirst == day)
  cat("day: ", day, "\n",sep="")
  cat("Activity count:", length(daylyActivities$DailyLoad), "\n", sep="")
  
  averageWorkLoad <- c(averageWorkLoad, mean(daylyActivities$SessionLoad, na.rm = T))
  workLoad <- c(workLoad, sum(daylyActivities$SessionLoad, na.rm = T))
}



fatigueFunction <- function(workLoad, index)
{
  if(index == 1)
  {
    return(workLoad[1])
  }
  else
  {
    return(workLoad[index] + (exp(1)^(-1/15))*fatigueFunction(workLoad, index -1))
  }
}

smoothedWork <- c()
for(day in dayList)
{
  smoothedWork <- c(smoothedWork, fatigueFunction(workLoad, day + 1))
}



fatigueData <- readFatigueSums()

dayNum <- max(fatigueData$TimeSinceAugFirst)

dayList <- 0:dayNum


slidingAverage <- c()
window <- 21 - 1
for(day in window:dayNum)
{
  windowAverage <- mean(fatigueData$fatigueSum[c((day-window):day)], na.rm = T)
  
  slidingAverage <- c(slidingAverage, windowAverage)
}

smoothedFatigueData <- c()
for(day in dayList)
{
  smoothedFatigueData <- c(smoothedFatigueData, fatigueFunction(fatigueData$fatigueSum, day + 1))
}

plot(dayList, smoothedFatigueData)


workTibble <- tibble(day = dayList, totalWork = workLoad,
                     averageWorkLoad = averageWorkLoad, 
                     smoothedWork = smoothedWork,
                     smoothedFatigueData = smoothedFatigueData)

plot(workTibble$totalWork, fatigueData$fatigueSum[-1])

workGraph <- ggplot(data = workTibble) + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  ggtitle("Team's Smoothed Work") + 
  geom_point(mapping = aes(x=day, y=smoothedWork)) + 
  labs(x = "Days Since August First 2017", y = "Teams Training Work")+ 
  theme_bw()

fatGraph <- ggplot(data = workTibble) + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  ggtitle("Team's Percieved Fatigue") + 
  geom_point(mapping = aes(x=day, y=smoothedFatigueData)) + 
  labs(x = "Days Since August First 2017", y = "Teams Average Normalized Fatigue")+ 
  theme_bw()


ggplot(data = workTibble) + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  ggtitle("Team's Percieved Fatigue") + 
  geom_point(mapping = aes(x=smoothedWork, y=smoothedFatigueData)) + 
  labs(x = "Smoothed Work Per Day", y = "Teams Average Normalized Fatigue")+ 
  theme_bw()


for(gameDay in games$Date)
{
  fatGraph <- fatGraph + geom_vline(xintercept = gameDay, linetype="dotted", 
                                    color = "blue", size=1.0)
  workGraph <- workGraph + geom_vline(xintercept = gameDay, linetype="dotted", 
                                      color = "blue", size=1.0)
}



workGraph
fatGraph
