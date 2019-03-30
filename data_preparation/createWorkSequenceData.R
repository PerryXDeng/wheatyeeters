source("readData.R")

library(tidyverse)


RPEData <-readNArpeData()


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
plot(dayList, averageWorkLoad, main="Average Work Load")
plot(dayList, workLoad, main="Daily Total Work Load")


slidingAverage <- c()

window <- 31 - 1
for(day in window:numDays)
{
  windowAverage <- mean(workLoad[c((day-window):day)])
  slidingAverage <- c(slidingAverage, windowAverage)
}



plot(window:numDays, slidingAverage, main="Sliding Average")
plot(density(slidingAverage), main="Sliding Average Density")
plot(density(workLoad), main="Total Work Load Average")


dataTibble <- tibble(TimeSinceAugFirst = window:numDays, slidingWorkAverage = slidingAverage)


ggplot(data = dataTibble) + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  ggtitle("Team's 7 Day Moving Average") + 
  geom_point(mapping = aes(x=TimeSinceAugFirst, y=slidingWorkAverage)) + 
  labs(x = "Days Since August Seventh 2017", y = "Teams Total Daily Load")+ 
  theme_bw()



write.csv(dataTibble, "cleaned/slidingWorkAverageSevenDay.csv")


################################      Wellness Data      ###################################

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

graphingTib <- tibble(slidingAverage = slidingAverage, days = window:dayNum)

ggplot(data = graphingTib) + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  ggtitle("Team's Average Normalized Fatigue") + 
  geom_point(mapping = aes(x=days, y=slidingAverage)) + 
  labs(x = "Days Since August Twenty First 2017", y = "Teams Average Normalized Fatigue")+ 
  theme_bw()

plot(density(slidingAverage))
plot(window:dayNum, slidingAverage)



