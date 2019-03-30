# Look at data



library(tidyverse)

gpsData <- read.csv("data/gps.csv")


gpsDataTibble <- as_tibble(gpsData)




workingTibble <- head(gpsDataTibble, 100000)


playerIds <-unique(workingTibble$PlayerID)


gameIds <- unique(workingTibble$GameID)


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
    averageSpeed <- c(averageSpeed, mean(speedTibble$Speed))
    
    # average for accel value  
    
    accelDistance <- c(accelDistance, mean(sqrt(speedTibble$AccelX^2 + speedTibble$AccelY^2 + speedTibble$AccelZ^ 2)))
    
    
    #xAccel <- c(xAccel, mean(speedTibble$AccelX))
    #yAccel <- c(yAccel, mean(speedTibble$AccelY))
    #zAccel <- c(zAccel, mean(speedTibble$AccelZ))
    
  
    # game and player id to vector
    playerIDMetrics <- c(playerIDMetrics, playerID)
    gameIDMetrics <- c(gameIDMetrics, gameID)
  }
}


plot(accelDistance, averageSpeed)






rpeData <- read.csv("./data/rpe.csv")
rpeDataTibble <- as_tibble(rpeData)


gameData <- read.csv("./data/game.csv")
gameDataTibble <- as_tibble(gameData)


wellnessData <- read.csv("./data/wellness.csv")
wellnessDataTibble <- as_tibble(wellnessData)

head(gpsData)