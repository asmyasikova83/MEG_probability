library(data.table)
library(dplyr)
library("ggplot2")
library("ggpubr")

#count and draw trial types over subjects

df <- fread('C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/events_classification_clean_autists.tsv') #Lera's table
path <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Events_autists_test/' #out_path

cols <- c('event[0] (time)','event[1]','event[2] (label)','response class','cur_fb','prev_fb')

df$`response class` <- gsub('_','',df$`response class`) #pre_risk to prerisk (delete '_')
df[cur_fb=="cur_lose",cur_fb:='negative'] #rename
df[cur_fb=="cur_rew",cur_fb:='positive']
df[prev_fb=="prev_lose",prev_fb:='negative'] #rename
df[prev_fb=="prev_rew",prev_fb:='positive']


#filter df, consider only those trials with previous gains, remove `prev_fb`=='positive if not needed  
#df <- df[`response time class`=='normal' & `learning criteria`=='trained' & `prev_fb`=='positive'] 
df <- df[`response time class`=='normal' & `learning criteria`=='trained']

colnames_table <- c('subj', 'run', 'response class', 'cur_fb', 'event[2] (label)')
#df <- data.table(va = )
subj_table <- setNames(data.table(matrix(nrow = 0, ncol = 5)), c('subj', 'run', 'response class', 'cur_fb', 'event[2] (label)'))
print(subj_table)

for (subject in unique(df$subj)){
#for (subject in 'P333'){
  for (runn in c('run1','run2','run3','run4','run5','run6')){
    for (trial_type in c('norisk','prerisk','risk','postrisk')){
      for (fb in c('negative','positive')) {

        print(paste0(subject,'_',runn,'_',trial_type,'_',fb))
        cols_final <- c('subj', 'run', 'response class', 'cur_fb', 'event[2] (label)')
        temp <- df[subj==subject & run==runn & `response class`==trial_type & cur_fb==fb, ..cols_final]
        print(temp)
        
        temp <- temp[, ..cols_final]
       
        temp$`event[2] (label)` <- as.integer(temp$`event[2] (label)`)
        print(temp$`subj`)
        if (!is.null(temp$`subj`)) {
            subj_table <- rbind(subj_table,temp, fill = TRUE)
        }

      }
    }
  }
}
####################################tables##################################
subj_table_by_trial = subj_table %>% group_by(`subj`, `response class`) %>%
  summarize(count_response_class = n())

subj_table_by_trial_mt <- reshape2::dcast(subj_table_by_trial,
                               `response class`~subj,
                               value.var =  "count_response_class",
                               fill = 0)

filename = 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Events_autists_test/subj_table_by_trial_mt.csv'
write.csv(subj_table_by_trial_mt, file = filename)

subj_table_by_fb = subj_table %>% group_by(`subj`, `response class`, `cur_fb`) %>%
  summarize(count_response_class = n())

subj_table_by_fb_mt <- reshape2::dcast(subj_table_by_fb,
                                       cur_fb + `response class`~ subj,
                                          value.var =  "count_response_class",
                                          fill = 0)

filename = 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Events_autists_test/subj_table_by_fb_mt.csv'
write.csv(subj_table_by_fb_mt, file = filename)
##################################plot#######################################

p1 <- ggline(subj_table_by_trial, 'response class', 'count_response_class',
             group = "response class",
             #linetype = "cur_fb", shape = "cur_fb",
             color = "response class", palette = c("#00AFBB", "#E7B800", 'red', 'cyan'),
             facet.by =  "subj",
             #add = c("mean_se"),
             order = c("norisk","prerisk","risk", "postrisk"),
             ylab = 'Counts)', xlab = "Trial type",
             font.label = list(size = 15, color = "black"))
ggpar(p1,
      ylim = c(0, 150),
      font.ytickslab = 6,
)
ggsave(filename = paste0(path,'_test','.png'), width =  6, height = 5)
