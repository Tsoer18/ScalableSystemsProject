#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(dplyr)
library(ggplot2)
library(scales)



library(readr)




# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("Visualization of tweets and temperature data"),

    # Sidebar with a slider input for number of bins 
    

        # Show a plot of the generated distribution
        mainPanel(
          titlePanel("Persistent temperature data"),
          plotOutput("plOlivert1"),
          titlePanel("Persistent tweet data"),
          plotOutput("plOlivert2"),
          titlePanel("Recent temperature data"),
          plotOutput("plOlivert3"),
          titlePanel("Recent tweet data"),
          plotOutput("plOlivert4")
          
          
        )
    )


# Define server logic required to draw a histogram
server <- function(input, output) {
  system("sudo microk8s kubectl cp ubuntu-recent-temp:copyTest/temperature.csv temperature.csv
")
  system("sudo microk8s kubectl cp ubuntu-recent-tweet:copyTest/tweets.csv tweets.csv
")
  system("sudo microk8s kubectl cp ubuntu-persist-temp:copyTest/persistentTemperature.csv persistentTemperature.csv
")
  system("sudo microk8s kubectl cp ubuntu-persist-tweet:copyTest/persistentTweets.csv persistentTweets.csv
")
  persistentTemperature <- read_csv("persistentTemperature.csv")
  
  persistentTweets <- read_csv("persistentTweets.csv")
  
  temperature <- read_csv("temperature.csv")
  tweets <- read_csv("tweets.csv")
  
  colnames(persistentTemperature)
  colnames(persistentTweets)
  
  colnames(temperature)
  colnames(tweets)
  

  output$plOlivert1 <- renderPlot({
    p <- ggplot(persistentTemperature, aes(y = temperature, x = date, ))
    p <- p + geom_point()
    p <- p + labs(y = "Temp", x = "Date")
    
    plot(p)
  }
)
  output$plOlivert2 <- renderPlot({

    # draw the histogram with the specified number of bins
    p <-ggplot(persistentTweets, aes(date)) +
      geom_histogram()
    
    plot(p)
  }
  )
  output$plOlivert3 <- renderPlot({
    p <- ggplot(temperature, aes(y = temperature, x = date, ))
    p <- p + geom_point()
    p <- p + labs(y = "Temp", x = "Date")
    
    plot(p)
  }
  )
  output$plOlivert4 <- renderPlot({
    # draw the histogram with the specified number of bins
   
    
    p <-ggplot(tweets, aes(date)) +
      geom_histogram()
  
    plot(p)
  }
  )
  
}



# Run the application 
shinyApp(ui = ui, server = server)
