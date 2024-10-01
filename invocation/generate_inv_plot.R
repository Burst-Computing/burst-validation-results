
library(ggplot2)
library(ggthemes)

generate_inv_plot <- function(size) {

filename = paste("960/gran", size, ".csv", sep='')
df <- read.csv(filename, header=TRUE, sep=",")
# rename column worker_start_tstamp to start
df$start <- df$worker_start_tstamp - min(df$host_job_create_tstamp)
df$end <- df$worker_end_tstamp - min(df$host_job_create_tstamp)
df$submit <- df$host_job_create_tstamp - min(df$host_job_create_tstamp)


df2 <- data.frame(start=seq(0, max(df$end)+1, 0.01))
df2$concurrent <- sapply(df2$start, function(x) sum(df$start <= x & df$end >= x))
# order by hostname and after by start
df <- df[order(df$hostname, df$start),]


max_start <- max(df$start)
max_start_index <- which.max(df$start)

#make that each 4 hostnames the color will be the same (4 colors) Ex: red = 0,4,8,12...; blue = 1,5,9,13...; green = 2,6,10,14...; yellow = 3,7,11,15...
# setting hostname = hostname %% 4
df$hostname <- df$hostname %% 4
df$hostname <- as.factor(df$hostname)


# create or overwrite id column wth numbers from 0 to n-1
df$id <- seq.int(nrow(df))-1


g <- ggplot(df, aes(y=id))
g <- g + scale_x_continuous(limits=c(0, 25))
g <- g + geom_segment(size=0.2, aes(xend=end, x=start, yend=id, color=hostname))
g <- g + geom_line(data=df2, aes(x=start, y=concurrent), color="black", size=0.6)
g <- g + geom_point(x=max_start, y=max_start_index, color="black", fill="green", size=1.4, shape=23)
print(max_start)
#set linux libertine font
g <- g + theme_minimal() + scale_color_manual(values=rev(c("#e66101", "#fdb863", "#b2abd2", "#5e3c99")))
#quitar las lineas horizontal del grid (las verticales dejarlas)
g <- g + theme(panel.grid.major.y = element_blank(), panel.grid.minor.y = element_blank())
g <- g + labs(x = NULL, y = NULL) 
g <- g + theme(text = element_text(family = "Linux Libertine"), legend.position = "none")
return(g)
}
