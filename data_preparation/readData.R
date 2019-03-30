library(tidyverse)


readGPSMetrics <- function()
{
  as_tibble(read.csv("./data/speedData.csv"))
}

readWellnessData <- function()
{
  as_tibble(read.csv("./cleaned/time_series_notnormalized_with_0NaN_wellness.csv"))
}

readRPEData <- function()
{
  as_tibble(read.csv("./cleaned/time_series_notnormalized_with_continuousNan_rpe.csv"))
}


readNArpeData <- function()
{
  as_tibble(read.csv("./cleaned/time_series_notnormalized_with_continuousNan_rpe.csv"))
}
