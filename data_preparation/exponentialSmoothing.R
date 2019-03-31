fatigueFunction <- function(workLoad, index)
{
  if(index == 1)
  {
    return(workLoad[1])
  }
  else
  {
    return(workLoad[index] + (exp(1)^(-1/15))**fatigueFunction(workLoad, index -1))
  }
}


smoothVector <- function(dataV)
{
  dataNew <- c()
  
  for(i in 1:length(dataV))
  {
    dataNew <- c(dataNew, fatigueFunction(dataV, i))
  }
  dataNew
}



slidingWindowSmooth <- function(dataV, windowSize = 7)
{
  dataNew <- c()
  
  
  for(i in 1:windowSize)
  {
    dataNew <- c(dataNew, mean(dataV[c(1:i)]))
  }
  
  
  for(i in (windowSize + 1):length(dataV))
  {
    dataNew <- c(dataNew, mean(dataV[(i-7):i]))
  }
  dataNew
}