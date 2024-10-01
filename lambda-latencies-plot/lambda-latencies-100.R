library(ggplot2)
library(ggthemes)

# I will a chart that have got:
#  - x-axis: categories:
#       - AWS Lambda 256 MB
#       - AWS Lambda 10240 MB
#       - GCP Functions 256 MB
#       - GCP Functions 8192 MB
# each category will have a boxplot with the distribution of (worker_start_tstamp - host_job_create_tstamp)

set1 <- read.csv("100func-single256.csv", header=TRUE, sep=",")
set2 <- read.csv("100func-biglambda.csv", header=TRUE, sep=",")
set3 <- read.csv("result-100-256MB.csv", header=TRUE, sep=",")
set4 <- read.csv("result-100-8192MB.csv", header=TRUE, sep=",")

ggplot() + 
  scale_x_discrete(limits=c("AWS Lambda 256 MB", "AWS Lambda 10240 MB", "GCP Functions 256 MB", "GCP Functions 8192 MB")) +
  scale_y_continuous() + 
  geom_boxplot(data=set1, aes(y=worker_func_start_tstamp - host_job_create_tstamp, x="AWS Lambda 256 MB", fill="1")) +
  geom_boxplot(data=set2, aes(y=worker_func_start_tstamp - host_job_create_tstamp, x="AWS Lambda 10240 MB", fill="2")) +
  geom_boxplot(data=set3, aes(y=worker_func_start_tstamp - host_job_create_tstamp, x="GCP Functions 256 MB", fill="4")) +
  geom_boxplot(data=set4, aes(y=worker_func_start_tstamp - host_job_create_tstamp, x="GCP Functions 8192 MB", fill="6")) +
  xlab("Function type") +
  ylab("Startup time (s)") +
  ggtitle("FaaS startup times") +
  theme_linedraw() + 
  theme(plot.title = element_text(hjust = 0.5), legend.position = "none") + 
#   set title 10px
    theme(plot.title = element_text(size=10)) +
    theme(axis.text.x = element_text(angle=90))
    # set axis title 8px
    theme(axis.title.x = element_text(size=8), axis.title.y = element_text(size=8)) + 
    # quit horizontal grid
    theme(panel.grid.major.y = element_blank(), panel.grid.minor.y = element_blank())
    # rotate x ticks labels
    
  


