# this script reads the database, and agregates networks that might be relevat
# to use the results later for the ISF grant

# --- includes ---------------------------------------------------------------
library(tidyverse)
library(reshape2)

# --- constants --------------------------------------------------------------
# read database
database_path <- "for_HPC/input/OIK-07303_database.csv"

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

unique(study$cdate)

#remove unneeded columns
study <- study %>% select(cdate, lower, higher)

# 3 years, 4 months in each year. sample in a year: 2013->33, 2014->34, 2015->39
# --> take the first 30 layers of each year?
# ----> aggregate by 10.

# divide the data into years
study$date <- as.Date(study$cdate, format="%Y-%m-%d")

# 2013
study_2013 <- study %>% filter(year(date) == 2013)
# ignore last 3 layers so we have dividable number of layers
study_2013 <- study_2013 %>% filter(date < as.Date("2013-08-15"))

# 2014
study_2014 <- study %>% filter(year(date) == 2014)
# ignore last 4 layers
study_2014 <- study_2014 %>% filter(date < as.Date("2014-08-28"))

# 2015
study_2015 <- study %>% filter(year(date) == 2015)
# ignore last 9 layers
study_2015 <- study_2015 %>% filter(date < as.Date("2015-08-05"))

length(unique(study_2015$cdate))

# turn back to a single network
study_dividable <- rbind(study_2013, study_2014, study_2015)

num_to_agg <- 10
# aggregate layers by 2
dates <- unique(study_dividable$cdate) %>% sort()
#new_layer_id <- length(dates)/num_to_agg
group_id <- 1

complete_new_network <- NULL
for(i in seq(1, length(dates), by = num_to_agg)){
  agg_group <- dates[i:(i+num_to_agg-1)]

  # filter all the rows that belong to the group
  group <- study_dividable %>% filter(cdate %in% agg_group)

  # remove duplicates
  group_edges <- group %>% select(lower, higher) %>% distinct()

  # add group id
  group_edges$cdate <- group_id
  group_id <- group_id + 1

  complete_new_network <- rbind(complete_new_network, group_edges)
}
# prepare the network for runnings
save_in_lp_format(complete_new_network, "CaraDonna2017_aggregated")

## smaller networks: ----------------------------------------------------------
# First: WinfreeYYc exists already (for_HPC/WinfreeYYc_mln.csv)

# Second: Lara-Romero2016
name <- "Lara-Romero2016"
study <- data %>% filter(study==name)
study %>% group_by(cdate) %>% summarise(n=n())
unique(study$sSite) # 2 sites

study %>% filter(sSite == "nevero") %>% count(cdate) # site 1 has 10 dates
study %>% filter(sSite == "penalara") %>% count(cdate) # site 2 has 12 dates

# take layers from only site 2
half_study <- study %>% filter(sSite == "penalara")

# make sure all layers have edges
half_study %>% group_by(cdate) %>% summarise(n=n())

# remove unneeded columns
half_study <- half_study %>% select(cdate, lower, higher)

# prepare the network for runnings
save_in_lp_format(half_study, "Lara_Romero2016_penalara")

## process results produced by python script: ----------------------------------
# read the csv file with the results
results <- read_csv("results/grant_sweep.csv")

# make a tile plot using ggplot
results %>%
  filter(study == "CaraDonna2017_aggregated") %>%
  select(-study, -precision, -recall) %>%
  melt(id=c("q", "u")) %>%
  ggplot(aes(x=q, y=u, fill=value)) +
  geom_tile() +
  scale_fill_gradientn(values=c(0, .2, .5, .8, 1), 
                       colours=c("#BE2A3E", "#EC754A", "#F5CA63", "#7AAF60", "#22763F"))+
  facet_wrap(~variable) + ggtitle("CaraDonna2017_aggregated")

results %>%
  filter(study == "Lara_Romero2016_penalara") %>%
  select(-study, -precision, -recall) %>%
  melt(id=c("q", "u")) %>%
  ggplot(aes(x=q, y=u, fill=value)) +
  geom_tile() +
  scale_fill_gradientn(values=c(0, .2, .5, .8, 1), 
                       colours=c("#BE2A3E", "#EC754A", "#F5CA63", "#7AAF60", "#22763F"))+
  scale_x_continuous(breaks = 2:10) +
  scale_y_continuous(breaks = 3:11) +
  facet_wrap(~variable) + ggtitle("Lara_Romero2016_penalara")

results %>%
  filter(study == "WinfreeYYc_mln") %>%
  select(-study, -precision, -recall) %>%
  melt(id=c("q", "u")) %>%
  ggplot(aes(x=q, y=u, fill=value)) +
  geom_tile() +
  scale_fill_gradientn(values=c(0, .2, .5, .8, 1), 
                       colours=c("#BE2A3E", "#EC754A", "#F5CA63", "#7AAF60", "#22763F"))+
  facet_wrap(~variable) + ggtitle("WinfreeYYc_mln")
