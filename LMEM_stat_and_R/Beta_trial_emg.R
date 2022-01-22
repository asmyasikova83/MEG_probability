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

path_p <- 'C:/MEG/mixed_models/analysis_emg_oculo/'
path <- 'C:/MEG/mixed_models/analysis_emg_oculo/'
out_path <- 'C:/MEG/mixed_models/analysis_emg_oculo/emg/'

subj_list <- fread('C:\\MEG\\mixed_models\\subj_list.csv')


#if before feedback onset
#df <- fread (paste0(path_p, 'p_vals_factor_significance_MEG_decision_making.csv'))
#if after feedback onset
#df <- fread (paste0(path_p, 'p_vals_factor_significance_veog_trial_type.csv'))
df <- fread (paste0(path_p, 'p_vals_factor_significance_heog_interaction.csv'))
df$V1 <- NULL

df[, interaction_fdr:=p.adjust(`trial_type:feedback_cur`, method = 'fdr')]
df[, trial_fdr:=p.adjust(`trial_type`, method = 'fdr')] 
df[, feedback_cur_fdr:=p.adjust(`feedback_cur`, method = 'fdr')] 

beta <- fread('C:/MEG/mixed_models/analysis_emg_oculo/df_LMEM_heog.csv') 
#beta$V1 <- NULL
beta <- as.data.table(beta)
beta <- beta[subject %in% subj_list$subj_list]

#beta[,`mean beta`:=rowMeans(beta[,.SD,.SDcol=c("beta power [1.5 1.7]","beta power [1.7 1.9]")])] # an ugly hack
beta[,`mean beta`:=rowMeans(beta[,.SD,.SDcol=c("beta power [1.5 1.7]","beta power [1.7 1.9]")])]
beta[, index := 1:.N, by=c('subject')] #set indexes of all trials of each subject
means <- beta[, mean(`mean beta`),by=c('subject','index')]

cols <- c("subject","round","trial_type","feedback_cur","feedback_prev","scheme",'index')
means <- merge.data.table(means,beta[, ..cols], by = c('subject','index'), all.x = TRUE) # take trial classification from "beta", sensor is random you can take any

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
##ggqqplot(residuals(m))
Tuk <- emmeans(m2, pairwise ~ trial_type, adjust = 'tukey',lmer.df = "satterthwaite",lmerTest.limit=8000)

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
thr <- max(means[, mean(get(interval)), by=trial_type]$V1) #
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
            ylab = 'Mean Beta heog 600-800 s postfb', xlab = "Trial type",
            font.label = list(size = 15, color = "black"))+
  theme(axis.title.x = element_text(size=16),
        axis.text.x  = element_text(size=14),
        axis.title.y = element_text(size=16)) + 
  
  
  stat_pvalue_manual(Tuk, label = 'stars', size = 6, tip.length = 0.001)

ggpar(p,
      ylim = c(-1.0, 2.0), #anterior
      font.ytickslab = 16,
)
# theme_bw()+
# theme(text = element_text(size=13))
ggsave(filename = paste0(out_path,'_Tukey_by_trial_1.5_1.9_heog.png'), width =  6, height = 5)
#save Tukey inside trial_type
Tuk <- Tuk[, c(1:6,11)]
write.csv(Tuk,paste0(out_path, 'Tuk_trial_type.csv'))

png(paste0(out_path, 'Tuk_trial_type.png'), height = 30*nrow(Tuk), width = 100*ncol(Tuk))
grid.table(Tuk)
dev.off()