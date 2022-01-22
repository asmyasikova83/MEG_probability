library(reshape2)
library(data.table)
library(ggplot2)
library(lme4)
library("ggpubr")
library(emmeans)
library(lmerTest)
library( dplyr )
library(stringi)
rm(list = ls())

#set type of analysis - for response '-700' or for feedback '1800'
analysis = '1800'

path_p <- 'C:/MEG/mixed_models/Low_Beta_cur/analysis_fix_cross/'
path <- 'C:/MEG/mixed_models/Low_Beta_cur/dataframe_for_LMEM_fix_cross/'
out_path <- 'C:/MEG/mixed_models/Low_Beta_cur/analysis_fix_cross/'


subj_list <- fread('C:\\MEG\\mixed_models\\subj_list.csv')

df <- fread (paste0(path_p, 'p_vals_factor_significance_MEG_fix_cross.csv'))
df$V1 <- NULL

df[, interaction_fdr:=p.adjust(`trial_type:feedback_cur`, method = 'fdr')]
df[, trial_fdr:=p.adjust(`trial_type`, method = 'fdr')]   

fronto_central<-c('MEG0222', 'MEG0232', 'MEG0322', 'MEG0332', 'MEG0342', 'MEG0422', 'MEG0432', 'MEG0442',
                  'MEG0612', 'MEG0632', 'MEG0712','MEG0742', 'MEG1012', 'MEG1422', 'MEG1512', 'MEG1522',
                  'MEG1532', 'MEG1542', 'MEG1622', 'MEG1632', 'MEG1642', 'MEG1712','MEG1722', 'MEG1732',
                  'MEG1742', 'MEG1812', 'MEG1822', 'MEG1832', 'MEG1842', 'MEG1912', 'MEG1922', 'MEG2012',
                  'MEG2112','MEG2142', 'MEG2232', 'MEG2422', 'MEG2512')

# choose sensors signigicant in both intervals
if (analysis == '1800'){
  sensors_all <-fronto_central 
}

print(sensors_all)

sensor_info <- fread('C:/MEG/mixed_models/sensors.csv')
files <- data.table(full_filename=list.files(path, pattern = '*.csv', full.names = T))
files$short_filename <- list.files(path, pattern = '*.csv', full.names = F)

files[, sensor:=stri_extract_first_regex(short_filename,"[0-9]+")]
files$sensor <- as.integer(files$sensor)
files <- merge.data.table(files,sensor_info,by = c('sensor'))
files$effect <- NULL

files <- files[sensor_name %in% sensors_all]

print(files)

# choose sensor

if (analysis == '1800'){
  sensor_choosen = 5 
}

temp <- fread(files[sensor==sensor_choosen]$full_filename) #donor of colnames for empty datatable "beta"
temp$V1 <- NULL
theta <- setNames(data.table(matrix(nrow = 0, ncol = length(colnames(temp))+2)), c(colnames(temp),'sensor','sensor_name'))
for (i in files$sensor){
  temp <- fread(files[sensor==i]$full_filename)
  temp$V1 <- NULL
  temp <- as.data.table(temp)
  temp <- temp[subject %in% subj_list$subj_list]
  
  temp$sensor <- i
  temp$sensor_name <- files[sensor==i]$sensor_name
  
  theta <- rbind(theta,temp, fill = TRUE)
}
if (analysis == '1800'){
  theta[,`mean beta power [-0.55  -0.35]`:=rowMeans(theta[,.SD,.SDcol=c("beta power [-0.55 -0.35]","beta power [-0.35 -0.15]")])] # an ugly hack
}

theta[, index := 1:.N, by=c('subject','sensor')] #set indexes of all trials of each subject, same for all sensors

if (analysis == '1800'){
  # compute means of sensors
  means <- theta[, mean(`mean beta power [-0.55  -0.35]`),by=c('subject','index')]
}

cols <- c("subject","round","trial_type","feedback_cur","feedback_prev","scheme",'index')
means <- merge.data.table(means,theta[sensor==sensor_choosen, ..cols], by = c('subject','index'), all.x = TRUE) # take trial classification from "beta", sensor is random you can take any

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
Tuk1 <- emmeans(m2, pairwise ~ feedback_cur | trial_type, adjust = 'tukey',lmer.df = "satterthwaite",lmerTest.limit=8000)

Tuk1 <- summary(Tuk1)$contrasts
Tuk1 <- data.table(Tuk1)

Tuk1[p.value<0.001, stars:='***']
Tuk1[p.value<0.01 & p.value>0.001 , stars:='**']
Tuk1[p.value<0.05 & p.value>0.01 , stars:='*']
Tuk1[p.value>0.05 & p.value<0.1 , stars:='#']
print(Tuk1)
signif <- Tuk1[!is.na(stars)]
print(signif)
sequence <-data.table(trial_type=c("norisk","prerisk","risk", "postrisk"),number=c(1,2,3,4))


y_values_rew <- means[feedback_cur == 'positive', mean(get(interval)),by='trial_type']
y_values_lose <- means[feedback_cur == 'negative', mean(get(interval)),by='trial_type']
setnames(y_values_lose,'V1','y_values_lose')
setnames(y_values_rew,'V1','y_values_rew')


y_values <- merge(y_values_lose,y_values_rew,by='trial_type')
y_values <- merge(y_values,sequence,by='trial_type')
y_values[,y_max:=max(y_values_lose,y_values_rew),by=trial_type]

if (analysis == '1800'){
  y_values <- merge(y_values,signif,by='trial_type')
}
########## Tukey feedback inside trial_type ##########

Tuk1 <- emmeans(m2, pairwise ~ feedback_cur | trial_type, adjust = 'tukey',lmer.df = "satterthwaite",lmerTest.limit=8000)
Tuk1 <- summary(Tuk1)$contrasts
Tuk1 <- data.table(Tuk1)

Tuk1[p.value<0.001, stars:='***']
Tuk1[p.value<0.01 & p.value>0.001 , stars:='**']
Tuk1[p.value<0.05 & p.value>0.01 , stars:='*']
Tuk1[p.value>0.05 & p.value<0.1 , stars:='#']


#prepare data to add stars to graph automatically 

#signif <- Tuk1[!is.na(stars)]
signif <- Tuk1

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
             ylab = 'Mean beta prior to fix cross (-0.55-0.15 s)', xlab = "Trial type",
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
      ylim = c(-4.3,-2.7), 
      font.ytickslab = 16,
)
ggsave(filename = paste0(out_path,'_Tukey_feedback_cur_fix_cross','.png'), width =  6, height = 5)

# save Tukey feedback cur #
write.csv(Tuk1,paste0(out_path,'Tuk_feedback_cur.csv'))

png(paste0(out_path,'Tuk_feedback_cur.png'), height = 30*nrow(Tuk1), width = 100*ncol(Tuk1))
#grid.table(Tuk1)
dev.off()
