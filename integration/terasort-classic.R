library(ggplot2)
library(gridExtra)

classic = read.csv("16-terasort-classic.csv")
classic$start_map <- classic$init_fn_map - min(classic$host_submit_map)
classic$end_map <- classic$end_fn_map - min(classic$host_submit_map)
classic$start_reduce <- classic$init_fn_reduce - min(classic$host_submit_map)
classic$end_reduce <- classic$end_fn_reduce - min(classic$host_submit_map)
classic$pre_shuffle <- classic$pre_upload_map - min(classic$host_submit_map)
classic$post_shuffle <- classic$post_download_reduce - min(classic$host_submit_map)


burst = read.csv("16-terasort-burst.csv")
burst$start <- burst$init_fn - min(burst$host_submit)
burst$end <- burst$end_fn - min(burst$host_submit)
burst$pre_shuffle <- burst$pre_shuffle - min(burst$host_submit)
burst$post_shuffle <- burst$post_shuffle - min(burst$host_submit)

# i want a plot that shows the time in X axis and the number of row in Y axis
# for each row:
#   - a segment from init_fn_map to end_fn_map
#   - a segment from init_fn_reduce to end_fn_reduce

g_classic <- ggplot(classic) +
  scale_x_continuous() + 
    geom_segment(aes(x=start_map, xend=end_map, y=fn_id, yend=fn_id), size=2, color="black") +
    geom_segment(aes(x=start_reduce, xend=end_reduce, y=fn_id, yend=fn_id), size=2, color="black") +
        geom_segment(aes(x=pre_shuffle, xend=post_shuffle, y=fn_id, yend=fn_id), size=2.2, color="green") +
  xlab("Classic") + ylab("# activation") + 
    theme_minimal()

g_burst <- ggplot(burst) +
  scale_x_continuous() +
    geom_segment(aes(x=start, xend=end, y=fn_id, yend=fn_id), color="black", size=2) +
    geom_segment(aes(x=pre_shuffle, xend=post_shuffle, y=fn_id, yend=fn_id), size=2.2, color="green") +
    xlab("Burst") + ylab("# activation") + 
    theme_minimal()

# grid arrange
g <- grid.arrange(g_classic, g_burst, ncol=2, top="Terasort 1GB - 16 workers")




