import numpy as np

f_name = '/net/server/data/Archive/prob_learn/asmyasnikova83/probability/signif_sensors/sensors_decision_pre_resp_900_200_super_sign.txt'
sensors_decision = np.loadtxt(f_name, dtype = int)

f_name_fb = '/net/server/data/Archive/prob_learn/asmyasnikova83/probability/signif_sensors/sensors_late_fb_1500_1900.txt'
sensors_fb = np.loadtxt(f_name_fb, dtype = int)

sensors_intersect = []
for i in range(len(sensors_decision)):
    for j in range(len(sensors_fb)):
        if sensors_decision[i] == sensors_fb[j]:
            sensors_intersect.append(sensors_decision[i])
print(sensors_intersect)
