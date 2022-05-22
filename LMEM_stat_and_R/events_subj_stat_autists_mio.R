library(data.table)
library(dplyr)
library("ggpubr")

#make a xlsx table with counts of trial types and fb

path <- 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Events_mio_list_compare/' #out_path
subj_mio_table <- data.table()

subjects = c('P301', 'P304', 'P307', 'P308', 'P311', 'P312', 'P313', 'P314', 'P316', 'P318', 'P320', 'P321', 'P322',
            'P323', 'P324', 'P325', 'P326', 'P327', 'P328', 'P329', 'P330', 'P331', 'P332', 'P333', 'P334', 'P335',
            'P336', 'P338', 'P341')

for (subject in subjects){
#consider an examples
#for (subject in 'P301'){
  for (runn in c('run1','run2','run3','run4','run5','run6')){
    for (trial_type in c('norisk','prerisk','risk','postrisk')){
      for (fb in c('negative','positive')) {

        filename <- print(paste0(path,subject,'_',runn,'_',trial_type,'_fb_',fb,'.txt'))
        
        if (file.exists(filename)){
            print("Exists!")
            temp <- read.table(filename,              # TXT data file indicated as string or full path to the file
                           header = FALSE,    # Whether to display the header (TRUE) or not (FALSE)
                           sep = "")
            print(temp)
            le <-length(temp[,1])
            #add all lines/entries of trial types
            if (le > 0){
                print(le)
                for (i in 1:le){
                    tab <- table(subject, runn, trial_type, fb)
                    print(tab)
                    subj_mio_table <- rbind(subj_mio_table,tab, fill = TRUE)
        }
        }
        }

      }
    }
  }
}

####################################tables##################################
subj_mio_table_by_trial = subj_mio_table %>% group_by(`subject`, `trial_type`) %>%
  summarize(count_trial_type = n())

subj_mio_table_by_trial_mt <- reshape2::dcast(subj_mio_table_by_trial,
                                          `trial_type`~subject,
                                          value.var =  "count_trial_type",
                                          fill = 0)

filename = 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Events_mio_list_compare/list_subj_mio_table_by_trial_mt_after_mio_clean.csv'
write.csv(subj_mio_table_by_trial_mt, file = filename)

subj_table_by_fb = subj_mio_table %>% group_by(`subject`, `trial_type`, `fb`) %>%
  summarize(count_trial_type = n())

subj_table_by_fb_mt <- reshape2::dcast(subj_table_by_fb,
                                       fb + `trial_type`~ subject,
                                       value.var =  "count_trial_type",
                                       fill = 0)

filename = 'C:/Users/trosh/OneDrive/jobs_Miasnikova/MEG/mixed_models/Events_mio_list_compare/list_subj_table_by_fb_mt_after_mio_clean.csv'
write.csv(subj_table_by_fb_mt, file = filename)