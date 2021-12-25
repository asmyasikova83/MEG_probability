TF plots
1. не забываем в functions.py 
прописать, на каком канале делаем tfr

2. получаем эпохированные данные для каждой из рассматриваемых частот
make_h5_for_TF_plots_veog.py

3. Создаем донора для комбайнов 1 и 2
make_donor_veog.py 

4. Усредняем отдельно отрицательный и положительный фидбеки

ave_into_subj_separ_fb_h5_veog.py

5. Построениe TF plots
plot_tfr_veog.py
