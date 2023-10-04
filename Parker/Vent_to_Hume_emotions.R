#Vent to Hume conversion
library(dplyr)

V88toH53 <- data.frame("Vent" = c(
  "Adoring", "Adventurous", "Affectionate", "Afraid", "Amazed", "Amused", "Angry", "Annoyed", "Anxious", "Artistic",
  "Ashamed", "Astonished", "Awkward", "Bitter", "Bored", "Calm", "Caring", "Chill", "Confident", "Conflicted",
  "Confused", "Content", "Creative", "Cuddly", "Curious", "Determined", "Disappointed", "Disgusted", "Done (anger)",
  "Dreamy", "Embarrassed", "Empty", "Excited", "Exhausted", "Frustrated", "Furious", "Guilty", "Happy", "Heartbroken",
  "Hopeful", "Hungry", "Hurt", "Hyped", "Imaginative", "Impatient", "Infatuated", "Insecure", "Inspired", "Interested",
  "Irritated", "Jealous", "Lazy", "Lonely", "Lost", "Loving", "Meh", "Miserable", "Motivated", "Musical", "Needy",
  "Nervous", "Nostalgic", "Numb", "Optimistic", "Overwhelmed", "Passionate", "Poetic", "Proud", "Relaxed", "Relieved",
  "Sad", "Safe", "Shocked", "Shy", "Sick", "Sleepy", "Sorry", "Spacey", "Stressed", "Strong", "Supportive", "Surprised",
  "Thankful", "Thoughtful", "Tired", "Uncomfortable", "Upset", "Worried"
),
                       "Hume" = c(
                         "Adoration", "Excitement", "Love", "Fear", "Awe", "Amusement", "Anger", "Annoyance", "Anxiety", "Aesthetic",
                         "Shame", "Surprise (positive)", "Awkwardness", "Disappointment", "Boredom", "Calmness", "Love", "Calmness",
                         "Pride", "Confusion", "Confusion", "Contentment", "Creativity", "Affection", "Interest", "Determination", "Disappointment",
                         "Disgust", "Anger", "Romantic", "Embarrassment", "Sadness", "Excitement", "Tiredness", "Annoyance", "Anger", "Shame",
                         "Joy", "Sadness", "Optimism", "Craving", "Pain", "Excitement", "Creativity", "Annoyance", "Romantic", "Shame", "Awe",
                         "Interest", "Annoyance", "Envy", "Tiredness", "Sadness", "Confusion", "Love", "Disappointment", "Sadness", "Determination",
                         "Aesthetic", "Dependence", "Anxiety", "Nostalgia", "Sadness", "Hope", "Anxiety", "Love", "Aesthetic", "Pride", "Calmness",
                         "Relief", "Sadness", "Security", "Surprise (negative)", "Social anxiety", "Pain", "Tiredness", "Guilt", "Confusion",
                         "Anxiety", "Power", "Love", "Surprise (positive)", "Gratitude", "Consideration", "Tiredness", "Discomfort", "Sadness",
                         "Anxiety"
                       )
)

your_data <- read.csv("Vent_to_Hume/test1.csv") #change depending on directory
your_data <- data.frame("Emotion" = your_data[,2]) #select column of emotions, 1 is first column
lookup_df <- V88toH53
result_df <- your_data %>% left_join(lookup_df, by = c("Emotion" = "Vent")) #Emotion will be the name of the selected column
write.csv(result_df, "Vent_to_Hume/test1_output.csv")
