library(ggplot2)
library(ggthemes)
library(gridExtra)


set1 <- read.csv("aws-100func-single256.csv", header=TRUE, sep=",")
set2 <- read.csv("aws-100func-biglambda.csv", header=TRUE, sep=",")
set3 <- read.csv("gcp-100-256MB.csv", header=TRUE, sep=",")
set4 <- read.csv("gcp-100-8192MB.csv", header=TRUE, sep=",")

set1.max <- max(set1$worker_func_start_tstamp - set1$host_job_create_tstamp)
set1.min <- min(set1$worker_func_start_tstamp - set1$host_job_create_tstamp)
set2.max <- max(set2$worker_func_start_tstamp - set2$host_job_create_tstamp)
set2.min <- min(set2$worker_func_start_tstamp - set2$host_job_create_tstamp)
set3.max <- max(set3$worker_func_start_tstamp - set3$host_job_create_tstamp)
set3.min <- min(set3$worker_func_start_tstamp - set3$host_job_create_tstamp)
set4.max <- max(set4$worker_func_start_tstamp - set4$host_job_create_tstamp)
set4.min <- min(set4$worker_func_start_tstamp - set4$host_job_create_tstamp)

foo <- rev(c("○", "●"  , "◇" ,"◆"))
           
           
color_vector <- rev(c("orange", "orange", "#4285F4", "#4285F4"))
g0 <- ggplot() + 
  scale_y_discrete(limits=foo, breaks = foo) +
  scale_x_continuous() + 
  geom_bar(stat="identity", aes(y="○", x=set1.max), width=0.5, fill="grey", color="grey",alpha=0.6) +
  geom_bar(stat="identity", aes(y="●", x=set2.max), width=0.5, fill="grey", color="grey",alpha=0.6) +
  geom_bar(stat="identity", aes(y="◇", x=set3.max), width=0.5, fill="grey", color="grey",alpha=0.6) +
  geom_bar(stat="identity", aes(y="◆", x=set4.max), width=0.5, fill="grey", color="grey",alpha=0.6) +
  geom_bar(stat="identity",aes(y="○", x=set1.min), width=0.5, color="grey", fill="white") +
  geom_bar(stat="identity",aes(y="●", x=set2.min), width=0.5, color="grey", fill="white") +
  geom_bar(stat="identity",aes(y="◇", x=set3.min), width=0.5, color="grey", fill="white") +
  geom_bar(stat="identity",aes(y="◆", x=set4.min), width=0.5, color="grey", fill="white") +
  theme(legend.position = 'none') +
  theme_minimal() + 
  theme(axis.text.y = element_text(color=color_vector, size =12, face="bold")) +
  labs(x = NULL, y = NULL) +
  theme(plot.title = element_text(hjust = 0.5), legend.position = "none", text = element_text(family = "Linux Libertine")) + 
  theme(plot.title = element_text(size=10)) +
  theme(axis.title.x = element_text(size=8), axis.title.y = element_text(size=8)) + 
  theme(panel.grid.major.y = element_blank(), panel.grid.minor.y = element_blank()) 

set5 <- read.csv("aws-1000func-single256.csv", header=TRUE, sep=",")
set6 <- read.csv("aws-1000func-biglambda.csv", header=TRUE, sep=",")
set7 <- read.csv("gcp-1000-256MB.csv", header=TRUE, sep=",")
set8 <- read.csv("gcp-1000-8192MB.csv", header=TRUE, sep=",")

set5.max <- max(set5$worker_func_start_tstamp - set5$host_job_create_tstamp)
set5.min <- min(set5$worker_func_start_tstamp - set5$host_job_create_tstamp)
set6.max <- max(set6$worker_func_start_tstamp - set6$host_job_create_tstamp)
set6.min <- min(set6$worker_func_start_tstamp - set6$host_job_create_tstamp)
set7.max <- max(set7$worker_func_start_tstamp - set7$host_job_create_tstamp)
set7.min <- min(set7$worker_func_start_tstamp - set7$host_job_create_tstamp)
set8.max <- max(set8$worker_func_start_tstamp - set8$host_job_create_tstamp)
set8.min <- min(set8$worker_func_start_tstamp - set8$host_job_create_tstamp)

foo <- rev(c("○", "●"  , "◇" ,"◆"))
           
           
color_vector <- rev(c("orange", "orange", "#4285F4", "#4285F4"))
g1 <- ggplot() + 
  scale_y_discrete(limits=foo, breaks = foo) +
  scale_x_continuous() + 
  geom_bar(stat="identity", aes(y="○", x=set5.max), width=0.5, fill="grey", color="grey", alpha=0.6) +
  geom_bar(stat="identity", aes(y="●", x=set6.max), width=0.5, fill="grey", color="grey",alpha=0.6) +
  geom_bar(stat="identity", aes(y="◇", x=set7.max), width=0.5, fill="grey", color="grey",alpha=0.6) +
  geom_bar(stat="identity", aes(y="◆", x=set8.max), width=0.5, fill="grey", color="grey",alpha=0.6) +
  geom_bar(stat="identity",aes(y="○", x=set5.min), width=0.5, color="grey", fill="white") +
  geom_bar(stat="identity",aes(y="●", x=set6.min), width=0.5, color="grey", fill="white") +
  geom_bar(stat="identity",aes(y="◇", x=set7.min), width=0.5, color="grey", fill="white") +
  geom_bar(stat="identity",aes(y="◆", x=set8.min), width=0.5, color="grey", fill="white") +
  theme(legend.position = 'none') +
  theme_minimal() + 
  theme(axis.text.y = element_text(color=color_vector, size =12, face="bold")) +
  labs(x = NULL, y = NULL) +
  theme(plot.title = element_text(hjust = 0.5), legend.position = "none", text = element_text(family = "Linux Libertine")) + 
  theme(plot.title = element_text(size=10)) +
  theme(axis.title.x = element_text(size=8), axis.title.y = element_text(size=8)) + 
  theme(panel.grid.major.y = element_blank(), panel.grid.minor.y = element_blank()) 


grid.arrange(g0, g1, ncol=2,
             bottom=textGrob("Time (s)", gp=gpar(fontsize=10, fontfamily="Linux Libertine")))

