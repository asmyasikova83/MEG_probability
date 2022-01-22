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


path_p <- 'C:/MEG/mixed_models/analysis_emg_oculo/'
path <- 'C:/MEG/mixed_models/analysis_emg_oculo/'
out_path <- 'C:/MEG/mixed_models/analysis_emg_oculo/'

subj_list <- fread('C:\\MEG\\mixed_models\\subj_list.csv')

#### make large table with p_values ####

#temp <- fread('C:/MEG/mixed_models/analysis_emg_oculo/df_LMEM_emg.csv')
#temp <- fread('C:/MEG/mixed_models/analysis_emg_oculo/df_LMEM_veog.csv')
temp <- fread('C:/MEG/mixed_models/analysis_emg_oculo/df_LMEM_heog.csv')

temp$V1 <- NULL
cols <- colnames(temp)[grep('[0-9]',colnames(temp))]

######## for trial_type #############
p_vals <- data.table()
temp <- temp[subject %in% subj_list$subj_list]
  
temp$subject <- as.factor(temp$subject)
temp$round <- as.factor(temp$round)
temp$feedback_cur <-as.factor(temp$feedback_cur)
temp$feedback_prev <-as.factor(temp$feedback_prev)
temp$scheme <-as.factor(temp$scheme)
temp$trial_type <- as.factor(temp$trial_type)
 
for (j in cols){
  #m <- lmer(get(j) ~ trial_type + (1|subject), data = temp)
  #m <- lmer(get(j) ~ feedback_cur + (1|subject), data = temp)
  m <- lmer(get(j) ~ trial_type*feedback_cur + (1|subject), data = temp)
  an <- anova(m)
  an <- data.table(an,keep.rownames = TRUE)
  an_cols <- c('rn','Pr(>F)') 
  an <- an[, ..an_cols]
  an$`Pr(>F)` <- format(an$`Pr(>F)`, digits = 3)
  an$interval <- j
  an$interval <- gsub('beta power','',an$interval)
  an <- dcast(an,formula = interval~rn,value.var = 'Pr(>F)')
  p_vals <- rbind(p_vals,an)
 }
#write.csv(p_vals,paste0(out_path, "p_vals_factor_significance_emg_trial_type.csv"))
#write.csv(p_vals,paste0(out_path, "p_vals_factor_significance_emg_interaction.csv"))
#write.csv(p_vals,paste0(out_path, "p_vals_factor_significance_veog_trial_type.csv"))
#write.csv(p_vals,paste0(out_path, "p_vals_factor_significance_veog_feedback_cur.csv"))
#write.csv(p_vals,paste0(out_path, "p_vals_factor_significance_veog_interaction.csv"))
write.csv(p_vals,paste0(out_path, "p_vals_factor_significance_heog_interaction.csv"))

