source("readData.R")

library(tidyverse)


RPEData <-readNArpeData()


numDays <- max(RPEData$TimeSinceAugFirst)


dayList <- 0:numDays
workLoad <- c()
averageWorkLoad <- c()


for(day in dayList)
{
  total <- 0
  
  daylyActivities <- subset(RPEData, TimeSinceAugFirst == day)
  cat("day: ", day, "\n",sep="")
  cat("Activity count:", length(daylyActivities$DailyLoad), "\n", sep="")
  
  averageWorkLoad <- c(averageWorkLoad, mean(daylyActivities$SessionLoad, na.rm = T))
  workLoad <- c(workLoad, sum(daylyActivities$SessionLoad, na.rm = T))
}
plot(dayList, averageWorkLoad, main="Average Work Load")
plot(dayList, workLoad, main="Daily Total Work Load")


slidingAverage <- c()

window <- 7 - 1
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