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

#path_p <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_AUTISTS/ALPHA/RESPONSE/'
#path_autists <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_AUTISTS/RESPONSE/ALPHA/dataframe_for_LMEM_alpha_10_15_trf_early_log_trained_400ms/'

#path_normals <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_NORMALS/RESPONSE'
#path_normals <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_NORMALS/RESPONSE/ALPHA/dataframe_for_LMEM_alpha_10_15_trf_early_log_trained_400ms/'

path_p <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_AUTISTS/RESPONSE/'
path_autists <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_AUTISTS/RESPONSE/dataframe_for_LMEM_beta_16_30_trf_early_log_autists_trained_400ms/'

path_normals <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_NORMALS/RESPONSE/dataframe_for_LMEM_beta_16_30_trf_early_log_normals_trained_400ms/'


out_path <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_AUTISTS/RESPONSE/'

####  read pval and do fdr co ####
#df <- fread (paste0(path_p, 'p_vals_factor_significance_MEG_group_bk.csv'))
#deprecated
df <- fread (paste0(path_p, 'p_vals_factor_significance_MEG_group400msALPHA.csv'))
df$V1 <- NULL


late_fb_triple_posterior <- c('61','62', '63','64', '70', '71', '72', '73', '77', '78', '79')
late_fb_triple_anterior <- c('5', '9', '11')

late_fb_double_trial_type_group <- c('63', '64','76', '86', '87', '88','89','92','93')
decision_alpha <- c('52', '56', '60', '61', '62', '63', '64', '65', '69', '70', '71', 
                    '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '84',
                    '86', '87', '88', '92', '94', '95', '96', '97', '99', '100')

sensors_all <- late_fb_triple_posterior
print(sensors_all)

#### prepare table with info ####

sensor_info <- fread('C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/sensors.csv')

files_normals <- data.table(full_filename=list.files(path_normals, pattern = '*.csv', full.names = T))
files_normals$short_filename <- list.files(path_normals, pattern = '*.csv', full.names = F)

files_normals[, sensor:=stri_extract_first_regex(short_filename,"[0-9]+")]
files_normals$sensor <- as.integer(files_normals$sensor)
files_normals  <- merge.data.table(files_normals,sensor_info,by = c('sensor'))
files_normals$effect <- NULL
files_normals <- files_normals[sensor%in% sensors_all]

files_autists <- data.table(full_filename=list.files(path_autists, pattern = '*.csv', full.names = T))
files_autists$short_filename <- list.files(path_autists, pattern = '*.csv', full.names = F)

files_autists[, sensor:=stri_extract_first_regex(short_filename,"[0-9]+")]
files_autists$sensor <- as.integer(files_autists$sensor)
files_autists  <- merge.data.table(files_autists,sensor_info,by = c('sensor'))
files_autists$effect <- NULL
files_autists <- files_autists[sensor %in% sensors_all]

sensor_choosen = 62


temp_autists<- fread(files_autists[sensor==sensor_choosen]$full_filename) #donor of colnames for empty datatable "beta"
temp_autists$V1 <- NULL
temp_autists$beta_power <- NULL

temp_normals <- fread(files_normals[sensor==sensor_choosen]$full_filename) #donor of colnames for empty datatable "beta"
temp_normals$V1 <- NULL

beta_autists <- setNames(data.table(matrix(nrow = 0, ncol = length(colnames(temp_autists))+2)), c(colnames(temp_autists),'sensor','sensor_name'))
beta_normals <- setNames(data.table(matrix(nrow = 0, ncol = length(colnames(temp_autists))+2)), c(colnames(temp_autists),'sensor','sensor_name'))

subj_list_autists <- fread('C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/subj_list_autists_short.csv')
subj_list_normals <- fread('C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/subj_list_normals_short.csv')

