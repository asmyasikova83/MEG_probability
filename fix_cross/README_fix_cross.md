Baseline evaluation

Давайте посмотрим на конкретные значения мощности в бейзлайне и в нашем проблемном интервале перед нажатием на кнопку (fix_cross_main.py
with functions:  make_fix_cross_signal (make baseline signal), make_fix_cross_signal_baseline (make baseline signal corrected via baseline),
make_response_signal (make signal prior to response), make_response_signal_baseline (make response signal corrected via baseline); evoked_ave_fix_cross.py
will average the signals over blocks; combined_planar_fix_cross.py will transform the signals into necessary format; create_df_table_fix_cross.py
will put the signals into a dataframe according to the following requirement:
Я предлагаю просто вытащить в таблицу числа перед фиксационным крестом и перед нажатием для ВСЕХ ситуаций
(для начала можно только риски и нериски без разбиение по фидбекам, если так будет проще).
Усреднить по интервалам, по испытуемых и по условиям, как для обычной ановы. Каждый испытуемый в отдельной строке.
На этой таблице можно сделать простую анову, и построить простую столбчатую диаграмму.
