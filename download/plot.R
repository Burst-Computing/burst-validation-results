library(ggplot2)
library(scales)
library(ggthemes)

boxplot_fill = "#00bfc4"
bar_fill = "darkblue"

# i want a plot with next specs:
#    in x axis: download_time
#    in y axis: different categories {1,2,4,6,12,24,48}
# i want a boxplot for each category with the download_time values

gran1 <- read.csv("plot/gran1.csv", header=TRUE, sep=",")
gran2 <- read.csv("plot/gran2.csv", header=TRUE, sep=",")
gran4 <- read.csv("plot/gran4.csv", header=TRUE, sep=",")
gran6 <- read.csv("plot/gran6.csv", header=TRUE, sep=",")
gran12 <- read.csv("plot/gran12.csv", header=TRUE, sep=",")
gran24 <- read.csv("plot/gran24.csv", header=TRUE, sep=",")
gran48 <- read.csv("plot/gran48.csv", header=TRUE, sep=",")

custom_transform <- function(x) {
  ifelse(x<0, x, 4.8*x)
}

custom_trans <- trans_new(name = "custom", transform = custom_transform, inverse = function(x) x)

g <- ggplot() + scale_y_discrete(limits=c("FaaS", "2", "4", "6", "12", "24", "48")) +
# i want a continuous x axis, with 0 value at center (left side limit -96, right side limit 20)
# is very important that 0 value is at center of x space in plot(notice that different steps are used for each side)
scale_x_continuous(trans=custom_trans, breaks=c(-100, -50, 0, 5, 10, 15, 20), labels=c("100GB", "50GB", 0, "5s", "10s", "15s", "20s")) +
  theme_minimal() + 
  geom_boxplot(data=gran1, aes(x=download_time, y="FaaS"), fill="#f8766d") +
geom_boxplot(data=gran2, aes(x=download_time, y="2"), fill=boxplot_fill) +
geom_boxplot(data=gran4, aes(x=download_time, y="4"), fill=boxplot_fill) +
geom_boxplot(data=gran6, aes(x=download_time, y="6"), fill=boxplot_fill)+
geom_boxplot(data=gran12, aes(x=download_time, y="12"), fill=boxplot_fill)+
geom_boxplot(data=gran24, aes(x=download_time, y="24"), fill=boxplot_fill)+
geom_boxplot(data=gran48, aes(x=download_time, y="48"), fill=boxplot_fill) + 
  geom_segment(aes(x=0, xend=-96, yend="FaaS", y="FaaS"), size=4, color=bar_fill) + 
  geom_segment(aes(x=0, xend=-48, yend="2", y="2"), size=4, color=bar_fill) + 
  geom_segment(aes(x=0, xend=-24, yend="4", y="4"), size=4, color=bar_fill) + 
  geom_segment(aes(x=0, xend=-16, yend="6", y="6"), size=4, color=bar_fill) + 
  geom_segment(aes(x=0, xend=-6, yend="12", y="12"), size=4, color=bar_fill) + 
  geom_segment(aes(x=0, xend=-4, yend="24", y="24"), size=4, color=bar_fill) + 
  geom_segment(aes(x=0, xend=-2, yend="48", y="48"), size=4, color=bar_fill) +
  # for both horizontal sides, i want two labels: one at left side and other at right side
  ylab("Granularity") + theme(plot.title = element_text(hjust = 0.5)) + 
  xlab("Download size                        Download time") + 
  theme(text = element_text(family = "Linux Libertine", size=10)) +
    # quit minor ticks in x axis
    theme(panel.grid.minor.x = element_blank()) 

ggsave(
  filename = "download-paper.pdf", 
  plot = g, 
  device = cairo_pdf, 
  width = 83, 
  height = 35,
  units = "mm"
)


