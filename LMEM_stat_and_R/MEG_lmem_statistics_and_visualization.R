
library(reshape2)
library(data.table)
library(ggplot2)
library(lme4)
library("ggpubr")
library(emmeans)
library(lmerTest)

path_p <- 'C:/Users/Ksenia/Desktop/project_probability/LMM_MEG/p_values_LMEM/' # path to files with p-vals
path <- 'C:/Users/Ksenia/Desktop/project_probability/LMM_MEG/dataframe_for_LMEM/'

out_path <- 'C:/Users/Ksenia/Desktop/project_probability/LMM_MEG/analysis/' ## path to save tables and pictures

## load subj_list ##
subj_list <- fread('C:/Users/Ksenia/Desktop/project_probability/LMM_MEG/subj_list.csv')


df <- fread (paste0(path_p, 'p_vals_factor_significance_MEG.csv'))
df$V1 <- NULL

# fdr 
df[, interaction_fdr:=p.adjust(`trial_type:feedback_cur`, method = 'fdr')]


# choose sensors signigicant in both intervals
sensors_1 <- unique(df[interaction_fdr<0.05 & interval==" [1.5 1.7]"]$sensor_name)
sensors_2 <- unique(df[interaction_fdr<0.05 & interval==" [1.7 1.9]"]$sensor_name)

sensors_all <- intersect(sensors_1,sensors_2) 



####### make dataframe with files info ########



sensor_info <- fread('C:/Users/Ksenia/Desktop/Events/sensors.csv')
files <- data.table(full_filename=list.files(path, pattern = '*.csv', full.names = T))
files$short_filename <- list.files(path, pattern = '*.csv', full.names = F)

# files$short_filename <- gsub('planar2','',files$short_filename)

files[, sensor:=stri_extract_first_regex(short_filename,"[0-9]+")]
# files[, interval:=str_extract(short_filename,'[0-9]+_[0-9]+.csv')]
# files[,interval:=gsub('.csv','',interval)]
files$sensor <- as.integer(files$sensor)
files <- merge.data.table(files,sensor_info,by = c('sensor'))
files$effect <- NULL





##### filter files and leave needed sensors only ######



files <- files[sensor_name %in% sensors_all] 


######## collect data and average #############

temp <- fread(files[sensor==5]$full_filename) #donor of colnames for empty datatable "beta"
temp$V1 <- NULL
beta <- setNames(data.table(matrix(nrow = 0, ncol = length(colnames(temp))+2)), c(colnames(temp),'sensor','sensor_name'))

for (i in files$sensor){
  temp <- fread(files[sensor==i]$full_filename)
  temp$V1 <- NULL
  temp <- as.data.table(temp)
  temp <- temp[subject %in% subj_list$subj_list]
  
  temp$sensor <- i
  temp$sensor_name <- files[sensor==i]$sensor_name
  
  beta <- rbind(beta,temp)
}

beta[,`mean beta power [1.5  1.9]`:=rowMeans(beta[,.SD,.SDcol=c("beta power [1.5 1.7]","beta power [1.7 1.9]")])] # mean of intervals 


beta[, index := 1:.N, by=c('subject','sensor')] #set indexes of all trials of each subject, same for all sensors 


means <- beta[, mean(`mean beta power [1.5  1.9]`),by=c('subject','index')] # compute means of sensors

cols <- c("subject","round","trial_type","feedback_cur","feedback_prev","scheme",'index')
means <- merge.data.table(means,beta[sensor==5, ..cols], by = c('subject','index'), all.x = TRUE) # take trial classification from "beta", sensor is random you can take any
  
means$subject <- as.factor(means$subject)
means$round <- as.factor(means$round)
means$feedback_cur <-as.factor(means$feedback_cur)
means$feedback_prev <-as.factor(means$feedback_prev)
means$scheme <-as.factor(means$scheme)
means$trial_type <- as.factor(means$trial_type)

setnames(means,'V1','mean_beta')


####### analysis ##########

interval <- 'mean_beta' #name of dependent variable

m <- lmer(get(interval) ~ trial_type*feedback_cur + (1|subject),data = means) # main part, fit model!
m2 <- m # it is because we missed step, so final model=initial model

#save anova table with fixed effects significance 
an <- anova(m2)
an <- data.table(an,keep.rownames = TRUE)
an[`Pr(>F)`<0.001, stars:='***']
an[`Pr(>F)`<0.01 & `Pr(>F)`>0.001 , stars:='**']
an[`Pr(>F)`<0.05 & `Pr(>F)`>0.01 , stars:='*']
an[`Pr(>F)`>0.05 & `Pr(>F)`<0.1 , stars:='#']
write.csv(an,paste0(out_path,'_anova.csv'))
png(paste0(out_path,'_anova.png'), height = 30*nrow(an), width = 100*ncol(an))
grid.table(an)
dev.off()


