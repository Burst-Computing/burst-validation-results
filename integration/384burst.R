library(ggplot2)
library(patchwork)

classic = read.csv("terasort-classic3.csv")
classic$start_map <- (classic$init_fn_map - min(classic$init_fn_map)) / 1000
classic$end_map <- (classic$end_fn_map - min(classic$init_fn_map)) / 1000
classic$start_reduce <- (classic$init_fn_reduce - min(classic$init_fn_map)) / 1000
classic$end_reduce <- (classic$end_fn_reduce - min(classic$init_fn_map)) / 1000
classic$pre_shuffle <- (classic$pre_upload_map - min(classic$init_fn_map)) / 1000
classic$post_shuffle <- (classic$post_download_reduce - min(classic$init_fn_map)) / 1000
classic$post_download_map <- (classic$post_download_map - min(classic$init_fn_map)) / 1000
classic$pre_upload_reduce <- (classic$pre_upload_reduce - min(classic$init_fn_map)) / 1000


burst = read.csv("terasort-burst2.csv")
burst$start <- (burst$init_fn - min(burst$init_fn)) / 1000
burst$end <- (burst$end_fn - min(burst$init_fn)) / 1000
burst$pre_shuffle <- (burst$pre_shuffle - min(burst$init_fn)) / 1000
burst$post_shuffle <- (burst$post_shuffle - min(burst$init_fn)) / 1000
burst$post_download <- (burst$post_download - min(burst$init_fn)) / 1000
burst$pre_upload <- (burst$pre_upload - min(burst$init_fn)) / 1000

g_classic <- ggplot(classic) +
    scale_x_continuous(limits=c(0,150)) + 
    geom_segment(aes(x=start_map, xend=end_map, y=fn_id, yend=fn_id, color="Compute time"), size=0.3) +
    geom_segment(aes(x=start_reduce, xend=end_reduce, y=fn_id, yend=fn_id, color="Compute time"), size=0.3) +
    geom_segment(aes(x=pre_shuffle, xend=post_shuffle, y=fn_id, yend=fn_id, color="Shuffle communication"), size=0.3) +
    geom_segment(aes(x=start_map, xend=post_download_map, y=fn_id, yend=fn_id, color="S3 download/upload"),  size=0.3) +
    geom_segment(aes(x=pre_upload_reduce, xend=end_reduce, y=fn_id, yend=fn_id, color="S3 download/upload"), size=0.3) +
    scale_color_manual(values=c("black", "orange2", "green2")) + 
    xlab("Wallclock time (s)") + ylab("# activation") + 
    theme_minimal() + theme(text = element_text(family = "Linux Libertine"), legend.position = "top", legend.direction ="vertical", legend.title = element_blank(), legend.margin = margin(0))

g_burst <- ggplot(burst) +
    scale_x_continuous(limits=c(0,150)) +
    geom_segment(aes(x=start, xend=end, y=fn_id, yend=fn_id, color="Compute time"), size=0.3) +
    geom_segment(aes(x=pre_shuffle, xend=post_shuffle, y=fn_id, yend=fn_id, color = "Shuffle communication"), size=0.3) +
    geom_segment(aes(x=start, xend=post_download, y=fn_id, yend=fn_id, color="S3 download/upload"), size=0.3) +
    geom_segment(aes(x=pre_upload, xend=end, y=fn_id, yend=fn_id, color="S3 download/upload"), size=0.3) +
    scale_color_manual(values=c("black", "orange2", "green2")) + 
    xlab("Wallclock time (s)") + ylab("# activation") + 
    theme_minimal() + theme(text = element_text(family = "Linux Libertine"), legend.position = "none")





