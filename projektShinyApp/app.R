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
system("sudo microk8s kubectl cp ubuntuconsumer:copyTest/temperature.csv temperature.csv
")
system("sudo microk8s kubectl cp ubuntuconsumer:copyTest/tweets.csv tweets.csv
")
system("sudo microk8s kubectl cp ubuntuconsumer:copyTest/persistentTemperature.csv persistentTemperature.csv
")
system("sudo microk8s kubectl cp ubuntuconsumer:copyTest/persistentTweets.csv persistentTweets.csv
")
persistentTemperature <- read_csv("persistentTemperature.csv")

persistentTweets <- read_csv("persistentTweets.csv")

temperature <- read_csv("temperature.csv")
tweets <- read_csv("tweets.csv")

colnames(persistentTemperature)
colnames(persistentTweets)

colnames(temperature)
colnames(tweets)



# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("Visualization of tweets and temperature data"),

    # Sidebar with a slider input for number of bins 
    

        # Show a plot of the generated distribution
        mainPanel(
          plotOutput("plOlivert1"),
          plotOutput("plOlivert2"),
          plotOutput("plOlivert3"),
          plotOutput("plOlivert4")
          
          
        )
    )


# Define server logic required to draw a histogram
server <- function(input, output) {
  

  output$plOlivert1 <- renderPlot({
    p <- ggplot(persistentTemperature, aes(y = temperature, x = date, ))
    p <- p + geom_point()
    p <- p + labs(y = "Temp", x = "Date")
    
    plot(p)
  }
)
  output$plOlivert2 <- renderPlot({

    # draw the histogram with the specified number of bins
    #hist(persistentTweets, col = 'darkgray', border = 'white')
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
   
    
    p <- ggplot(tweets) +
      geom_histogram(aes(x = tweets)) +
      scale_x_date(labels = date_format("%m %d %Y"), date_breaks = "30 days") +
      theme(legend.position = "bottom",
            axis.text.x = element_text(angle = 45, hjust = 1))
  plot(p)
    }
  )
  
}



# Run the application 
shinyApp(ui = ui, server = server)
