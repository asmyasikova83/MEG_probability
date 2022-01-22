library(reshape2)
library(data.table)
library(ggplot2)
library(lme4)
library("ggpubr")
library(emmeans)
library(lmerTest)
library( dplyr )
library(stringi)
library(stringr)
library("MuMIn")


rm(list = ls())
path_p <- 'C:/MEG/mixed_models/analysis_emg_oculo/'
path <- 'C:/MEG/mixed_models/analysis_emg_oculo/'
out_path <- 'C:/MEG/mixed_models/analysis_emg_oculo/emg/'

subj_list <- fread('C:\\MEG\\mixed_models\\subj_list.csv')


#if before feedback onset
#df <- fread (paste0(path_p, 'p_vals_factor_significance_MEG_decision_making.csv'))
#if after feedback onset
#df <- fread (paste0(path_p, 'p_vals_factor_significance_veog_trial_type.csv'))
df <- fread (paste0(path_p, 'p_vals_factor_significance_heog_interaction.csv'))
df$V1 <- NULL

df[, interaction_fdr:=p.adjust(`trial_type:feedback_cur`, method = 'fdr')]
df[, trial_fdr:=p.adjust(`trial_type`, method = 'fdr')] 
df[, feedback_cur_fdr:=p.adjust(`feedback_cur`, method = 'fdr')] 

beta <- fread('C:/MEG/mixed_models/analysis_emg_oculo/df_LMEM_heog.csv') 
#beta$V1 <- NULL
beta <- as.data.table(beta)
beta <- beta[subject %in% subj_list$subj_list]

#beta[,`mean beta`:=rowMeans(beta[,.SD,.SDcol=c("beta power [1.5 1.7]","beta power [1.7 1.9]")])] # an ugly hack
beta[,`mean beta`:=rowMeans(beta[,.SD,.SDcol=c("beta power [1.5 1.7]","beta power [1.7 1.9]")])]
beta[, index := 1:.N, by=c('subject')] #set indexes of all trials of each subject
means <- beta[, mean(`mean beta`),by=c('subject','index')]

cols <- c("subject","round","trial_type","feedback_cur","feedback_prev","scheme",'index')
means <- merge.data.table(means,beta[, ..cols], by = c('subject','index'), all.x = TRUE) # take trial classification from "beta", sensor is random you can take any

means$subject <- as.factor(means$subject)
means$round <- as.factor(means$round)
means$feedback_cur <-as.factor(means$feedback_cur)
means$feedback_prev <-as.factor(means$feedback_prev)
means$scheme <-as.factor(means$scheme)
means$trial_type <- as.factor(means$trial_type)
setnames(means,'V1','mean_beta')

interval <- 'mean_beta' #name of dependent variable

m <- lmer(get(interval) ~ trial_type*feedback_cur + (1|subject),data = means) # main part, fit model!
m2 <- m # it is because we missed step, so final model=initial model
print(anova(m2))
#ggqqplot(residuals(m))
T########## Tukey feedback inside trial_type ##########

Tuk1 <- emmeans(m2, pairwise ~ feedback_cur | trial_type, adjust = 'tukey',lmer.df = "satterthwaite",lmerTest.limit=8000)
Tuk1 <- summary(Tuk1)$contrasts
Tuk1 <- data.table(Tuk1)

Tuk1[p.value<0.001, stars:='***']
Tuk1[p.value<0.01 & p.value>0.001 , stars:='**']
Tuk1[p.value<0.05 & p.value>0.01 , stars:='*']
Tuk1[p.value>0.05 & p.value<0.1 , stars:='#']


#prepare data to add stars to graph automatically 

signif <- Tuk1[!is.na(stars)]

sequence <-data.table(trial_type=c("norisk","prerisk","risk", "postrisk"),number=c(1,2,3,4)) 

y_values_rew <- means[feedback_cur == 'positive',
                      mean(get(interval)),by='trial_type']
setnames(y_values_rew,'V1','y_values_rew')

y_values_lose <- means[feedback_cur == 'negative',
                       mean(get(interval)),by='trial_type']
setnames(y_values_lose,'V1','y_values_lose')

y_values <- merge(y_values_lose,y_values_rew,by='trial_type')
y_values <- merge(y_values,sequence,by='trial_type')
y_values[,y_max:=max(y_values_lose,y_values_rew),by=trial_type]
y_values <- merge(y_values,signif,by='trial_type')

# plot
p1 <- ggline(means, 'trial_type', interval,
             color = 'feedback_cur',
             add = c("mean_se"),
             position = position_dodge(0.15),
             order = c("norisk","prerisk","risk", "postrisk"),
             ylab = 'Mean beta HEOG 600-800 ms postfb', xlab = "Trial type",
             size = 0.7, 
             font.label = list(size = 16, color = "black"))+
  scale_color_discrete(name = "Current feedback", labels = c("Loss", "Gain"))+
  
  # theme_bw()+
  theme(legend.position=c(0.22,0.85),
        legend.direction = "vertical",
        text = element_text(size=18),
        legend.background = element_rect(size=0.01, linetype="solid",colour = 'black'),
        axis.title.x = element_text(size=18),
        axis.text.x  = element_text(size=16),
        axis.title.y = element_text(size=18))+
  
  geom_signif(y_position=c(y_values$y_max +0.05),
              xmin=c(y_values$number-0.075), xmax=c(y_values$number+0.075),
              annotation=c(y_values$stars), 
              tip_length=0.001,textsize = 7,vjust = 0.4)

ggpar(p1,
      #ylim = c(-1.00,2.0),
      ylim = c(-0.15,1.5),
      #ylim = c(-6.05, 3.0),
      font.ytickslab = 16,
)
# theme_bw()+
# theme(text = element_text(size=13))
ggsave(filename = paste0(out_path,'_Tukey_feedback_cur_1.5_1.9_heog','.png'), width =  6, height = 5)

# save Tukey feedback cur #
write.csv(Tuk1,paste0(out_path,'Tuk_feedback_cur.csv'))

png(paste0(out_path,'Tuk_feedback_cur.png'), height = 30*nrow(Tuk1), width = 100*ncol(Tuk1))
grid.table(Tuk1)
dev.off()


