library(dplyr)
library(ggplot2)
library(shiny)
library(viridis)




# read data from file
df <- read.csv("https://raw.githubusercontent.com/esteban-data-enthusiast/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv")


# define the User Interface
ui <- fluidPage(title = "DATA608 Assignment 3",
  
  tabsetPanel(
  
    tabPanel(title = "QUESTION 1",
    
      tags$div(class="q1",
               tags$h3("DATA608 Assignment 3 - Question 1"),
               tags$h4('By: Esteban Aramayo'),
               tags$p("As a researcher, you frequently compare mortality rates from particular causes across
      different States. You need a visualization that will let you see (for 2010 only) the crude
      mortality rate, across all States, from one cause (for example, Neoplasms, which are
      effectively cancers). Create a visualization that allows you to rank States by crude mortality
      for each cause of death.")),
      headerPanel('CDC Mortality Causes Explorer'),
      sidebarPanel(
        selectInput('year', 'Year', unique(df$Year), selected = 2010),
        selectInput('cause', 'Death Cause', unique(df$ICD.Chapter), selected='Neoplasms'),
      ),
      mainPanel(
        plotOutput('plot1', height = "600px")
      )
    
    ),
    
    tabPanel(title = "QUESTION 2",
             
             tags$div(class="q1",
                      tags$h3("DATA608 Assignment 3 - Question 2"),
                      tags$h4('By: Esteban Aramayo'),
                      tags$p("Often you are asked whether particular States are improving their mortality rates (per cause)
faster than, or slower than, the national average. Create a visualization that lets your clients
see this for themselves for one cause of death at the time. Keep in mind that the national
average should be weighted by the national population.")),
             headerPanel('CDC Crude Mortality Rate Across All US States vs National Average'),
      sidebarPanel(
        selectInput('state', 'State', unique(df$State), selected = 'NY'),
        selectInput('cause2', 'Death Cause', unique(df$ICD.Chapter), selected='Neoplasms'),
      ),
      mainPanel(
       plotOutput('plot2', height = "600px")
      )
             
    )
  
  )
)


# define the Server function
server <- function(input, output, session) {
  
  ##############################################################################
  # Question 1
  ##############################################################################
  selectedData <- reactive({
    dfSlice <- df %>%
      filter(Year == input$year, ICD.Chapter == input$cause) %>%
      select(Year, ICD.Chapter, State, Crude.Rate)
  })
  
  
  plotTitle <- reactive({
    pTitle <- paste0('Death Crude Rate for ', input$year, ' for "', input$cause, '" in the US by State')
  })
  
  
  output$plot1 <- renderPlot({
    
    ggplot(selectedData(), aes(x = reorder(State, Crude.Rate), y = Crude.Rate, fill = Crude.Rate)) +
      geom_col(position = position_dodge(), width = 0.6) +
      coord_flip() +
      geom_text(aes(label = Crude.Rate),
                size = 3,
                hjust = -0.5) +
      ggtitle(plotTitle()) +
      xlab("State") +
      ylab("Crude Mortality Rate") +
      theme_minimal() +
      scale_fill_viridis_c()   # add color palette that can also be distinguished by colorblind viewers
    
  })
  
  
  ##############################################################################
  # Question 2
  ##############################################################################
  selectedData2 <- reactive({
    dfSlice2 <- df %>% 
      group_by(Year, ICD.Chapter) %>%
      mutate(US_Population = sum(Population),
             US_Count = sum(Deaths), 
             US.Crude.Rate = (US_Count/US_Population) * 10^5) %>% 
      group_by(Year, ICD.Chapter, State) %>%
      mutate(S_Count = sum(Deaths),
             State.Crude.Rate = (S_Count/Population) * 10^5 ) %>%
      select(ICD.Chapter, State, Year, US.Crude.Rate, State.Crude.Rate) %>% 
      filter(ICD.Chapter == input$cause2, State == input$state)
  })
  
  
  output$plot2 <- renderPlot({
    
    selectedData2() %>% 
      ggplot() +
      geom_col(aes(x = Year, y = State.Crude.Rate, fill = State.Crude.Rate)) +
      xlab("Year") +
      ylab("Crude Mortality Rate") +
      geom_line(aes(x = Year, y = US.Crude.Rate, linetype = "National Average"), col = "red", lwd = 2) +
      theme_minimal() +
      scale_fill_viridis_c()   # add color palette that can also be distinguished by colorblind viewers
  
  })
  
}
  

shinyApp(ui = ui, server = server)

