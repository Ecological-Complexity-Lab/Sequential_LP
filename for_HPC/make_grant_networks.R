# this script reads the database, and agregates networks that might be relevat
# to use the results later for the ISF grant

# --- includes ---------------------------------------------------------------
library(tidyverse)

# --- constants --------------------------------------------------------------
# read database
database_path <- "for_HPC/OIK-07303_database.csv"

# We know there are 30 studies in this database
# after checking the structure of each netrwork,
# we found the following as potential networks to be used:

# CaraDonna2017: 106 layers.
# Fang2016:      147 layers.
# MacLeod2016:   185 layers.
# Petanidou2008: 347 layers.
# Rasmussen2013: 106 layers.

# --- functions -------------------------------------------------------------
save_in_lp_format <- function(netwk, name){
  # function that gets a network and saves it in the right format
  nodes <- unique(c(netwk$lower, netwk$higher))
  nodes <- tibble(name=nodes, ID=1:length(nodes))

  #save only layers with more then one edge
  layers <- netwk %>% group_by(cdate) %>% summarise(n=n()) %>% 
    filter(n>1) %>% arrange(cdate) 
  layers$id <- 1:nrow(layers)

  # make ID only networks
  with_ids <- netwk %>%
    left_join(nodes, by=c("lower" ="name")) %>%
    left_join(nodes, by=c("higher"="name")) %>%
    left_join(layers, by=c("cdate")) %>%
    select(layer=id, from=ID.x, to=ID.y) %>%
    drop_na() # remove edges from layers with only one edge

  # save the network
  write_csv(with_ids, paste(name, ".csv", sep=""))
}

# --- main ------------------------------------------------------------------
data <- read.csv(database_path)

## CaraDonna2017: -----------------------------------------------------------
# Start with CaraDonna2017: 106 layers. 1 site.
name <- "CaraDonna2017"
study <- data %>% filter(study==name)
study %>% group_by(cdate) %>% summarise(n=n()) # not alot of edges per layer

print(unique(study$cdate))

# 3 years, 4 months in each year. sample in a year: 2013->33, 2014->34, 2015->41
# --> take the first 30 layers of each year?
# ----> aggregate by 2, 5, 10.

# prepare the data to be run in the top-seq-lp (Xie's tool)
study %>% select(cdate, lower, higher)