for (i in files_autists$sensor){
  
  temp_autists <- fread(files_autists[sensor==i]$full_filename)
  temp_autists$V1 <- NULL
  temp_autists$beta_power <- NULL
  temp_autists <- as.data.table(temp_autists)
  temp_autists <- temp_autists[subject %in% subj_list_autists$subj_list]
  
  temp_autists$sensor <- as.factor(i)
  temp_autists$sensor_name <- files_autists[sensor==i]$sensor_name
  temp_autists$group <- c('autists')
  temp_autists$group <- as.factor(temp_autists$group)
  
  beta_autists <- rbind(beta_autists,temp_autists, fill = TRUE)
  
}  

cols_short_sample <-  colnames(temp_autists)

for (i in files_normals$sensor){
  
  temp_normals <- fread(files_normals[sensor==i]$full_filename)
  temp_normals$V1 <- NULL
  temp_normals <- as.data.table(temp_normals)
  temp_normals <- temp_normals[subject %in% subj_list_normals$subj_list]
  
  temp_normals$sensor <- as.factor(i)
  temp_normals$sensor_name <- files_normals[sensor==i]$sensor_name
  temp_normals$group <- c('normals')
  temp_normals$group <- as.factor(temp_normals$group)
  
  temp_normals_sh <- temp_normals[, ..cols_short_sample]
  
  
  beta_normals <- rbind(beta_normals,temp_normals_sh, fill = TRUE)
}
beta_normals <- beta_normals[trial_type != 'prerisk']
beta_normals <- beta_normals[trial_type != 'postrisk']
#beta_normals <- beta_normals[feedback_cur == 'positive']
#beta_normals <- beta_normals[feedback_cur == 'negative']

beta_normals[,`mean beta power [1.1 1.5]`:=rowMeans(beta_normals[,.SD,.SDcol=c("beta power [1.1 1.5]","beta power [1.1 1.5]")])]
#beta_normals[,`mean beta power [-0.9 -0.5]`:=rowMeans(beta_normals[,.SD,.SDcol=c("beta power [-0.9 -0.5]","beta power [-0.9 -0.5]")])]
#beta_normals[,`mean beta power [1.5 1.9]`:=rowMeans(beta_normals[,.SD,.SDcol=c("beta power [1.5 1.9]","beta power [1.5 1.9]")])]
beta_normals[, index := 1:.N, by=c('subject','sensor')] #set indexes of all trials of each subject, same for all sensors

means_normals <- beta_normals[, mean(`mean beta power [1.1 1.5]`),by=c('subject','index')]
#means_normals <- beta_normals[, mean(`mean beta power [-0.9 -0.5]`),by=c('subject','index')]
#means_normals <- beta_normals[, mean(`mean beta power [1.5 1.9]`),by=c('subject','index')]

beta_autists <- beta_autists[trial_type != 'prerisk']
beta_autists <- beta_autists[trial_type != 'postrisk']
#beta_autists <- beta_autists[feedback_cur == 'positive']
#beta_autists <- beta_autists[feedback_cur == 'negative']

beta_autists[,`mean beta power [1.1 1.5]`:=rowMeans(beta_autists[,.SD,.SDcol=c("beta power [1.1 1.5]","beta power [1.1 1.5]")])]
#beta_autists[,`mean beta power [-0.9 -0.5]`:=rowMeans(beta_autists[,.SD,.SDcol=c("beta power [-0.9 -0.5]","beta power [-0.9 -0.5]")])]
#beta_autists[,`mean beta power [1.5 1.9]`:=rowMeans(beta_autists[,.SD,.SDcol=c("beta power [1.5 1.9]","beta power [1.5 1.9]")])]
beta_autists[, index := 1:.N, by=c('subject','sensor')] #set indexes of all trials of each subject, same for all sensors

means_autists <- beta_autists[, mean(`mean beta power [1.1 1.5]`),by=c('subject','index')]
#means_autists <- beta_autists[, mean(`mean beta power [-0.9 -0.5]`),by=c('subject','index')]
#means_autists <- beta_autists[, mean(`mean beta power [1.5 1.9]`),by=c('subject','index')]

