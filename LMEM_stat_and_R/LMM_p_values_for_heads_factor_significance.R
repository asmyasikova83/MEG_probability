# save tables with p-values

library(reshape2)
library(data.table)
library(ggplot2)
library(lme4)
# library("ggpubr")
library(emmeans)
library(lmerTest)
library(stringi)
library(stringr)
# install.packages("xlsx")
# library(xlsx)

#path_p <- 'C:/MEG/mixed_models/Beta_cur/analysis_bline_nologdiv/'
#path <- 'C:/MEG/mixed_models/Beta_cur/dataframe_for_LMEM_bline_nologdiv/'
#out_path <- 'C:/MEG/mixed_models/Beta_cur/analysis_bline_nologdiv/'

#path_p <- 'C:/MEG/mixed_models/Theta_cur/analysis_for _article/'
#path <- 'C:/MEG/mixed_models/Theta_cur/dataframe_for_LMEM_check/'
#out_path <- 'C:/MEG/mixed_models/Theta_cur/analysis_for _article/'

#path_p <- 'C:/MEG/mixed_models/Beta_cur_arly_log/analysis/'
#path <- 'C:/MEG/mixed_models/Beta_cur_arly_log/dataframe_for_LMEM/'
#out_path <- 'C:/MEG/mixed_models/Beta_cur_arly_log/pre-trial/'

#### prepare table with info ####
sensor_info <- fread('C:/MEG/mixed_models/sensors.csv')
files <- data.table(full_filename=list.files(path, pattern = '*.csv', full.names = T))
files$short_filename <- list.files(path, pattern = '*.csv', full.names = F)
# files$short_filename <- gsub('planar1','',files$short_filename)

files[, sensor:=stri_extract_first_regex(short_filename,"[0-9]+")]
files[, interval:=str_extract(short_filename,'[0-9]+_[0-9]+.csv')]
files[,interval:=gsub('.csv','',interval)]
files$sensor <- as.integer(files$sensor)
files <- merge.data.table(files,sensor_info,by = c('sensor'))
files$effect <- NULL

## load subj_list ##
#subj_list <- fread('C:/MEG/mixed_models/subj_list.csv')
subj_list <- fread('C:\\MEG\\mixed_models\\subj_list.csv')

#### make large table with p_values ####

temp <- fread(files[sensor==0]$full_filename)
temp$V1 <- NULL
cols <- colnames(temp)[grep('[0-9]',colnames(temp))]

######## for trial_type #############
p_vals <- data.table()
for (i in files$sensor){
  temp <- fread(files[sensor==i]$full_filename)
  temp$V1 <- NULL
  
  temp <- temp[subject %in% subj_list$subj_list]
  
  temp$subject <- as.factor(temp$subject)
  temp$round <- as.factor(temp$round)
  temp$feedback_cur <-as.factor(temp$feedback_cur)
  temp$feedback_prev <-as.factor(temp$feedback_prev)
  temp$scheme <-as.factor(temp$scheme)
  temp$trial_type <- as.factor(temp$trial_type)
  
  for (j in cols){
    m <- lmer(get(j) ~ trial_type + (1|subject), data = temp)
    an <- anova(m)
    an <- data.table(an,keep.rownames = TRUE)
    an_cols <- c('rn','Pr(>F)') 
    an <- an[, ..an_cols]
    an$`Pr(>F)` <- format(an$`Pr(>F)`, digits = 3)
    an$interval <- j
    an$interval <- gsub('beta power','',an$interval)
    an <- dcast(an,formula = interval~rn,value.var = 'Pr(>F)')
    an$sensor <- i
    an$sensor_name <- files[sensor==i]$sensor_name
    p_vals <- rbind(p_vals,an)
  }
}
  
write.csv(p_vals,paste0(out_path, "p_vals_factor_significance_MEG_pre_trial.csv"))

###### feedback_cur #######
p_vals <- data.table()
for (i in files$sensor){
  temp <- fread(files[sensor==i]$full_filename)
  temp$V1 <- NULL
  
  temp <- temp[subject %in% subj_list$subj_list]
  
  temp$subject <- as.factor(temp$subject)
  temp$round <- as.factor(temp$round)
  temp$feedback_cur <-as.factor(temp$feedback_cur)
  temp$feedback_prev <-as.factor(temp$feedback_prev)
  temp$scheme <-as.factor(temp$scheme)
  temp$trial_type <- as.factor(temp$trial_type)
  
  for (j in cols){
    m <- lmer(get(j) ~ trial_type*feedback_cur + (1|subject), data = temp)
    Tuk <- data.table(summary(emmeans(m, pairwise ~ feedback_cur | trial_type, adjust = 'tukey',lmer.df = "satterthwaite",lmerTest.limit=8000))$contrasts)
    Tuk[,contrast:=gsub(' - ','_',contrast)]
    Tuk[,p.value:=format(p.value, digits = 3)]
    Tuk[,contrast:=paste0(trial_type,'-',contrast)]
    columns <- c('contrast','p.value')
    Tuk <- Tuk[,..columns]
    Tuk$interval <- j
    Tuk$interval <- gsub('beta power','',Tuk$interval)
    Tuk <- dcast(Tuk,formula = interval~contrast,value.var = 'p.value')
    Tuk$sensor <- i
    Tuk$sensor_name <- files[sensor==i]$sensor_name
    p_vals <- rbind(p_vals,Tuk)
  }
}

write.table(p_vals,paste0(out_path,"p_vals_Tukey_by_feedback_cur_MEG.txt"))




