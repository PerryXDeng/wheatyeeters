# Look at data



library(tidyverse)

library(DBI)
library(RSQLite)

gpsData <- read.csv("data/gps.csv")


gpsDataTibble <- as_tibble(gpsData)



#workingTibble <- head(gpsDataTibble, 500000)

workingTibble <- gpsDataTibble


playerIds <-unique(workingTibble$PlayerID)
cat("Number of Players: ", length(playerIds), sep="")

gameIds <- unique(workingTibble$GameID)
cat("Number of Games: ", length(gameIds), sep="")


playerIDMetrics <- c()
gameIDMetrics <- c()
averageSpeed <- c()

accelDistance <- c()


for(playerID in playerIds)
{
  for(gameID in gameIds)
  {
    cat(playerID, gameID , '\n', sep=" ")
    speedTibble <- subset(workingTibble, GameID == gameID & PlayerID == playerID)
    
    
    # crunch average speed    
    averageSpeed <- c(averageSpeed, mean(speedTibble$Speed, na.rm = 0))
    
    # average for accel value  
    
    accelDistance <- c(accelDistance, mean(sqrt(speedTibble$AccelX^2 + speedTibble$AccelY^2 + speedTibble$AccelZ^ 2), na.rm = 0))
    
  
    # game and player id to vector
    playerIDMetrics <- c(playerIDMetrics, playerID)
    gameIDMetrics <- c(gameIDMetrics, gameID)
  }
}


plot(accelDistance, averageSpeed)

compressedMetrics <- tibble(gameID = gameIDMetrics, playerID = playerIDMetrics, averageSpeed = averageSpeed, accelerationVector = accelDistance)


length(compressedMetrics$averageSpeed)
length(compressedMetrics$accelerationVector)

write.csv(compressedMetrics, "data/speedData.csv")

#putSQLiteHere <- "gpsData.sqlite" # could also be ":memory:"
#mySQLiteDB <- dbConnect(RSQLite::SQLite(),putSQLiteHere)


#dbWriteTable(mySQLiteDB, "gpsData", compressedMetrics, overwrite=TRUE)

#dbDisconnect(mySQLiteDB)




wellnessData <- read.csv("./data/wellness_na.csv")
wellnessDataTibble <- as_tibble(wellnessData)




#plot(wellnesPlayer1$Fatigue * wellnesPlayer1$Soreness * wellnesPlayer1$Irritability, wellnesPlayer1$SleepHours * wellnesPlayer1$SleepQuality)


wellnessCleaned <- as_tibble(read.csv("./cleaned/dirty_wellness.csv"))
wellnesPlayer1 <- subset(wellnessCleaned, PlayerID == 1)


ggplot(data = wellnessCleaned) + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  ggtitle("Hours of Sleep Box Plot") + 
  geom_boxplot(na.rm = T, mapping = aes(y=SleepHours, group = PlayerID), outlier.colour = "red", outlier.shape = 1) + 
  labs(group = "Player ID", y = "Hours of Sleep") +
  coord_flip() +
  theme_bw()


ggplot(data = wellnessCleaned) + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  ggtitle("Fatigue Box Plot") + 
  geom_boxplot(na.rm = T, mapping = aes(y=Fatigue, group = PlayerID), outlier.colour = "red", outlier.shape = 1) + 
  labs(group = "Player ID", y = "Fatigue Score") +
  coord_flip() +
  theme_bw()


ggplot(data = wellnessCleaned) + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  ggtitle("Sleep Quality Box Plot") + 
  geom_boxplot(na.rm = T, mapping = aes(y=SleepQuality, group = PlayerID), outlier.colour = "red", outlier.shape = 1) + 
  labs(group = "Player ID", y = "Sleep Quality") +
  coord_flip() +
  theme_bw()


ggplot(data = wellnessCleaned) + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  ggtitle("Training Readiness Box Plot") + 
  geom_boxplot(na.rm = T, mapping = aes(y=TrainingReadinessNum, group = PlayerID), outlier.colour = "red", outlier.shape = 1) + 
  labs(group = "Player ID", y = "Training Readiness") +
  coord_flip() +
  theme_bw()


plot(density(wellnesPlayer1$SleepHours))

max(wellnessCleaned$SleepHours, na.rm = T)
min(wellnessCleaned$SleepHours, na.rm = T)


playerIdsWellness <-unique(wellnessCleaned$PlayerID)
cat("Number of Players: ", length(playerIdsWellness), sep="")




rpeData <- read.csv("./data/rpe.csv")
rpeDataTibble <- as_tibble(rpeData)


gameData <- read.csv("data/games.csv")
gameDataTibble <- as_tibble(gameData)



par(mfrow = c(4, 5))

playerIdsWellness <- sort(playerIdsWellness)

for(playerID in playerIdsWellness)
{
  if(!is.na(playerID) && playerID < 88)
  {
    #print(playerID)
    #welnessTibble <- c()
    
    
    welnessTibble <- subset(wellnessCleaned,PlayerID == playerID)
    #print(length(welnessTibble$SleepHours))
    
    plot(density(welnessTibble$SleepHours, kernel = "gaussian", bw=0.5), main = paste("Player ", playerID, sep=""), xlab="Hours of Sleep")
    
    #lines(density(welnessTibble$SleepHours))
  }
}


plot(density(wellnesPlayer1$SleepHours, kernel = "gaussian", bw=0.4), ylim=c(0,.7), xlab = "Hours of Sleep", main="Team's Sleep Distribution")
for(playerID in playerIdsWellness)
{
  if(!is.na(playerID) && playerID < 88)
  {
    #print(playerID)
    #welnessTibble <- c()
    
    welnessTibble <- subset(wellnessCleaned,PlayerID == playerID)

    lines(density(welnessTibble$SleepHours,kernel = "gaussian", bw=0.4))
  }
}



plot(density(wellnesPlayer1$Fatigue, kernel = "gaussian", bw=0.4), ylim=c(0,.7), xlab = "Self Reported Fatigue", main="Team's Fatigue Distribution")
for(playerID in playerIdsWellness)
{
  if(!is.na(playerID) && playerID < 88)
  {
    #print(playerID)
    #welnessTibble <- c()
    
    welnessTibble <- subset(wellnessCleaned,PlayerID == playerID)
    
    lines(density(welnessTibble$Fatigue,kernel = "gaussian", bw=0.4))
  }
}






head(gpsData)









# Normalize Wellness data

