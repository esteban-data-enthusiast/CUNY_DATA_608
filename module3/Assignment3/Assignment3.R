library(dplyr)
library(ggplot2)
library(shiny)
library(viridis)

# Question 1:
# 
# As a researcher, you frequently compare mortality rates from particular causes across
# different States. You need a visualization that will let you see (for 2010 only) the crude
# mortality rate, across all States, from one cause (for example, Neoplasms, which are
# effectively cancers). Create a visualization that allows you to rank States by crude mortality
# for each cause of death.


# read data from file
df <- read.csv("https://raw.githubusercontent.com/esteban-data-enthusiast/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv")

# filter the data for year 2010 only
df_2010 <- df %>%
  filter(Year == 2010) %>%
  select(ICD.Chapter, State, Crude.Rate)

# built unique list of death causes sorted in ascending order
df_death_causes <- df_2010 %>%
  dplyr::select(ICD.Chapter) %>%
  dplyr::distinct(ICD.Chapter) %>%
  dplyr::arrange(ICD.Chapter)



# death_cause <- "Diseases of the circulatory system"
death_cause <- "Neoplasms"
# death_cause <- "Diseases of the genitourinary system"

plotTitle <- paste0('Death Crude Rate for "', chosen_death_cause, '" in the US by State')

# plot 
df_2010 %>%
  filter(ICD.Chapter == death_cause) %>%
ggplot(aes(x = reorder(State, Crude.Rate), y = Crude.Rate, fill = Crude.Rate)) +
  geom_col(position = position_dodge(), width = 0.6) +
  coord_flip() +
  geom_text(aes(label = Crude.Rate),
            size = 2,
            hjust = -0.5) +
  ggtitle(plotTitle) +
  xlab("State") +
  ylab("Crude Rate") +
  theme_minimal() +
  scale_fill_viridis_c()   # add color palette that can also be distinguished by colorblind viewers
  



# ui <- fluidPage()
# 
# server <- function(input, output) {}
# 
# shinyApp(ui = ui, server = server)
# 
