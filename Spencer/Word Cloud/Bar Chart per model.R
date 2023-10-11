library(tidyverse)
scores <- tibble(scores = c(.2,.1,.4,.3,.15,.3,.05,.1,.2,.4),
                 emotion = c('Boredom', 'Faithful', 'Anticipation','Contemplation','Trust','Boredom', 'Faithful', 'Anticipation','Contemplation','Trust'),
                 color=c('#992222','green','yellow','blue','lightblue','#992222','green','yellow','blue','lightblue'),
                 model=c('GPT','GPT','GPT','GPT','GPT','Hume','Hume','Hume','Hume','Hume'))
ggplot(scores,aes(x=scores,y=reorder(emotion,scores)))+geom_col(fill=scores$color) +
  theme_minimal() +
  labs(title='Emotion Scores for this Entry',
       x='Score',y=element_blank(),)+
  theme(panel.grid.minor = element_blank()) + facet_wrap(as.factor(scores$model))

