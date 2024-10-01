generate_boxplot <- function(size) {

gran1 <- read.csv(paste(size, "/gran1.csv", sep=''), header=TRUE, sep=",")
gran2 <- read.csv(paste(size, "/gran2.csv", sep=''), header=TRUE, sep=",")
gran4 <- read.csv(paste(size, "/gran4.csv", sep=''), header=TRUE, sep=",")
gran6 <- read.csv(paste(size, "/gran6.csv", sep=''), header=TRUE, sep=",")
gran12 <- read.csv(paste(size, "/gran12.csv", sep=''), header=TRUE, sep=",")
gran24 <- read.csv(paste(size, "/gran24.csv", sep=''), header=TRUE, sep=",")
gran48 <- read.csv(paste(size, "/gran48.csv", sep=''), header=TRUE, sep=",")

g <- ggplot() + 
  scale_y_discrete(limits=c("FaaS", "2", "4", "6", "12", "24", "48")) +
  scale_x_continuous(limits=c(0,22)) + 
  geom_boxplot(data=gran1, aes(x=worker_start_tstamp - host_job_create_tstamp, y="FaaS", fill="1"), outlier.size = 0.1) +
  geom_boxplot(data=gran2, aes(x=worker_start_tstamp - host_job_create_tstamp, y="2", fill="2")) +
  geom_boxplot(data=gran4, aes(x=worker_start_tstamp - host_job_create_tstamp, y="4", fill="2")) +
  geom_boxplot(data=gran6, aes(x=worker_start_tstamp - host_job_create_tstamp, y="6", fill="2")) +
  geom_boxplot(data=gran12, aes(x=worker_start_tstamp - host_job_create_tstamp, y="12", fill="2")) +
  geom_boxplot(data=gran24, aes(x=worker_start_tstamp - host_job_create_tstamp, y="24", fill="2")) +
  geom_boxplot(data=gran48, aes(x=worker_start_tstamp - host_job_create_tstamp, y="48", fill="2")) +
  #xlab("Startup time (s)") +
  #ylab("Granularity") +
  #disable x and y axis labels
  labs(x = NULL, y = NULL) +
  theme_minimal() + 
  theme(plot.title = element_text(hjust = 0.5), legend.position = "none", text = element_text(family = "Linux Libertine")) + 
#   set title 10px
    theme(plot.title = element_text(size=10)) +
    # set axis title 8px
    theme(axis.title.x = element_text(size=8), axis.title.y = element_text(size=8)) + 
    # quit horizontal grid
    theme(panel.grid.major.y = element_blank(), panel.grid.minor.y = element_blank()) 
  
return(g)
}