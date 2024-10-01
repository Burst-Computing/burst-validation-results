library(ggplot2)
library(ggthemes)
library(gridExtra)
library(grid)


source("generate_inv_plot.R")
g1 <- generate_inv_plot(1)
g2 <- generate_inv_plot(48)

g <- grid.arrange(g1, g2, ncol=2,
        bottom=textGrob("Time (s)", gp=gpar(fontsize=10, fontfamily="Linux Libertine")),
        left=textGrob("# activation", gp=gpar(fontsize=10, fontfamily="Linux Libertine"), rot=90))
ggsave(
  filename = "invocation-paper.pdf", 
  plot = g, 
  device = cairo_pdf, 
  width = 83, 
  height = 35,
  units = "mm"
)