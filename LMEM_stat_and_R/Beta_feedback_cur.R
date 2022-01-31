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

#cluster_post_error <- c('MEG0312','MEG0322', 'MEG0342', 'MEG0512', 'MEG0522','MEG0532', 'MEG0542') #post-error cluster
#cluster_decision  <- c('MEG0222', 'MEG0232', 'MEG0322','MEG0332','MEG0412', 'MEG0422', 'MEG0432',
#                       'MEG0442','MEG0622','MEG0632','MEG0712','MEG0732','MEG0742','MEG1032',
#                       'MEG1042','MEG1112','MEG1122', 'MEG1132','MEG1142', 'MEG1242','MEG1622',
#                       'MEG1632', 'MEG1732','MEG1812','MEG1822','MEG1832', 'MEG1842',' MEG1912',
#                       'MEG1922','MEG1932','MEG1942',' MEG2012','MEG2022',' MEG2032','MEG2042',
#                       'MEG2112','MEG2122','MEG2212','MEG2222','MEG2232','MEG2242','MEG2312',
#                       'MEG2322','MEG2332','MEG2342','MEG2442','MEG2512')
anterior_cluster <-  c('MEG0222', 'MEG0232', 'MEG0322', 'MEG0332', 'MEG0342', 'MEG0412', 'MEG0422', 'MEG0442', 'MEG0612', 'MEG0632', 'MEG0722', 'MEG0732', 'MEG1042', 'MEG1622')
#cluster_decision  <- c('MEG0332')

#cluster_decision  <- c('MEG0442')
#cluster_decision  <- c('MEG1912')

whole <- c('MEG0222', 'MEG0232', 'MEG0322', 'MEG0332', 'MEG0342','MEG0412', 'MEG0422', 'MEG0442', 'MEG0612',
           'MEG0632', 'MEG0722', 'MEG0732','MEG1042','MEG1622','MEG1632','MEG1642','MEG1722', 'MEG1732', 'MEG1812', 'MEG1842',
           'MEG1912', 'MEG1922','MEG2012','MEG2022','MEG2032','MEG2042','MEG2112', 'MEG2232','MEG2312','MEG2432', 'MEG2442')

occipital_cluster <-  c('MEG1632', 'MEG1642', 'MEG1722', 'MEG1732', 'MEG1842', 'MEG1912', 'MEG1922', 
                        'MEG2012', 'MEG2022', 'MEG2032', 'MEG2042', 'MEG2112', 'MEG2232', 'MEG2312', 'MEG2432', 
                        'MEG2442')

#cluster_post_error<- c('MEG0312','MEG0512','MEG0542')

#whole cluster for fb, no outliers
sensors_all <- c('MEG0222', 'MEG0232', 'MEG0322', 'MEG0332', 'MEG0342', 'MEG0412', 'MEG0422', 'MEG0442', 'MEG0612',
                 'MEG0632', 'MEG0722', 'MEG0732', 'MEG1042', 'MEG1622', 'MEG1632', 'MEG1642', 'MEG1722', 'MEG1732',
                 'MEG1842', 'MEG1912', 'MEG1922', 'MEG2012', 'MEG2022', 'MEG2032', 'MEG2042', 'MEG2112', 'MEG2232',
                 'MEG2312', 'MEG2432', 'MEG2442') 
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

# choose sensor whole, occip, decision 15, pos-error 16 
sensor_choosen = 15

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

beta[, index := 1:.N, by=c('subject','sensor')] #set indexes of all trials of each subject, same for all sensors

# compute means of sensors
means <- beta[, mean(`mean beta power [1.5  1.9]`),by=c('subject','index')]

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
y_values <- merge(y_values,signif,by='trial_type')

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
  geom_hline(yintercept=-0.0, linetype='dashed', col = 'black', size = 1)+
  #scale_color_discrete(name = "Previous feedback", labels = c("Loss", "Gain"))+
  
  # theme_bw()+
#  theme(legend.position=c(0.52,0.85),
#        legend.direction = "vertical",
#        text = element_text(size=18),
#        legend.background = element_rect(size=0.01, linetype="solid",colour = 'black'),
#        axis.title.x = element_text(size=18),
#        axis.text.x  = element_text(size=16),
#        axis.title.y = element_text(size=18))+
 
  theme(text = element_text(size=18),
        legend.background = element_rect(size=0.01, linetype="solid",colour = 'black'),
        axis.title.x = element_text(size=26),
        axis.text.x  = element_text(size=24),
        axis.line = element_line(size = 2),
        axis.ticks = element_line(size = 5) , 
        axis.ticks.length = unit(.5, "cm"),
        axis.title.y = element_text(size=16)) + 

  geom_signif(y_position=c(y_values$y_max +0.05),
              xmin=c(y_values$number-0.075), xmax=c(y_values$number+0.075),
              annotation=c(y_values$stars), 
              tip_length=0.001,textsize = 12,vjust = 0.4)

ggpar(p1,
      ylim = c(-2.0,0.0), #whole
      #ylim = c(-3.5,0.0), #occip
      #ylim = c(-1.1,2.0), #anterior
      font.ytickslab = 20,
)
ggsave(filename = paste0(out_path,'_Tukey_feedback_FIG6_whole_cur','.png'), width =  6, height = 5)

# save Tukey feedback cur #
write.csv(Tuk1,paste0(out_path,'Tuk_feedback_cur.csv'))

png(paste0(out_path,'Tuk_feedback_cur.png'), height = 30*nrow(Tuk1), width = 100*ncol(Tuk1))
#grid.table(Tuk1)
dev.off()
