#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(RJDBC)


#SKAL BRUGE CDATA DRIVER SOM SKAL DOWNLOADES OG SMIDES OVER PÅ VM POTENTIELT IDK HVORDAN DET VIRKER XD
#



#data <- read.df("hdfs://simple-hdfs-namenode-default-0.simple-hdfs-namenode-default:8020/weather-report.avro", "avro")

# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("Old Faithful Geyser Data"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
            sliderInput("bins",
                        "Number of bins:",
                        min = 1,
                        max = 50,
                        value = 30)
        ),

        # Show a plot of the generated distribution
        mainPanel(
           plotOutput("distPlot")
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {

    output$distPlot <- renderPlot({
        # generate bins based on input$bins from ui.R
        x    <- faithful[, 2]
        bins <- seq(min(x), max(x), length.out = input$bins + 1)

        # draw the histogram with the specified number of bins
        hist(x, breaks = bins, col = 'darkgray', border = 'white',
             xlab = 'Waiting time to next eruption (in mins)',
             main = 'Histogram of waiting times')
    })
    print('Lavede connections')
    kafka_driver <- JDBC(driverClass = "cdata.jdbc.apachekafka.ApacheKafkaDriver", classPath = "ApacheKafkaJDBCDriver/lib/cdata.jdbc.apachekafka.jar", identifier.quote = "'")
    kafka_conn <- dbConnect(kafka_driver,"jdbc:apachekafka:BootStrapServers=https://strimzi-kafka-bootstrap:9092;Topic=INGESTION_TWEETS;")
    dbListTables(kafka_conn)
    
    avro_driver <- JDBC(driverClass = "cdata.jdbc.avro.AvroDriver", classPath = "AvroJDBCDriver/lib/cdata.jdbc.avro.jar", identifier.quote = "'")
    avro_conn <- dbConnect(avro_driver,"jdbc:avro:URI=hdfs://simple-hdfs-namenode-default-0.simple-hdfs-namenode-default:8020/tweets.avroInitiateOAuth=GETANDREFRESH")
    dbListTables(avro_conn)
}

# Run the application 
shinyApp(ui = ui, server = server)
