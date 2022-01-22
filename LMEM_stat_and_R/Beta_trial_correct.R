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
#analysis = '1800'

path_p <- 'C:/MEG/mixed_models/Beta_cur/analysis_bline_nologdiv/'
path <- 'C:/MEG/mixed_models/Beta_cur/dataframe_for_LMEM_bline_nologdiv/'
out_path <- 'C:/MEG/mixed_models/Beta_cur/analysis_bline_nologdiv/'

subj_list <- fread('C:\\MEG\\mixed_models\\subj_list.csv')

#if before feedback onset
#df <- fread (paste0(path_p, 'p_vals_factor_significance_MEG_decision_making.csv'))
#if after feedback onset
df <- fread (paste0(path_p, 'p_vals_factor_significance_MEG.csv'))
df$V1 <- NULL

df[, interaction_fdr:=p.adjust(`trial_type:feedback_cur`, method = 'fdr')]
df[, trial_fdr:=p.adjust(`trial_type`, method = 'fdr')] 

#sensors_2 <- unique(df[trial_fdr<0.05 & interval==" [-0.9 -0.7]"]$sensor_name)
#sensors_3 <- unique(df[trial_fdr<0.05 & interval==" [-0.7 -0.5]"]$sensor_name)
#sensors_4 <- unique(df[trial_fdr<0.05 & interval==" [-0.5 -0.3]"]$sensor_name)
#sensors_2 <- unique(df[trial_fdr<0.05 & interval==" [-0.9 -0.7]"]$sensor_name)
#sensors_3 <- unique(df[trial_fdr<0.05 & interval==" [-0.7 -0.5]"]$sensor_name)
#sensors_4 <- unique(df[trial_fdr<0.05 & interval==" [-0.5 -0.3]"]$sensor_name)
#sensors_5 <- unique(df[interaction_fdr<0.05 & interval==" [1.5 1.7]"]$sensor_name)
#sensors_6 <- unique(df[interaction_fdr<0.01 & interval==" [1.7 1.9]"]$sensor_name)
sensors_2 <- unique(df[trial_fdr<0.05 & interval==" [0.7 0.9]"]$sensor_name)
#sensors_2 <- unique(df[interval==" [0.7 0.9]"]$sensor_name)

#sensors_2 <- unique(df[trial_fdr<0.05 & interval==" [1.1 1.3]"]$sensor_name)
#sensors_3 <- unique(df[trial_fdr<0.05 & interval==" [1.3 1.5]"]$sensor_name)

#sensors_2 <- unique(df[trial_fdr<0.05 & interval==" [0.1 0.3]"]$sensor_name)
#sensors_3 <- unique(df[trial_fdr<0.05 & interval==" [0.3 0.5]"]$sensor_name)

#sensors_dual <- intersect(sensors_2, sensors_3)
#sensors_d2 <- intersect(sensors_dual, sensors_4)
#sensors_d3 <- intersect(sensors_d2, sensors_5)
#sensors_all <- intersect(sensors_d3, sensors_6)

#sensors_all <-sensors_2
#print(sensors_all)
#sensors_all <- intersect(sensors_2, sensors_3)

#sensors_all <- unique(df[trial_fdr<0.1 & interval==" [-0.5 -0.3]"]$sensor_name)

cluster_post_error <- c('MEG0312','MEG0322', 'MEG0342', 'MEG0512', 'MEG0522','MEG0532', 'MEG0542') #post-error cluster
anterior_cluster <-  c('MEG0222', 'MEG0232', 'MEG0322', 'MEG0332', 'MEG0342', 'MEG0412', 'MEG0422', 'MEG0442', 'MEG0612', 'MEG0632', 'MEG0722', 'MEG0732', 'MEG1042', 'MEG1622')

whole <- c('MEG0222', 'MEG0232', 'MEG0322', 'MEG0332', 'MEG0342','MEG0412', 'MEG0422', 'MEG0442', 'MEG0612',
'MEG0632', 'MEG0722', 'MEG0732','MEG1042','MEG1622','MEG1632','MEG1642','MEG1722', 'MEG1732', 'MEG1812', 'MEG1842',
'MEG1912', 'MEG1922','MEG2012','MEG2022','MEG2032','MEG2042','MEG2112', 'MEG2232','MEG2312','MEG2432', 'MEG2442')

