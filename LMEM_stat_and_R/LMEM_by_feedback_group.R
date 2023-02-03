
library(reshape2)
library(data.table)
library(ggplot2)
library(lme4)
library(emmeans)
library(lmerTest)
library(stringi)
library(stringr)
library(dplyr)

path_autists <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_AUTISTS/RESPONSE'
path_autists <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_AUTISTS/RESPONSE/dataframe_for_LMEM_beta_16_30_trf_early_log_autists_trained_600ms/'
#path_autists <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_AUTISTS/RESPONSE/dataframe_for_LMEM_beta_16_30_trf_early_log_autists_not_trained/'

path_normals <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_NORMALS/RESPONSE'
path_normals <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_NORMALS/RESPONSE/dataframe_for_LMEM_beta_16_30_trf_early_log_normals_trained_600ms/'
#path_normals <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_NORMALS/RESPONSE/dataframe_for_LMEM_beta_16_30_trf_early_log_normals_not_trained/'

out_path <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_AUTISTS/RESPONSE/'

#### prepare table with info ####

sensor_info <- fread('C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/sensors.csv')

files_normals <- data.table(full_filename=list.files(path_normals, pattern = '*.csv', full.names = T))
files_normals$short_filename <- list.files(path_normals, pattern = '*.csv', full.names = F)

files_normals[, sensor:=stri_extract_first_regex(short_filename,"[0-9]+")]
files_normals$sensor <- as.integer(files_normals$sensor)
files_normals  <- merge.data.table(files_normals,sensor_info,by = c('sensor'))
files_normals$effect <- NULL


files_autists <- data.table(full_filename=list.files(path_autists, pattern = '*.csv', full.names = T))
files_autists$short_filename <- list.files(path_autists, pattern = '*.csv', full.names = F)

files_autists[, sensor:=stri_extract_first_regex(short_filename,"[0-9]+")]
files_autists$sensor <- as.integer(files_autists$sensor)
files_autists  <- merge.data.table(files_autists,sensor_info,by = c('sensor'))
files_autists$effect <- NULL

## load subj_list ##

subj_list_autists <- fread('C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/subj_list_autists_short.csv')
subj_list_normals <- fread('C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/subj_list_normals_short.csv')

#### make large table with p_values ####


temp_normals <- fread(files_normals[sensor==0]$full_filename) #donor of colnames for empty datatable "beta"
temp_normals$V1 <- NULL
temp_normals$sensor_name <-files_normals[sensor==0]$sensor_name

temp_autists <- fread(files_autists[sensor==0]$full_filename) #donor of colnames for empty datatable "beta"
temp_autists$V1 <- NULL
temp_autists$beta_power <- NULL
temp_autists$sensor_name <-files_autists[sensor==0]$sensor_name

cols <- colnames(temp_autists)[grep('[0-9]',colnames(temp_autists))]


######################################fb##############
p_vals <- data.table()
for (i in files_autists$sensor){
#for (i in 1:2){
  #download group autists
  print(i)
  temp_autists <- fread(files_autists[sensor==i]$full_filename)
  temp_autists$V1 <- NULL
  temp_autists$beta_power <- NULL
  temp_autists <- temp_autists[subject %in% subj_list_autists$subj_list]
  
  temp_autists$subject <- as.factor(temp_autists$subject)
  temp_autists$round <- as.factor(temp_autists$round)
  temp_autists$feedback_cur <-as.factor(temp_autists$feedback_cur)
  temp_autists$trial_type <- as.factor(temp_autists$trial_type)
  temp_autists$sensor <- as.factor(i)
  #temp_autists$sensor_name <- as.factor(temp_autists$sensor_name)
  temp_autists$group <- c('autists')
  temp_autists$group <- as.factor(temp_autists$group)
  cols_short_sample <-  colnames(temp_autists)
  
  
  #download group normals
  temp_normals <- fread(files_normals[sensor==i]$full_filename)
  temp_normals$V1 <- NULL
  
  temp_normals <- temp_normals[subject %in% subj_list_normals$subj_list]
  
  temp_normals$subject <- as.factor(temp_normals$subject)
  temp_normals$round <- as.factor(temp_normals$round)
  temp_normals$feedback_cur <-as.factor(temp_normals$feedback_cur)
  #temp$feedback_prev <-as.factor(temp$feedback_prev)
  #temp_normals$scheme <-as.factor(temp_normals$scheme)
  temp_normals$trial_type <- as.factor(temp_normals$trial_type)
  temp_normals$sensor <- as.factor(i)
  #temp_normals$sensor_name <- as.factor(temp_normals$sensor_name)
  temp_normals$group <- c('normals')
  temp_normals$group <- as.factor(temp_normals$group)
  
  temp_normals_sh <- temp_normals[, ..cols_short_sample]
  
  temp_bind <- rbind(temp_normals_sh,temp_autists)
  
  temp_bind <- temp_bind[trial_type != 'prerisk']
  temp_bind <- temp_bind[trial_type != 'postrisk']
  

  for (j in cols){
     m <- lmer(get(j) ~ trial_type*feedback_cur*group + (1|subject), data = temp_bind)
     #Tuk <- data.table(summary(emmeans(m2, pairwise ~ trial_type, adjust = 'tukey',lmer.df = "satterthwaite",lmerTest.limit=8000))$contrasts) #if trial number >8000 change limit
     Tuk <- data.table(summary(emmeans(m, pairwise ~  feedback_cur | trial_type |  group, adjust = 'tukey',lmer.df = "satterthwaite",lmerTest.limit=8000))$contrasts)
     Tuk <- Tuk[, group1:=gsub(' -.*', '', contrast)][, group2:=gsub('.*- ', '', contrast)]
     Tuk[,contrast:=gsub(' - ','_',contrast)]
     print(Tuk)
     Tuk[,p.value:=format(p.value, digits = 3)]
     Tuk[,contrast:=paste0(group, '_', trial_type,'-',contrast)]
     columns <- c('contrast', 'p.value')
     Tuk <- Tuk[,..columns]
     Tuk$interval <- j
     Tuk$interval <- gsub('beta power','',Tuk$interval)
     Tuk <- dcast(Tuk,formula = interval~contrast,value.var = 'p.value')
     Tuk$sensor <- i
     Tuk$sensor_name <- files_autists[sensor==i]$sensor_name
     p_vals <- rbind(p_vals,Tuk)
     }
}
write.csv(p_vals,paste0(out_path, "p_vals_by_feedback_MEG_group_600ms_fin.csv"))