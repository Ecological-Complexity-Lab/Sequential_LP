# includes:
library(tidyverse)

# check dryad database:

# read
data <- read.csv("for_HPC/OIK-07303_database.csv")

# how many studies?
studies <- unique(data$study)
length(studies) # 30 studies

# get one study
stud1 <- data %>% filter(study=="Alarcon2008")

# how many layers does it have?
length(unique(stud1$cdate)) # 50

# how many sites does it have?
length(unique(stud1$sSite)) # 1

# edges per layer
stud1 %>% group_by(cdate) %>% summarise(n=n()) 

# check layers in each study:
for (st in studies) {
  stud_simthirgn <- data %>% filter(study==st)
  temporal_layers <- length(unique(stud_simthirgn$cdate)) # 50
  print(paste("No. of dates in study '", st, "' : ", temporal_layers, sep = ""))
}


# Choose a small network:
name <- "WinfreeYYc"
small_study <- data %>% filter(study==name)
length(unique(small_study$cdate)) # 8
length(unique(small_study$sSite)) # 1
small_study %>% group_by(cdate) %>% summarise(n=n()) 

# prepare the data to be run in the top-seq-lp (Xie's tool)
small_study %>% select(cdate, lower, higher)

nodes <- unique(c(small_study$lower, small_study$higher))
nodes <- tibble(name=nodes, ID=1:length(nodes))

#save only layers with more then one edge
layers <- small_study %>% group_by(cdate) %>% summarise(n=n()) %>% 
  filter(n>1) %>% arrange(cdate) 
layers$id <- 1:nrow(layers)

# make ID only networks
with_ids <- small_study %>%
  left_join(nodes, by=c("lower" ="name")) %>%
  left_join(nodes, by=c("higher"="name")) %>%
  left_join(layers, by=c("cdate")) %>%
  select(layer=id, from=ID.x, to=ID.y) %>%
  drop_na() # remove edges from layers with only one edge

# save 
write_csv(with_ids, "WinfreeYYc_mln.csv")