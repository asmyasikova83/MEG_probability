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

path_p <- 'C:/MEG/mixed_models/Beta_cur/analysis_bline_nologdiv/'
path <- 'C:/MEG/mixed_models/Beta_cur/dataframe_for_LMEM_bline_nologdiv/'
out_path <- 'C:/MEG/mixed_models/Beta_cur/analysis_bline_nologdiv/'


subj_list <- fread('C:\\MEG\\mixed_models\\subj_list.csv')

#df <- fread (paste0(path_p, 'p_vals_factor_significance_MEG_decision_making.csv'))
df <- fread (paste0(path_p, 'p_vals_factor_significance_MEG.csv'))
df$V1 <- NULL

df[, interaction_fdr:=p.adjust(`trial_type:feedback_cur`, method = 'fdr')]

df[, interaction_fdr:=p.adjust(`trial_type:feedback_cur`, method = 'fdr')]
df[, trial_fdr:=p.adjust(`trial_type`, method = 'fdr')]   

#sensors_2 <- unique(df[interaction_fdr<0.007 & interval==" [1.5 1.7]"]$sensor_name)
#sensors_3 <- unique(df[interaction_fdr<0.005 & interval==" [1.7 1.9]"]$sensor_name)

#sensors_2 <- unique(df[interaction_fdr<0.05 & interval==" [1.5 1.7]"]$sensor_name)
#sensors_3 <- unique(df[interaction_fdr<0.05 & interval==" [1.7 1.9]"]$sensor_name)

#sensors_2 <- unique(df[trial_fdr<0.05 & interval==" [1.1 1.3]"]$sensor_name)
#sensors_3 <- unique(df[trial_fdr<0.05 & interval==" [1.3 1.5]"]$sensor_name)

sensors_2 <- unique(df[trial_fdr<0.05 & interval==" [0.1 0.3]"]$sensor_name)
sensors_3 <- unique(df[trial_fdr<0.05 & interval==" [0.3 0.5]"]$sensor_name)

#sensors_all <- intersect(sensors_2, sensors_3)
#print(sensors_all)

anterior_cluster <-  c('MEG0222', 'MEG0232', 'MEG0322', 'MEG0332', 'MEG0342', 'MEG0412', 'MEG0422', 'MEG0442', 'MEG0612', 'MEG0632', 'MEG0722', 'MEG0732', 'MEG1042', 'MEG1622')

whole <- c('MEG0222', 'MEG0232', 'MEG0322', 'MEG0332', 'MEG0342','MEG0412', 'MEG0422', 'MEG0442', 'MEG0612',
           'MEG0632', 'MEG0722', 'MEG0732','MEG1042','MEG1622','MEG1632','MEG1642','MEG1722', 'MEG1732', 'MEG1812', 'MEG1842',
           'MEG1912', 'MEG1922','MEG2012','MEG2022','MEG2032','MEG2042','MEG2112', 'MEG2232','MEG2312','MEG2432', 'MEG2442')

occipital_cluster <-  c('MEG1632', 'MEG1642', 'MEG1722', 'MEG1732', 'MEG1842', 'MEG1912', 'MEG1922', 
                        'MEG2012', 'MEG2022', 'MEG2032', 'MEG2042', 'MEG2112', 'MEG2232', 'MEG2312', 'MEG2432', 
                        'MEG2442')
sensors_all <- anterior_cluster 
#print(sensors_all)

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

# if whole
#sensor_choosen = 5 
#if occipital and early fb [1200  1400]
sensor_choosen = 59
#anterior 59
#occip 93
#whole  60
#sensor_choosen = 5  

temp <- fread(files[sensor==sensor_choosen]$full_filename) #donor of colnames for empty datatable "beta"
temp$V1 <- NULL
beta <- setNames(data.table(matrix(nrow = 0, ncol = length(colnames(temp))+2)), c(colnames(temp),'sensor','sensor_name'))
for (i in files$sensor){
  temp <- fread(files[sensor==i]$full_filename)
  temp$V1 <- NULL
  temp <- as.data.table(temp)
  temp <- temp[subject %in% subj_list$subj_list]
  
  temp$sensor <- i
  temp$sensor_name <- files[sensor==i]$sensor_name
  
  beta <- rbind(beta,temp, fill = TRUE)
}


beta[,`mean beta power [1.5  1.9]`:=rowMeans(beta[,.SD,.SDcol=c("beta power [1.5 1.7]","beta power [1.7 1.9]")])] # an ugly hack
#beta[,`mean beta power [1.2  1.4]`:=rowMeans(beta[,.SD,.SDcol=c("beta power [1.1 1.3]","beta power [1.3 1.5]")])] # an ugly hack


beta[, index := 1:.N, by=c('subject','sensor')] #set indexes of all trials of each subject, same for all sensors

# compute means of sensors

means <- beta[, mean(`mean beta power [1.5  1.9]`),by=c('subject','index')]
#means <- beta[, mean(`mean beta power [1.2  1.4]`),by=c('subject','index')]

cols <- c("subject","round","trial_type","feedback_cur","feedback_prev","scheme",'index')
means <- merge.data.table(means,beta[sensor==sensor_choosen, ..cols], by = c('subject','index'), all.x = TRUE) # take trial classification from "beta", sensor is random you can take any

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
             ylab = 'Mean beta 600-800 ms postfeedback', xlab = "Trial type",
             size = 2.0, 
             font.label = list(size = 16, color = "black"))+
  #scale_color_discrete(name = "Current feedback", labels = c("Loss", "Gain"))+
  
  # theme_bw()+
  theme(legend.position=c(0.22,0.85),
        legend.direction = "vertical",
        text = element_text(size=18),
        legend.background = element_rect(size=0.01, linetype="solid",colour = 'black'),
        axis.title.x = element_text(size=26),
        axis.line = element_line(size = 2),
        axis.ticks = element_line(size = 4) , 
        axis.ticks.length = unit(.5, "cm"),
        axis.text.x  = element_text(size=24),
        axis.title.y = element_text(size=26))+
  
  geom_signif(y_position=c(y_values$y_max +0.05),
              xmin=c(y_values$number-0.075), xmax=c(y_values$number+0.075),
              annotation=c(y_values$stars), 
              tip_length=0.001,textsize = 12,vjust = 0.4)

ggpar(p1,
      #ylim = c(-2.0,0.0), #whole
      #ylim = c(-3.1, -1), #occip
      ylim = c(-1.15, 1.956), #anterior
      font.ytickslab = 40,
)
ggsave(filename = paste0(out_path,'_Tukey_feedback_anter_thick_font','.png'), width =  8, height = 7)

# save Tukey feedback cur #
write.csv(Tuk1,paste0(out_path,'Tuk_feedback_cur.csv'))

png(paste0(out_path,'Tuk_feedback_cur.png'), height = 30*nrow(Tuk1), width = 100*ncol(Tuk1))
#grid.table(Tuk1)
dev.off()
