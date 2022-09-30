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

path_p <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_AUTISTS/RESPONSE/'
#path_autists <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_AUTISTS/RESPONSE/dataframe_for_LMEM_beta_16_30_trf_early_log_autists_trained/'
#path_autists <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_AUTISTS/RESPONSE/dataframe_for_LMEM_beta_16_30_trf_early_log_autists_not_trained/'
path_autists <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_AUTISTS/RESPONSE/dataframe_for_LMEM_beta_16_30_trf_early_log_autists_ignore_train/'

#path_normals <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_NORMALS/RESPONSE'
#path_normals <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_NORMALS/RESPONSE/dataframe_for_LMEM_beta_16_30_trf_early_log_normals_trained/'
#path_normals <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_NORMALS/RESPONSE/dataframe_for_LMEM_beta_16_30_trf_early_log_normals_not_trained/'
path_normals <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_NORMALS/RESPONSE/dataframe_for_LMEM_beta_16_30_trf_early_log_normals_ignore_train/'

out_path <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_AUTISTS/RESPONSE/'

####  read pval and do fdr co ####
#df <- fread (paste0(path_p, 'p_vals_factor_significance_MEG_group.csv'))
df <- fread (paste0(path_p, 'p_vals_factor_significance_MEG_group_not_trianed.csv'))
df$V1 <- NULL

df[, triple_interaction_fdr:=p.adjust(`group:trial_type:feedback_cur:group`, method = 'fdr')]
df[, trial_interaction_fdr:=p.adjust(`group:trial_type:group`, method = 'fdr')]
df[, fb_interaction_fdr:=p.adjust(`feedback_cur:group`, method = 'fdr')]
df[, group_fdr:=p.adjust(`group`, method = 'fdr')]

sensors_1 <- unique(df[`group`<0.05 & interval==" [-0.9 -0.7]"]$sensor)
sensors_2 <- unique(df[`group`<0.05 & interval==" [-0.7 -0.5]"]$sensor)
sensors_3 <- unique(df[`group`<0.05 & interval==" [-0.5 -0.3]"]$sensor)

#sensors_1 <- unique(df[`trial_type:feedback_cur:group`<0.05 & interval==" [1.5 1.7]"]$sensor)
#sensors_2 <- unique(df[`trial_type:feedback_cur:group`<0.05 & interval==" [1.7 1.9]"]$sensor)
#sensors_1 <- unique(df[`feedback_cur:group`<0.05 & interval==" [1.1 1.3]"]$sensor)
#sensors_2 <- unique(df[`feedback_cur:group`<0.05 & interval==" [1.3 1.5]"]$sensor)

frontal_cluster <- c('8', '9', '10', '11', '16','17','18','19','20','21','23','28','29','30', '31','32', '33','34', '35', '36','42', '43', '44','45')
anterior_cluster <-  c('9', '10','11','12','13','20','22','37')
cluster_slide_3  <-  c('36', '38', '39', '40','41','46', '49','82','83')
#sensors_all  <- cluster_slide_3 
#sensors_all <-sensors_1
#sensors_all <- sensors_u[2:6] #late f

sensors_u <- intersect(sensors_1, sensors_2)
sensors_all <- sensors_u
#sensors_all <- intersect(sensors_u, sensors_3) 

#sensors_all <- anterior_cluster
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

sensor_choosen = 52  #slide 3, frontal
#sensor_choosen = 10 #anterior 
#sensor_choosen = 64 #63  #late fb

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
  cols_short_sample <-  colnames(temp_autists)
  
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
  
  beta_bind <- rbind(beta_normals,beta_autists, fill = TRUE)
}

beta_bind[,`mean beta power [-0.9 -0.5]`:=rowMeans(beta_bind[,.SD,.SDcol=c("beta power [-0.9 -0.7]","beta power [-0.7 -0.5]")])]
#beta_bind[,`mean beta power [1.5 1.9]`:=rowMeans(beta_bind[,.SD,.SDcol=c("beta power [1.5 1.7]","beta power [1.7 1.9]")])]
#beta_bind[,`mean beta power [1.1 1.5]`:=rowMeans(beta_bind[,.SD,.SDcol=c("beta power [1.1 1.3]","beta power [1.3 1.5]")])]

