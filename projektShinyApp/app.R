#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(tidyverse)
library(plotly)
library(shiny)
library(dplyr)
library(ggplot2)
library(gapminder)
library(gganimate)

system("HENT VORES CSV FILER UD HER")

library(readr)
persistentTemperature <- read_csv("persistentTemperature.csv")

persistentTweets <- read_csv("persistentTweets.csv")

temperature <- read_csv("temperature.csv")
tweets <- read_csv("tweets.csv")


# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("Visualization of tweets and temperature data"),

    # Sidebar with a slider input for number of bins 
    

        # Show a plot of the generated distribution
        mainPanel(
          plotlyOutput("plOlivert1")
          
        )
    )


# Define server logic required to draw a histogram
server <- function(input, output) {

  output$plOlivert1 <- renderPlotly({
    p <- ggplot(persistentTemperature, aes(y = temperature, x = date, ))
    p <- p + geom_point()
    p <- p + labs(y = "Temp", x = "Date")
    
    ggplotly(p)
  }
)
}



# Run the application 
shinyApp(ui = ui, server = server)
