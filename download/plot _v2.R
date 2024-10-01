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

print(max(gran48$download_time))
print(max(gran1$download_time))

custom_transform <- function(x) {
  ifelse(x<0, x, 4.8*x)
}

custom_trans <- trans_new(name = "custom", transform = custom_transform, inverse = function(x) x)

ggplot() + scale_y_discrete(limits=c("1", "2", "4", "6", "12", "24", "48")) +
# i want a continuous x axis, with 0 value at center (left side limit -96, right side limit 20)
# is very important that 0 value is at center of x space in plot(notice that different steps are used for each side)
scale_x_continuous() +
  theme_minimal() + 
  geom_boxplot(data=gran1, aes(x=download_time, y="1"), fill="#f8766d", outlier.size = 0.2) +
geom_boxplot(data=gran2, aes(x=download_time, y="2"), fill=boxplot_fill) +
geom_boxplot(data=gran4, aes(x=download_time, y="4"), fill=boxplot_fill) +
geom_boxplot(data=gran6, aes(x=download_time, y="6"), fill=boxplot_fill)+
geom_boxplot(data=gran12, aes(x=download_time, y="12"), fill=boxplot_fill)+
geom_boxplot(data=gran24, aes(x=download_time, y="24"), fill=boxplot_fill)+
geom_boxplot(data=gran48, aes(x=download_time, y="48"), fill=boxplot_fill, outlier.size = 0.2) + 
  # for both horizontal sides, i want two labels: one at left side and other at right side
  ylab("Granularity")  + 
  xlab("Download time") + 
  theme(text = element_text(family = "Linux Libertine")) +
    # quit minor ticks in x axis
    theme(panel.grid.minor.x = element_blank(), panel.grid.major.y = element_blank()) 