cols <- c("subject","round","trial_type","feedback_cur", "index")
means_normals <- merge.data.table(means_normals,beta_normals[sensor==sensor_choosen, ..cols], by = c('subject','index'), all.x = TRUE) # take trial classification from "beta", sensor is random you can take any
means_autists <- merge.data.table(means_autists,beta_autists[sensor==sensor_choosen, ..cols], by = c('subject','index'), all.x = TRUE) # take trial classification from "beta", sensor is random you can take any
means_normals$group <- 'normals'
means_autists$group <- 'autists'

means <- rbind(means_autists, means_normals)

means$subject <- as.factor(means$subject)
means$round <- as.factor(means$round)
means$feedback_cur <-as.factor(means$feedback_cur)
#means$feedback_prev <-as.factor(means$feedback_prev)
#means$scheme <-as.factor(means$scheme)
means$trial_type <- as.factor(means$trial_type)
means$group <- as.factor(means$group)
setnames(means,'V1','mean_beta')


interval <- 'mean_beta' #name of dependent variable
#if after feedback onset
m <- lmer(get(interval) ~ trial_type*feedback_cur*group + (1|subject),data = means) # main part, fit model
#m <- lmer(get(interval) ~ trial_type*group + (1|subject),data = means) # main part, fit model
m2 <- m # it is because we missed step, so final model=initial model
print(anova(m2))
# plot Tukey over trial types

T########## Tukey feedback inside trial_type ##########

#Tuk <- emmeans(m2, pairwise ~ group | trial_type, adjust = 'tukey',lmer.df = "satterthwaite",lmerTest.limit=8000)
#Tuk<- summary(Tuk)$contrasts

result <- emmeans(m2, pairwise ~ group | trial_type, adjust = 'tukey',lmer.df = "satterthwaite",lmerTest.limit=8000) # Tukey inside "trial type" factor
#print(summary(result))

# compute y_position to draw p-value on graph
# get estimated marginal means
em_means <- summary(result$emmeans)
em_means <- data.table(em_means)
em_means <- em_means[, c('trial_type','group', 'emmean')]
setnames(em_means,'emmean','mean_beta')
em_means$mean <- 'emmean'

#the same order of trial_types as in means
em_means_ed<- data.frame(em_means)
em_means_ed[1,] <- em_means[1,]
em_means_ed[2,] <- em_means[5,]
em_means_ed[3,] <- em_means[7,]
em_means_ed[4,] <- em_means[3,]

em_means_ed[5,] <- em_means[2,]
em_means_ed[6,] <- em_means[6,]
em_means_ed[7,] <- em_means[8,]
em_means_ed[8,] <- em_means[4,]

Tuk <- data.table(summary(emmeans(m2, pairwise ~ group | trial_type, adjust = 'tukey',lmer.df = "satterthwaite",lmerTest.limit=8000))$contrasts) #if trial number >8000 change limit
Tuk <- data.table(Tuk)
print(Tuk)
#Tuk <- Tuk[, group1:=gsub(' -.*', '', contrast)][, group2:=gsub('.*- ', '', contrast)]
Tuk <- Tuk[, contrast := gsub('(', '', gsub(')', '', contrast, fixed = TRUE), fixed = TRUE)]
#Tuk <- Tuk[, group1 := gsub('(', '', gsub(')', '', group1, fixed = TRUE), fixed = TRUE)]
#Tuk <- Tuk[, group2 := gsub('(', '', gsub(')', '', group2, fixed = TRUE), fixed = TRUE)]
#Tuk <- Tuk[p.value<0.1, p_significant:=format(p.value, digits = 3)]

Tuk[p.value<0.001, stars:='***']
Tuk[p.value<0.01 & p.value>0.001 , stars:='**']
Tuk[p.value<0.05 & p.value>0.01 , stars:='*']
Tuk[p.value>0.05 & p.value<0.1 , stars:='#']

# compute y_position to draw p-value on graph
n <- Tuk[!is.na(p_significant), .N]

#prepare data to add stars to graph automatically 

