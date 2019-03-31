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


readNormalizedMetrics <- function()
{
  as_tibble(read.csv("./cleaned/time_series_normalized_wellness.csv"))
}


readFatigueSums <- function()
{
  as_tibble(read.csv("./cleaned/fatigue_total_sum.csv"))
}


readGameRandChanges <- function()
{
  as_tibble(read.csv("./cleaned/time_series_days_ranked.csv"))
}
