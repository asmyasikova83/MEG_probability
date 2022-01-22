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


#path <- 'C:/MEG/mixed_models/Low_Beta_cur/dataframe_delta_cur/'
#out_path <-'C:/MEG/mixed_models/Low_Beta_cur/p_values_LMEM/'
#out <- 'C:/MEG/mixed_models/Low_Beta_cur/p_values_LMEM/p_vals_fb_cur_Tukey_by_trial_type_MEG_delta.csv'
out_trial <- 'C:/MEG/mixed_models/Beta_cur/analysis_bline_nologdiv/p_vals_fb_cur_Tukey_by_trial_type_MEG_poster.csv'
out_fb <- 'C:/MEG/mixed_models/Beta_cur/analysis_bline_nologdiv/p_vals_Tukey_by_feedback_cur_MEG_poster.csv'



path_p <- 'C:/MEG/mixed_models/Beta_cur/analysis_bline_nologdiv/'
path <- 'C:/MEG/mixed_models/Beta_cur/dataframe_for_LMEM_bline_nologdiv/'
out_path <- 'C:/MEG/mixed_models/Beta_cur/analysis_bline_nologdiv/'

#### prepare table with info ####
sensor_info <- fread('C:/MEG/mixed_models/sensors.csv')
files <- data.table(full_filename=list.files(path, pattern = '*.csv', full.names = T))
files$short_filename <- list.files(path, pattern = '*.csv', full.names = F)

files[, sensor:=stri_extract_first_regex(short_filename,"[0-9]+")]
files[, interval:=str_extract(short_filename,'[0-9]+_[0-9]+.csv')]
# files[,interval:=gsub('.csv','',interval)]
files$sensor <- as.integer(files$sensor)
files <- merge.data.table(files,sensor_info,by = c('sensor'))
files$effect <- NULL

## load subj_list ##
subj_list <- fread('C:\\MEG\\mixed_models\\subj_list.csv')

#### make large table with p_values ####

temp <- fread(files[sensor==0]$full_filename)
temp$V1 <- NULL
cols <- colnames(temp)[grep('[0-9]',colnames(temp))]


# p_vals_large <- data.table(sensor=files$sensor,sensor_name=files$sensor_name)
# p_vals_large[,(cols):=0]
# colnames(p_vals_large) <- gsub('beta power','p_val',colnames(p_vals_large))

###### feedback_#######
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

#write.table(p_vals,paste0(out_path,"p_vals_Tukey_by_feedback_cur_MEG.csv"))
write.csv(p_vals, out_fb, row.names = TRUE)

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
  #if high beta rescale, center and check for singularity
  #temp_resc[,cols] <- scale(temp[,cols])
  #temp$`beta power [-0.9 -0.7]`<- scale(temp$`beta power [-0.9 -0.7]`)
  
  for (j in cols){
    m <- lmer(get(j) ~ trial_type*feedback_cur + (1|subject), data = temp)
    #m_sc <- update(m,data=temp_resc)
    Tuk <- data.table(summary(emmeans(m, pairwise ~ trial_type, adjust = 'tukey',lmer.df = "satterthwaite",lmerTest.limit=8000))$contrasts)
    Tuk[,contrast:=gsub(' - ','_',contrast)]
    Tuk[,p.value:=format(p.value, digits = 3)]
    
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
  
#write.table(p_vals,paste0(out_path, "p_vals_fb_prev_Tukey_by_trial_type_MEG_poster.csv"))
write.csv(p_vals, out_trial, row.names = TRUE)





