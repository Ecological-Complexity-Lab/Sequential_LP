# this script reads the database from dryad and explores it a bit.
# then prepares the data of one network to be run in the top-seq-lp (Xie's tool)

# includes:
library(tidyverse)

# explore dryad database: -----------------------------------------------

# read
data <- read.csv("for_HPC/input/OIK-07303_database.csv")

# how many studies?
studies <- unique(data$study)
length(studies) # 30 studies

# get one study
stud1 <- data %>% filter(study == "Alarcon2008")

# how many layers does it have?
length(unique(stud1$cdate)) # 50

# how many sites does it have?
length(unique(stud1$sSite)) # 1

# edges per layer
stud1 %>% group_by(cdate) %>% summarise(n=n()) 

# check layers in each study:
for (st in studies) { 
  stud_simthirgn <- data %>% filter(study == st)
  temporal_layers <- length(unique(stud_simthirgn$cdate)) # 50
  sited_in_study <- length(unique(stud_simthirgn$sSite)) # 50
  print(paste("dates in study '", st, "' : ", temporal_layers, ". sites :", sited_in_study , sep = ""))
}

# prepare a small network in the right format: ----------------------------
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