occipital_cluster <-  c('MEG1632', 'MEG1642', 'MEG1722', 'MEG1732', 'MEG1842', 'MEG1912', 'MEG1922', 
                       'MEG2012', 'MEG2022', 'MEG2032', 'MEG2042', 'MEG2112', 'MEG2232', 'MEG2312', 'MEG2432', 
                        'MEG2442')

decision <- c('MEG0332', 'MEG0412', 'MEG0422', 'MEG0442', 'MEG0512', 'MEG0632', 'MEG0732', 'MEG0742', 'MEG1042',
              'MEG1112', 'MEG1122', 'MEG1132', 'MEG1142', 'MEG1242', 'MEG1622', 'MEG1812', 'MEG1822', 'MEG1832', 
              'MEG1842', 'MEG1912', 'MEG1922', 'MEG1942', 'MEG2012', 'MEG2022', 'MEG2032', 'MEG2042', 'MEG2112',
              'MEG2132', 'MEG2322', 'MEG2212', 'MEG2222', 'MEG2232', 'MEG2242', 'MEG2312', 'MEG2322', 'MEG2332',
              'MEG2342', 'MEG2442', 'MEG2512', 'MEG2522', 'MEG2642')
#check for specific behavior of beta band power in separate channels from frontal, central, parietal brain areas
#cluster_decision  <- c('MEG0332')

#cluster_decision  <- c('MEG0442')
#cluster_decision  <- c('MEG1912')

#set a cluster

#sensors_all <- cluster_post_error
#sensors_all <- cluster_decision 
#sensors_all <- occipital_cluster
#sensors_all <- decision

#choose 3 best channels

#20, 26, 59 for anterior
#60, 69 for occip
#sensors_all <- intersect(sensors_2,sensors_3)
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

# choose sensor which is a template for a df
# if whole
#sensor_choosen = 5 
#if occipital
#sensor_choosen = 60
#if post-error
#sensor_choosen = 16
#if decision
#200-400 ms sensor 59
sensor_choosen = 19
#sensor_choosen = 10 0332
#sensor_choosen = 15 #0442
#sensor_choosen = 70 #1912


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

#beta[,`mean beta power [0.1  0.5]`:=rowMeans(beta[,.SD,.SDcol=c("beta power [0.1 0.3]","beta power [0.3 0.5]")])] # an ugly hack

#beta[,`mean beta power [1.2  1.4]`:=rowMeans(beta[,.SD,.SDcol=c("beta power [1.1 1.3]","beta power [1.3 1.5]")])] # an ugly hack

#beta[,`mean beta power [1.5  1.9]`:=rowMeans(beta[,.SD,.SDcol=c("beta power [1.5 1.7]","beta power [1.7 1.9]")])] # an ugly hack
beta[,`mean beta power [0.7  0.9]`:=rowMeans(beta[,.SD,.SDcol=c("beta power [0.7 0.9]","beta power [0.7 0.9]")])] # an ugly hack
#beta[,`mean beta power [-0.9  -0.1]`:=rowMeans(beta[,.SD,.SDcol=c("beta power [-0.9 -0.7]","beta power [-0.7 -0.5]", "beta power [-0.5 -0.3]", "beta power [-0.3 -0.1]")])] # an ugly hack

beta[, index := 1:.N, by=c('subject','sensor')] #set indexes of all trials of each subject, same for all sensors

# compute means of sensors

#means <- beta[, mean(`mean beta power [1.2  1.4]`),by=c('subject','index')]
#means <- beta[, mean(`mean beta power [1.5  1.9]`),by=c('subject','index')]
means <- beta[, mean(`mean beta power [0.7  0.9]`),by=c('subject','index')]
#means <- beta[, mean(`mean beta power [-0.9  -0.1]`),by=c('subject','index')]
#means <- beta[, mean(`mean beta power [0.1  0.5]`),by=c('subject','index')]

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
#if after feedback onset
#m <- lmer(get(interval) ~ trial_type*feedback_cur + (1|subject),data = means) # main part, fit model
m <- lmer(get(interval) ~ trial_type + (1|subject),data = means) # main part, fit model!
m2 <- m # it is because we missed step, so final model=initial model
print(anova(m2))
# plot Tukey over trial types

