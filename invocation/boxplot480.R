library(ggplot2)
library(ggthemes)

# I will a chart that have got:
#  - x-axis: lapse time in seconds
#  - y-axis: categories (1,2,4,6,12,24,48)
# each category will have a boxplot with the distribution of (worker_start_tstamp - host_job_create_tstamp)
# each caterogy is in a different file gran{1|2|4|6|12|24|48}.csv

gran1 <- read.csv("480/gran1.csv", header=TRUE, sep=",")
gran2 <- read.csv("480/gran2.csv", header=TRUE, sep=",")
gran4 <- read.csv("480/gran4.csv", header=TRUE, sep=",")
gran6 <- read.csv("480/gran6.csv", header=TRUE, sep=",")
gran12 <- read.csv("480/gran12.csv", header=TRUE, sep=",")
gran24 <- read.csv("480/gran24.csv", header=TRUE, sep=",")
gran48 <- read.csv("480/gran48.csv", header=TRUE, sep=",")

ggplot() + 
  scale_y_discrete(limits=c("1", "2", "4", "6", "12", "24", "48")) +
  scale_x_continuous(limits=c(0,10)) + 
  geom_boxplot(data=gran1, aes(x=worker_start_tstamp - host_job_create_tstamp, y="1", fill="1"), outlier.size = 0.8) +
  geom_boxplot(data=gran2, aes(x=worker_start_tstamp - host_job_create_tstamp, y="2", fill="2")) +
  geom_boxplot(data=gran4, aes(x=worker_start_tstamp - host_job_create_tstamp, y="4", fill="4")) +
  geom_boxplot(data=gran6, aes(x=worker_start_tstamp - host_job_create_tstamp, y="6", fill="6")) +
  geom_boxplot(data=gran12, aes(x=worker_start_tstamp - host_job_create_tstamp, y="12", fill="12")) +
  geom_boxplot(data=gran24, aes(x=worker_start_tstamp - host_job_create_tstamp, y="24", fill="24")) +
  geom_boxplot(data=gran48, aes(x=worker_start_tstamp - host_job_create_tstamp, y="48", fill="48")) +
  xlab("Startup time") +
  ylab("Granularity") +
  ggtitle("burst_size = 480") +
  theme_linedraw() + 
  theme(plot.title = element_text(hjust = 0.5), legend.position = "none") + 
#   set title 10px
    theme(plot.title = element_text(size=10)) +
    # set axis title 8px
    theme(axis.title.x = element_text(size=8), axis.title.y = element_text(size=8)) + 
    # quit horizontal grid
    theme(panel.grid.major.y = element_blank(), panel.grid.minor.y = element_blank()) 
  