#signif <- Tuk1[!is.na(stars)]
signif <- Tuk

#thr <- max(means[, mean(get(interval)) + sterr(get(interval)), by=trial_type]$V1) #
thr <- max(means[, abs(mean(get(interval))), by=trial_type]$V1)
print(thr)

#sequence <-data.table(trial_type=c("norisk","prerisk","risk", "postrisk"),number=c(1,2,3,4)) 
sequence <-data.table(trial_type=c("norisk","risk"),number=c(1,2)) 

y_values_rew <- means[group == 'normals',
                      mean(get(interval)),by='trial_type']
setnames(y_values_rew,'V1','y_values_rew')

y_values_lose <- means[group == 'autists',
                       mean(get(interval)),by='trial_type']
setnames(y_values_lose,'V1','y_values_lose')

y_values <- merge(y_values_lose,y_values_rew,by='trial_type')
y_values <- merge(y_values,sequence,by='trial_type')
y_values[,y_max:=max(y_values_lose,y_values_rew),by=trial_type]
y_values <- merge(y_values,signif,by='trial_type')


# plot Tukey

p1 <- ggline(em_means, x = 'trial_type', y = 'mean_beta',
#p1 <- ggline(means, x = 'trial_type', y = 'mean_beta',
             color = 'group',
             #add = c("mean_se"),
             palette = c("#FF9900", "#FF33CC"),
             position = position_dodge(0.15),
             #order = c("norisk","prerisk","risk", "postrisk"),
             #ylab = 'Mean beta -0.9 - 0.5 s ', xlab = "Trial type",
             #ylab = 'Mean beta 1.5 1.9 s Negative FB ', xlab = "Trial type",
             #ylab = 'Mean beta 1.5 1.9 s Positive FB ', xlab = "Trial type",
             ylab = 'Mean beta 1.1-1.5 s after response ', xlab = "Trial type",
             size = 2.0, 
             font.label = list(size = 16, color = "black"))+
  geom_hline(yintercept=-0.0, linetype='dashed', col = 'black', size = 1)+
  #  scale_color_discrete(name = "Cur fb", labels = c("autists", "normals"))+
  #scale_color_discrete(name = "Cur fb AUTISTS", labels = c("Loss", "Gain"))+
  
  # theme_bw()+
  theme(legend.position=c(0.15,0.85),
        legend.direction = "vertical",
        text = element_text(size=18),
        legend.background = element_rect(size=0.01, linetype="solid",colour = 'black'),
        axis.title.x = element_text(size=18),
        axis.text.x  = element_text(size=16),
        axis.title.y = element_text(size=18))+
  
  geom_signif(y_position=c(y_values$y_max +0.5),
              xmin=c(y_values$number-0.035), xmax=c(y_values$number+0.35),
              annotation=c(y_values$stars), 
              tip_length=0.001,textsize = 7,vjust = 0.4)

ggpar(p1,
      ylim = c(-5.0, -1.0), #late fb
      #ylim = c(-7.0, 1.0), #decis
      #ylim = c(-2.0, 0.5), #early fb
      #ylim = c(0.0, 1.5), slide 3
      #ylim = c(-2.0, 3.0),
      font.ytickslab = 16,
)

#ggplot(data=em_means_ed, aes(x=trial_type, y=mean_beta, group=group ,  color=group, size = 0.2)) +
#ggplot(data=em_means_ed, aes(x=trial_type, y=mean_beta, group=group ,  color=group, size = 0.2)) +
#  ylim(-5.0, -2.25)+
#  geom_line() +
#  geom_point()+
  #  theme_bw()
#  theme(
#    text = element_text(size=18),
#    legend.background = element_rect(size=0.01, linetype="solid",colour = 'black'),
#    axis.title.x = element_text(size=18),
#    axis.text.x  = element_text(size=16),
#    axis.title.y = element_text(size=18))
#ggsave(filename = paste0(out_path,'_aver_means','.png'), width =  8, height = 7)
