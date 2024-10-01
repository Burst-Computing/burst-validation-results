size <- 960
gran1 <- read.csv(paste(size, "/gran1.csv", sep=''), header=TRUE, sep=",")
gran2 <- read.csv(paste(size, "/gran2.csv", sep=''), header=TRUE, sep=",")
gran4 <- read.csv(paste(size, "/gran4.csv", sep=''), header=TRUE, sep=",")
gran6 <- read.csv(paste(size, "/gran6.csv", sep=''), header=TRUE, sep=",")
gran12 <- read.csv(paste(size, "/gran12.csv", sep=''), header=TRUE, sep=",")
gran24 <- read.csv(paste(size, "/gran24.csv", sep=''), header=TRUE, sep=",")
gran48 <- read.csv(paste(size, "/gran48.csv", sep=''), header=TRUE, sep=",")

iter <- list(gran1, gran2, gran4, gran6, gran12, gran24, gran48)
# index <- list("gran1", "gran2", "gran4", "gran6", "gran12", "gran24", "gran48")

for (x in iter){
  x$lats = x$worker_start_tstamp - min(x$host_job_create_tstamp)
  mad = mean(abs((x$lats -mean(x$lats))))
  iqr = unname(quantile(x$lats, 0.75)) - unname(quantile(x$lats, 0.25))
  idr = unname(quantile(x$lats, 0.9)) - unname(quantile(x$lats, 0.1))
  ar = max(x$lats) - min(x$lats)
  print(c(">>>>>>> ", "<<<<<<<"))
  print(c("Median average deviation: ", mad))
  print(c("Interquantile distance: ", iqr))
  print(c("Interdecile distance : ", idr))
  print(c("Max range: ", ar))
}