beta_bind[, index := 1:.N, by=c('subject','sensor')] #set indexes of all trials of each subject, same for all sensors
#means <- beta_bind[, mean(`mean beta power [1.5 1.9]`),by=c('subject','index', 'group')]
#means <- beta_bind[, mean(`mean beta power [1.1 1.5]`),by=c('subject','index', 'group')]
means <- beta_bind[, mean(`mean beta power [-0.9 -0.5]`),by=c('subject','index')]

cols <- c("subject","group", "round","trial_type","feedback_cur", "scheme", "index")
means <- merge.data.table(means,beta_bind[sensor==sensor_choosen, ..cols], by = c('subject','index'), all.x = TRUE) # take trial classification from "beta", sensor is random you can take any


setnames(means,'V1','mean_beta')
interval <- 'mean_beta' #name of dependent variable
#if after feedback onset
#m <- lmer(get(interval) ~ group*trial_type*feedback_cur + (1|subject),data = means) # main part, fit model
m <- lmer(get(interval) ~ group*trial_type + (1|subject),data = means) # main part, fit model

m2 <- m # it is because we missed step, so final model=initial model
print(anova(m2))
# plot Tukey over trial types

# prepare table with statistics
interval <- 'mean_beta'
########## Tukey feedback inside feedback ##########

#Tuk1 <- emmeans(m2, pairwise ~ group|trial_type|feedback_cur, adjust = 'tukey',lmer.df = "satterthwaite",lmerTest.limit=8000)
Tuk1 <- emmeans(m2, pairwise ~ group|trial_type, adjust = 'tukey',lmer.df = "satterthwaite",lmerTest.limit=8000)

Tuk1 <- summary(Tuk1)$contrasts
Tuk1 <- data.table(Tuk1)

Tuk1[p.value<0.001, stars:='***']
Tuk1[p.value<0.01 & p.value>0.001 , stars:='**']
Tuk1[p.value<0.05 & p.value>0.01 , stars:='*']
Tuk1[p.value>0.05 & p.value<0.1 , stars:='#']

#prepare data to add stars to graph automatically 

#signif <- Tuk1[!is.na(stars)]
signif <- Tuk1
#signif_pos <- signif[feedback_cur == 'positive']
#signif <- Tuk1[!is.na(stars)]
signif <- signif[feedback_cur == 'negative']

sequence <-data.table(trial_type=c("norisk","prerisk","risk", "postrisk"),number=c(1,2,3,4)) 

means_positive <- means[feedback_cur == 'positive']
means_negative <- means[feedback_cur == 'negative'] 

y_values_rew <- means_positive[group == 'normals',
                      mean(get(interval)),by='trial_type']
setnames(y_values_rew,'V1','y_values_rew')

y_values_lose <- means_positive[group == 'autists',
                       mean(get(interval)),by='trial_type']
setnames(y_values_lose,'V1','y_values_lose')

y_values <- merge(y_values_lose,y_values_rew,by='trial_type')
y_values <- merge(y_values,sequence,by='trial_type')
y_values[,y_max:=max(y_values_lose,y_values_rew),by=trial_type]
y_values <- merge(y_values,signif,by='trial_type')

# plot
#p1 <- ggline(means_positive, 'trial_type', interval,
p1 <- ggline(means_negative, 'trial_type', interval,
             color = 'group',
             palette = c("#FF9900", "#FF33CC"),
             add = c("mean_se"),
             position = position_dodge(0.15),
             order = c("norisk","prerisk","risk", "postrisk"),
             ylab = 'Mean beta NEGATIVE FB', xlab = "Trial type",
             #ylab = 'Mean beta POSITIVE FB', xlab = "Trial type",
             size = 2.0, 
             font.label = list(size = 16, color = "black"))+
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
  
  geom_signif(y_position=c(y_values$y_max +0.05),
              xmin=c(y_values$number-0.075), xmax=c(y_values$number+0.075),
              annotation=c(y_values$stars), 
              tip_length=0.001,textsize = 7,vjust = 0.4)

ggpar(p1,
      #ylim = c(-0.5, 2.0),
      ylim = c(-2.5, 0.0),
      #ylim = c(-3.0, -1.0),#late fb
      #ylim = c(-0.7, 1.0),#late fb slide 3 autists
      #ylim = c(-0.5, 2.0),#late fb slide 3 normals
      font.ytickslab = 16,
)

