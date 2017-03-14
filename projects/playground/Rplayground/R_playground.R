getwd()
setwd('/Users/dischnerz/code/udatascience/projects/playground')

# Read a csv - neat
statesInfo <- read.csv('stateData.csv')

# Northeast subset of the DataFrame
stateSubset <- subset(statesInfo, state.region == 1)
head(stateSubset,2)
dim(stateSubset)