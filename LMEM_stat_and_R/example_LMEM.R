library(data.table)
library(rstatix) # нет пакета в 3.6.3
library(ggplot2)
library(lme4)
library("ggpubr") # нет пакета в 3.6.3
library(emmeans)
library(lsmeans)
library(gridExtra)
library(lmerTest)

#Для одного сенсора
df <- read.csv('active1_st_5.csv')
### превращаем нужные переменные в факторы ###
df$stimulus <- factor(df$stimulus)
df$subjects <- factor(df$subjects)

#строим модель
Model <- lmer(beta_power_sust ~ RTs + (1 + RTs|subjects) + (1 + RTs|stimulus), data=df)
summary(Model)

s <- step(Model) #автоматически ищем упрощенную модель
s

ggplot(data = df, aes(x = RTs, y = beta_power_sust)) + 
  geom_point() + geom_smooth(method = 'lm')
