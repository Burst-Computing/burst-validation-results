library(ggplot2)
library(ggthemes)
library(gridExtra)
library(grid)

source("generate_boxplot.R")
g1 <- generate_boxplot(48)
g4 <- generate_boxplot(960)

#plot g1, g2, g3 in a grid
g <- grid.arrange(g1, g4, ncol=2, 
        bottom=textGrob("Start-up time (s)", gp=gpar(fontsize=10, fontfamily="Linux Libertine")), 
        left=textGrob("Granularity", gp=gpar(fontsize=10, fontfamily="Linux Libertine"), rot=90))

ggsave(
  filename = "boxplot-paper-2.pdf", 
  plot = g, 
  device = cairo_pdf, 
  width = 83, 
  height = 35,
  units = "mm"
)