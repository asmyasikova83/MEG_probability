
TFR analysis of stimulus-locked data

main_stim.py -calls make_beta_signal which conducts TFR analysis of the events, both feedbacks combined (see suffix feedback further - it means separate processing for each fb, no suffix means fb combined processing)

main_stim_feedback.py calls make_beta_signal which conducts TFR analysis of the events, each feedback separately

subtraction_second_baseline_trial_type.py

subtraction_second_baselin_feedback.py - вторая корректировка на бейзлайн (полную версию двух шагового метода корректировка на БЛ можно посмотеть в probability_learning/function.py, была заменена на одношаговыю с ранним логарифмированием, т.е. оба метода дают одинаковый результат, но одношаговую проще объяснять) 

evoked_ave_between_runs_and_fb_var3.py

evoked_ave_between_runs_var3_separ_fb.py - по итогу скрипта получаем усредненные данные внутри каждого испытуемого. Усреденение происходит средствами MNE: сначала усредняем данные внутри фидбека (и внутри блока (run)), т.е. из эпох получаем evoked. Затем собираем список evoked для каждого испытуемого (должно получаеться от 0 до 12, по количеству блоков 6, каждый блок разделен на 2 фид бека - 12)

combined_planar_average_into_subjects.py
combined_planar_average_into_subjects_feedback.py - calls combine_planar_Evoked which summarizes the data from both planars

