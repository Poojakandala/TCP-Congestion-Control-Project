# ---------- Install and load required packages ----------
if (!require("caret")) install.packages("caret")
if (!require("randomForest")) install.packages("randomForest")
if (!require("ggplot2")) install.packages("ggplot2")
if (!require("shiny")) install.packages("shiny")

library(caret)
library(randomForest)
library(ggplot2)
library(shiny)

# ---------- Set working directory as needed ----------
setwd("E:/TCP_project")

# ---------- Step 1: Load your dataset ----------
df <- read.csv("tcp_network_data.csv")
df$congested <- as.factor(df$congested)
head(df)

# ---------- Step 2: Split into train and test sets (80/20) ----------
set.seed(42)
train_idx <- createDataPartition(df$congested, p = 0.8, list = FALSE)
train_data <- df[train_idx, ]
test_data  <- df[-train_idx, ]
cat("Train:", nrow(train_data), "| Test:", nrow(test_data), "\n")

# ---------- Step 3: Train the Random Forest model (include new feature) ----------
model <- randomForest(
  congested ~ window_size + rtt + throughput + bytes_in_flight + packet_loss + resend_time_after_congestion,
  data = train_data,
  ntree = 100
)
print(model)
cat("Model training complete\n")

# ---------- Step 4: Evaluate the model on test data ----------
preds <- predict(model, newdata = test_data)
confmat <- confusionMatrix(preds, test_data$congested)
print(confmat)

# ---------- Step 5: Predict congestion for new sample (include resend time feature) ----------
sample <- data.frame(
  window_size = 500,
  rtt = 30,
  throughput = 60,
  bytes_in_flight = 4000,
  packet_loss = 0.03,
  resend_time_after_congestion = 120
)
sample_pred <- predict(model, newdata = sample)
cat("Prediction for sample data:", as.character(sample_pred), "\n")

# ---------- Step 6: Export actual vs predicted for test set ----------
results <- data.frame(Actual = test_data$congested, Predicted = preds)
write.csv(results, "tcp_congestion_results_r.csv", row.names = FALSE)
cat("Saved evaluation results as tcp_congestion_results_r.csv\n")

# ---------- Step 7: Boxplots for feature visualization (including new feature) ----------
ggplot(df, aes(x = congested, y = window_size, fill = congested)) +
  geom_boxplot() +
  labs(title = "Window Size by Congested State", x = "Congested", y = "Window Size") +
  theme_minimal()

ggplot(df, aes(x = congested, y = rtt, fill = congested)) +
  geom_boxplot() +
  labs(title = "RTT by Congested State", x = "Congested", y = "RTT (ms)") +
  theme_minimal()

ggplot(df, aes(x = congested, y = throughput, fill = congested)) +
  geom_boxplot() +
  labs(title = "Throughput by Congested State", x = "Congested", y = "Throughput (Mbps)") +
  theme_minimal()

ggplot(df, aes(x = congested, y = bytes_in_flight, fill = congested)) +
  geom_boxplot() +
  labs(title = "Bytes in Flight by Congested State", x = "Congested", y = "Bytes in Flight") +
  theme_minimal()

ggplot(df, aes(x = congested, y = packet_loss, fill = congested)) +
  geom_boxplot() +
  labs(title = "Packet Loss by Congested State", x = "Congested", y = "Packet Loss") +
  theme_minimal()

ggplot(df, aes(x = congested, y = resend_time_after_congestion, fill = congested)) +
  geom_boxplot() +
  labs(title = "Resend Time After Congestion by Congested State", x = "Congested", y = "Resend Time After Congestion (ms)") +
  theme_minimal()

# ---------- Interactive Shiny App (with mean resend time box) ----------
ui <- fluidPage(
  titlePanel("Interactive TCP Data Plotter"),
  sidebarLayout(
    sidebarPanel(
      selectInput("xvar", "X Variable:", choices = names(df), selected = names(df)[1]),
      selectInput("yvar", "Y Variable:", choices = names(df), selected = names(df)[2]),
      selectInput("plotType", "Plot Type:", choices = c("Scatterplot", "Boxplot"), selected = "Scatterplot")
    ),
    mainPanel(
      plotOutput("dataPlot"),
      hr(),
      strong("Mean Time Taken to Resend After Congestion (ms):"),
      verbatimTextOutput("meanResendTime")
    )
  )
)

server <- function(input, output) {
  output$dataPlot <- renderPlot({
    x <- input$xvar
    y <- input$yvar
    type <- input$plotType
    
    if (type == "Scatterplot") {
      ggplot(df, aes_string(x = x, y = y, color = "congested")) +
        geom_point(alpha = 0.6, size = 2) +
        labs(title = paste(y, "vs", x), color = "Congested") +
        theme_minimal()
    } else {
      ggplot(df, aes_string(x = "congested", y = y, fill = "congested")) +
        geom_boxplot() +
        labs(title = paste(y, "by Congested State"), x = "Congested", y = y) +
        theme_minimal()
    }
  })
  output$meanResendTime <- renderPrint({
    mean_val <- mean(df$resend_time_after_congestion[df$congested == 1])
    sprintf("%.2f", mean_val)
  })
}

shinyApp(ui = ui, server = server)
