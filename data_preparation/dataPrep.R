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







rpeData <- read.csv("./data/rpe.csv")
rpeDataTibble <- as_tibble(rpeData)


gameData <- read.csv("./data/game.csv")
gameDataTibble <- as_tibble(gameData)


wellnessData <- read.csv("./data/wellness.csv")
wellnessDataTibble <- as_tibble(wellnessData)

head(gpsData)