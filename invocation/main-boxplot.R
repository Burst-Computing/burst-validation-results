library(ggplot2)
library(ggthemes)
library(gridExtra)

source("generate_boxplot.R")
g1 <- generate_boxplot(48)
g2 <- generate_boxplot(96)
g3 <- generate_boxplot(480)
g4 <- generate_boxplot(960)

#plot g1, g2, g3 in a grid
grid.arrange(g1, g2, g3, g4, ncol=2)
# add x and y axis labels to grid

