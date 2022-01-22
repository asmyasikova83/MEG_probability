
library(data.table)

fpath <- 'C:/MEG/subjects_age_sex.csv'
out_path <-'C:/MEG/mixed_models/Beta_cur/'

res <- fread(fpath)  # read first sheet
res<-as.data.frame(res)
res_short <- res[40:102, ]

print(mean(res_short$AGE))
print(sd(res_short$AGE))

fem_counter <- 0
male_counter <- 0
for (i in res_short$SEX){
    if (i == 'F'){
    fem_counter <- fem_counter + 1       
    print('Fem')
  }
  if (i == 'M'){
    male_counter <- male_counter + 1       
    #print('Male')
  }
}
print(fem_counter)
fem_counter <- 0
print(male_counter)
male_counter <- 0

