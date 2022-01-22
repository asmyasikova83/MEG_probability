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


rm(list = ls())

path_p <- 'C:/MEG/mixed_models/Beta_cur/analysis_bline_nologdiv/'
path <- 'C:/MEG/mixed_models/Beta_cur/dataframe_for_LMEM_bline_nologdiv/'
out_path <- 'C:/MEG/mixed_models/Beta_cur/analysis_bline_nologdiv/'

subj_list <- fread('C:\\MEG\\mixed_models\\subj_list.csv')

df <- fread (paste0(path_p, 'p_vals_factor_significance_MEG.csv'))
df$V1 <- NULL


df[, interaction_fdr:=p.adjust(`trial_type:feedback_cur`, method = 'fdr')]
df[, trial_type_fdr:=p.adjust(`trial_type`, method = 'fdr')]
df[, feedback_cur_fdr:=p.adjust(`feedback_cur`, method = 'fdr')]

# choose sensors signigficant in both intervals
#sensors_2 <- unique(df[`trial_type:feedback_cur`<0.05 & interval=="[1.7 1.9]"]$sensor_name)
#sensors_3 <- unique(df[`trial_type:feedback_cur`<0.05 & interval=="[1.9 2.1]"]$sensor_name)
# time interval is based on the interction trial_type*feedbak_cur with fdr adj
sensors_2 <- unique(df[interaction_fdr<0.05 & interval==" [1.5 1.7]"]$sensor_name)
sensors_3 <- unique(df[interaction_fdr<0.05 & interval==" [1.7 1.9]"]$sensor_name)
#sensors_2 <- unique(df[trial_type_fdr<0.05 & interval==" [-0.5 -0.3]"]$sensor_name)
#sensors_3 <- unique(df[trial_type_fdr<0.05 & interval==" [-0.3 -0.1]"]$sensor_name)
#anterior_cluster <-  c('MEG0222', 'MEG0232', 'MEG0322', 'MEG0332', 'MEG0342', 'MEG0412', 'MEG0422', 'MEG0442', 'MEG0612', 'MEG0632', 'MEG0722', 'MEG0732', 'MEG1042', 'MEG1542', 'MEG1622')
occipital_cluster <-  c('MEG1632', 'MEG1642', 'MEG1722', 'MEG1732', 'MEG1842', 'MEG1912', 'MEG1922', 'MEG2012', 'MEG2022', 'MEG2032', 'MEG2042', 'MEG2112', 'MEG2232', 'MEG2312', 'MEG2432', 'MEG2442', 'MEG2622')
#sensors_all <- intersect(sensors_2,sensors_3)
sensors_all <- occipital_cluster
#sensors_all <- anterior_cluster
#for decision making anterior
#sensors_all <-  c('MEG0442','MEG0632', 'MEG0742', 'MEG1042', 'MEG1112', 'MEG1122', 'MEG1132', 'MEG1142', 'MEG1242', 'MEG1812')
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

#sensor_choosen = 63 #for all, occipital
sensor_choosen = 60
#sensor_choosen = 66

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

beta[,`mean beta power [1.5  1.9]`:=rowMeans(beta[,.SD,.SDcol=c("beta power [1.5 1.7]","beta power [1.7 1.9]")])] # mean of intervals
#beta[,`mean beta power [-0.5  -0.1]`:=rowMeans(beta[,.SD,.SDcol=c("beta power [-0.5 -0.3]","beta power [-0.3 -0.1]")])] # mean of intervals
beta[, index := 1:.N, by=c('subject','sensor')] #set indexes of all trials of each subject, same for all sensors 
means <- beta[, mean(`mean beta power [1.5  1.9]`),by=c('subject','index')] # compute means of sensors
#means <- beta[, mean(`mean beta power [-0.5  -0.1]`),by=c('subject','index')] # compute means of sensors
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

p1 <- ggline(means[subject %in% unique(subject)], 'trial_type', interval, 
            color = "subject",
            facet.by = "feedback_cur",
            add = c("mean_se"),
            order = c("norisk","prerisk","risk", "postrisk"),
            ylab = 'Mean beta (1.5-1.9 s)', xlab = "Trial type",
            size = 2)+
     theme(legend.position=c(0.49,0.80),
       legend.direction = "vertical",
        text = element_text(size=40),
        legend.background = element_rect(size=0.01, linetype="solid",colour = 'red'),
        axis.title.x = element_text(size=40),
        axis.text.x  = element_text(size=36),
        axis.title.y = element_text(size=40))
  
ggpar(p1,
      #ylim = c(-1.00,2.0),
      #ylim = c(-3.00,-1.0),
      ylim = c(-10.02, 7.22),
      font.ytickslab = 46,
)
# theme_bw()+
# theme(text = element_text(size=13))
ggsave(filename = paste0(out_path,'_SUBJ','.png'), width =  26, height = 25)

# save Tukey feedback cur #
write.csv(Tuk1,paste0(out_path,'Tuk_feedback_cur.csv'))

png(paste0(out_path,'Tuk_feedback_cur.png'), height = 30*nrow(Tuk1), width = 100*ncol(Tuk1))
grid.table(Tuk1)
dev.off()


