fatigueFunction <- function(workLoad, index)
{
  if(index == 1)
  {
    return(workLoad[1])
  }
  else
  {
    return(workLoad[index] + 0.7*fatigueFunction(workLoad, index -1))
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


smoothVector(c(1,2,3,4))

plot(1:100, smoothVector(1:100))