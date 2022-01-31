library(data.table)
library(lme4)
library(emmeans)
library(lmerTest)
library(ggplot2)
library(reshape2)
library(data.table)
library(ggplot2)
library(lme4)
library("ggpubr")
library( dplyr )
library(stringi)

path_p <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_bline_nologdiv/'
path <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/dataframe_for_LMEM_bline_nologdiv/'
out_path <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Beta_cur/analysis_bline_nologdiv/'


subj_list <- fread('C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/subj_list.csv')


#if before feedback onset
#df <- fread (paste0(path_p, 'p_vals_factor_significance_MEG_decision_making.csv'))
#if after feedback onset
df <- fread (paste0(path_p, 'p_vals_factor_significance_MEG.csv'))
df$V1 <- NULL

df[, interaction_fdr:=p.adjust(`trial_type:feedback_cur`, method = 'fdr')]
df[, trial_fdr:=p.adjust(`trial_type`, method = 'fdr')]   

anterior_cluster <-  c('MEG0222', 'MEG0232', 'MEG0322', 'MEG0332', 'MEG0342', 'MEG0412', 'MEG0422', 'MEG0442', 'MEG0612', 'MEG0632', 'MEG0722', 'MEG0732', 'MEG1042', 'MEG1622')

occipital_cluster <-  c('MEG1632', 'MEG1642', 'MEG1722', 'MEG1732', 'MEG1842', 'MEG1912', 'MEG1922', 
                        'MEG2012', 'MEG2022', 'MEG2032', 'MEG2042', 'MEG2112', 'MEG2232', 'MEG2312', 'MEG2432', 
                        'MEG2442')
whole <- c('MEG0222', 'MEG0232', 'MEG0322', 'MEG0332', 'MEG0342', 'MEG0412', 'MEG0422', 'MEG0442', 'MEG0612',
           'MEG0632', 'MEG0722', 'MEG0732', 'MEG1042', 'MEG1622', 'MEG1632', 'MEG1642', 'MEG1722', 'MEG1732',
           'MEG1842', 'MEG1912', 'MEG1922', 'MEG2012', 'MEG2022', 'MEG2032', 'MEG2042', 'MEG2112', 'MEG2232',
           'MEG2312', 'MEG2432', 'MEG2442') 

#sensors_all <- intersect(sensors_2,sensors_3)
sensors_all <- whole 
print(sensors_all)

sensor_info <- fread('C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/sensors.csv')
files <- data.table(full_filename=list.files(path, pattern = '*.csv', full.names = T))
files$short_filename <- list.files(path, pattern = '*.csv', full.names = F)

files[, sensor:=stri_extract_first_regex(short_filename,"[0-9]+")]
files$sensor <- as.integer(files$sensor)
files <- merge.data.table(files,sensor_info,by = c('sensor'))
files$effect <- NULL

files <- files[sensor_name %in% sensors_all]

print(files)

# choose sensor
sensor_choosen = 60

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
print(summary(m))
# get Tukey
result <- emmeans(m2, pairwise ~ trial_type, adjust = 'tukey',lmer.df = "satterthwaite",lmerTest.limit=8000) # Tukey inside "trial type" factor
print(summary(result))

# get usual means
#means <- df[, mean(get(interval)), by = 'trial_type']
means <- beta[, mean(`mean beta power [1.5  1.9]`), by = 'trial_type']
means$mean <- 'usual_mean'
setnames(means,'V1','mean_beta')


# get estimated marginal means

em_means <- summary(result$emmeans)
em_means <- data.table(em_means)
em_means <- em_means[, c('trial_type','emmean')]
setnames(em_means,'emmean','mean_beta')
em_means$mean <- 'emmean'

#the same order of trial_types as in means
em_means_ed<- data.table(em_means)
em_means_ed[1,] <- em_means[1,]
em_means_ed[2,] <- em_means[3,]
em_means_ed[3,] <- em_means[4,]
em_means_ed[4,] <- em_means[2,]

#av <- fread (paste0(path_p, 'averaged_mean.csv'))
#av$V1 <- NULL

# bind all means
all_means <- rbind(means, em_means_ed)


# plot to compare means
all_means
ggplot(data=all_means, aes(x=trial_type, y=mean_beta, group=mean, color=mean, size = 0.2)) +
  ylim(-1.3,-0.5)+
  geom_line() +
  geom_point()+
#  theme_bw()
  theme(
        text = element_text(size=18),
        legend.background = element_rect(size=0.01, linetype="solid",colour = 'black'),
        axis.title.x = element_text(size=18),
        axis.text.x  = element_text(size=16),
        axis.title.y = element_text(size=18))
ggsave(filename = paste0(out_path,'_usual_means_feedbak_cur','.png'), width =  8, height = 7)