#save ranova table with random effects significance 


ran <- ranova(m2)
ran <- data.table(ran,keep.rownames = TRUE)
ran[`Pr(>Chisq)`<0.001, stars:='***']
ran[`Pr(>Chisq)`<0.01 & `Pr(>Chisq)`>0.001 , stars:='**']
ran[`Pr(>Chisq)`<0.05 & `Pr(>Chisq)`>0.01 , stars:='*']
ran[`Pr(>Chisq)`>0.05 & `Pr(>Chisq)`<0.1 , stars:='#']
# ran <- format(ran, digits = 3)
write.csv(ran,paste0(out_path,'ranova.csv'))
png(paste0(out_path,'ranova.png'), height = 30*nrow(ran), width = 100*ncol(ran))
grid.table(ran)
dev.off()


##### Tukey by trial_type #####


# prepare table with statistics  
Tuk <- data.table(summary(emmeans(m2, pairwise ~ trial_type, adjust = 'tukey',lmer.df = "satterthwaite",lmerTest.limit=8000))$contrasts) #if trial number >8000 change limit 
Tuk <- Tuk[, group1:=gsub(' -.*', '', contrast)][, group2:=gsub('.*- ', '', contrast)]
Tuk <- Tuk[p.value<0.1, p_significant:=format(p.value, digits = 3)]

# compute y_position to draw p-value on graph
n <- Tuk[!is.na(p_significant), .N]

thr <- max(means[, mean(get(interval)) + sterr(get(interval)), by=trial_type]$V1) #
thr <- thr+0.02 #for RT
if (n>1){
  Tuk <- Tuk[!is.na(p_significant), y.position := seq((thr+0.005), (thr+0.305), 0.3/(n-1))] #here you can choose other values
} else {
  Tuk <- Tuk[!is.na(p_significant), y.position := thr+0.02]
}

Tuk[p.value<0.001, stars:='***']
Tuk[p.value<0.01 & p.value>0.001 , stars:='**']
Tuk[p.value<0.05 & p.value>0.01 , stars:='*']
Tuk[p.value>0.05 & p.value<0.1 , stars:='#']


# plot Tukey


p <- ggline(means, 'trial_type', interval,
       add = c("mean_se"),
       order = c("norisk","prerisk","risk", "postrisk"),
       ylab = 'Mean beta power (1.5-1.9 s)', xlab = "Trial type",
       font.label = list(size = 15, color = "black"))+
  theme(axis.title.x = element_text(size=16),
        axis.text.x  = element_text(size=14),
        axis.title.y = element_text(size=16)) + 
  
  
  stat_pvalue_manual(Tuk, label = 'stars', size = 6, tip.length = 0.001)

ggpar(p,
      # ylim = c(-1.85,-1.15),
      ylim = c(-2.8,-0.7), #you must choose values suitable for feedback analysis and for this
      # ylim = c(-0.25,0.1), #-400-0
      font.ytickslab = 16,
)
# theme_bw()+
# theme(text = element_text(size=13))
ggsave(filename = paste0(out_path,'_Tukey_trial_type_1.5-1.9','.png'), width =  6, height = 5)

#save Tukey inside trial_type
Tuk <- Tuk[, c(1:6,11)]
write.csv(Tuk,paste0(out_path, 'Tuk_trial_type.csv'))

png(paste0(out_path, 'Tuk_trial_type.png'), height = 30*nrow(Tuk), width = 100*ncol(Tuk))
grid.table(Tuk)
dev.off()




########## Tukey feedback inside trial_type ##########

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
                    mean(get(interval))+sterr(get(interval)),by='trial_type']
setnames(y_values_rew,'V1','y_values_rew')

y_values_lose <- means[feedback_cur == 'negative',
                     mean(get(interval))+sterr(get(interval)),by='trial_type']
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
       ylab = 'Mean beta power (1.5-1.9 s)', xlab = "Trial type",
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
      ylim = c(-2.8,-0.7), 
      font.ytickslab = 16,
)
# theme_bw()+
# theme(text = element_text(size=13))
ggsave(filename = paste0(out_path,'_Tukey_feedback_cur_1.5-1.9','.png'), width =  6, height = 5)

# save Tukey feedback cur #
write.csv(Tuk1,paste0(out_path,'Tuk_feedback_cur.csv'))

png(paste0(out_path,'Tuk_feedback_cur.png'), height = 30*nrow(Tuk1), width = 100*ncol(Tuk1))
grid.table(Tuk1)
dev.off()

  