# prepare table with statistics 
interval <- 'mean_beta'
Tuk <- data.table(summary(emmeans(m2, pairwise ~ trial_type, adjust = 'tukey',lmer.df = "satterthwaite",lmerTest.limit=8000))$contrasts) #if trial number >8000 change limit 
Tuk <- Tuk[, group1:=gsub(' -.*', '', contrast)][, group2:=gsub('.*- ', '', contrast)]
Tuk <- Tuk[p.value<0.1, p_significant:=format(p.value, digits = 3)]

# compute y_position to draw p-value on graph
n <- Tuk[!is.na(p_significant), .N]

print(n)

#thr <- max(means[, mean(get(interval)) + sterr(get(interval)), by=trial_type]$V1) #
thr <- max(means[, abs(mean(get(interval))), by=trial_type]$V1)
print(means[, abs(mean(get(interval))), by=trial_type]$V1)
print(unique(means$trial_type))

#TODO ask Kseniya
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

print(Tuk)
##### Tukey by trial_type #####


# prepare table with statistics  
Tuk <- data.table(summary(emmeans(m2, pairwise ~ trial_type, adjust = 'tukey',lmer.df = "satterthwaite",lmerTest.limit=8000))$contrasts) #if trial number >8000 change limit 
Tuk <- Tuk[, group1:=gsub(' -.*', '', contrast)][, group2:=gsub('.*- ', '', contrast)]
Tuk <- Tuk[p.value<0.1, p_significant:=format(p.value, digits = 3)]

# compute y_position to draw p-value on graph
n <- Tuk[!is.na(p_significant), .N]

#thr <- max(means[, mean(get(interval)) + sterr(get(interval)), by=trial_type]$V1) #
#0.2 is added for early response
thr <- max(means[,  0.2+mean(get(interval)), by=trial_type]$V1) #
thr <- thr+0.02 #for RT
if (n>1){
  Tuk <- Tuk[!is.na(p_significant), y.position := seq((thr+0.05), (thr+0.355), 0.3/(n-1))] #here you can choose other values
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
            size = 2.0,
            #ylab = 'Mean beta 200-400 ms postfeedback', xlab = "Trial type",
            #ylab = 'Mean beta 600-800 ms postfeedback', xlab = "Trial type",
            ylab = 'Mean beta 800 ms after response', xlab = "Trial type",
            #ylab = 'Mean beta 300 ms after response', xlab = "Trial type",
            #ylab = 'Mean beta 800-200 ms prior to response', xlab = "Trial type",
            font.label = list(size = 25, color = "black"))+
  theme(axis.title.x = element_text(size=26),
        axis.text.x  = element_text(size=24),
        axis.line = element_line(size = 3),
        axis.ticks = element_line(size = 5) , 
        axis.ticks.length = unit(.5, "cm"),
        axis.title.y = element_text(size=26)) +
  
  stat_pvalue_manual(Tuk, label = 'stars', size = 14, tip.length = 0.005)

ggpar(p,
      #ylim = c(-5.5,-3.5),#decision 1912
      #ylim = c(-4.5,-2.0),#decision 0332
      #ylim = c(-2.5,-0.5),#decision 0332
      #ylim = c(-3.5, 1.0),#decision
      #ylim = c(-2.0, 0.0),#early response
      #ylim = c(-4.2,-2.5),#occipital
      #ylim = c(-1.1,0.10), #feedback effects
      ylim = c(0.0,2.1), #post error
      #ylim = c(-0.0,1.1), #post error
      font.ytickslab = 40,
)
# theme_bw()+
# theme(text = element_text(size=13))
ggsave(filename = paste0(out_path,'_Tukey_trial_type_anticip__thicker_font','.png'), width =  10, height = 8)

#save Tukey inside trial_type
Tuk <- Tuk[, c(1:6,11)]
write.csv(Tuk,paste0(out_path, 'Tuk_trial_type.csv'))

png(paste0(out_path, 'Tuk_trial_type.png'), height = 30*nrow(Tuk), width = 100*ncol(Tuk))
grid.table(Tuk)
dev.off()
