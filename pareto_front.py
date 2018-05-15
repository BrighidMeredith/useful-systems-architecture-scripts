# Calculate Pareto Front

import csv
from itertools import islice


def lifetime_muat(time_to_first_replacement, avg_lifetime, replacement_costs):
    return (time_to_first_replacement/10 + 1) * (avg_lifetime/30 + 1) * (replacement_costs/200 + 1)

def area_muat(covered_area, missile_area):
    return (covered_area / 16000000 + 1) * (missile_area / 10000 + 1)

def success_muat(prob1, prob2):
    return (prob1 + 1) * (prob2 +1)

def clean_metrics_file():
    with open('sample_archs_metrics.csv', 'r', newline='') as csvfile:
        with open('cleaned_sample_archs_metrics.csv','w', newline='') as newcsvfile:
            writer = csv.writer(newcsvfile)
            csv_reader = islice(csv.reader(csvfile), 1, None)
            for row in csv_reader:
                if row[1] == '' or row[2] == '' or row[3] == '':
                    # Invalid
                    pass
                elif float(row[14]) < .01:
                    pass
                elif float(row[7]) < .01:
                    pass
                else:
                    writer.writerow(row)

clean_metrics_file()

with open('cleaned_sample_archs_metrics.csv', 'r', newline='') as csvfile:
    csv_reader = islice(csv.reader(csvfile), 1, None)
    # Step 1: Identify maximum values for each metric
    print('step 1')
    area_monitored = 0
    lifetime_to_first_replacement = 0
    avg_lifetime = 0
    replacement_costs = 1000000
    missile_range = 0
    missile_interception = 0
    system_cost = 100000000
    probability_of_success = 0
    best_lifetime_value = 0
    best_area_value = 0
    best_prob = 0
    for row in csv_reader:
        #payload	platform	launch	monitors	sensor	spacecraft-orbits	hq	area_monitored
        # lifetime_to_first_replacement	avg_lifetime	replacement_costs	missile_range	missile_interception	system_cost	probability_of_success
        #print(row)
        am = area_muat(float(row[7]), float(row[11]))
        if am > best_area_value:
            best_area_value = am
        if float(row[7]) > area_monitored:
            area_monitored = float(row[7])
            #print(area_monitored)
        if float(row[8]) > lifetime_to_first_replacement:
            lifetime_to_first_replacement = float(row[8])
            #print(lifetime_to_first_replacement)
        if float(row[9]) > avg_lifetime:
            avg_lifetime = float(row[9])
            #print(avg_lifetime)
        if float(row[10]) < replacement_costs:
            replacement_costs = float(row[10])
            #print(replacement_costs)
        if float(row[11]) > missile_range:
            missile_range = float(row[11])
            #print(missile_range)
        if float(row[12]) > missile_interception:
            missile_interception = float(row[12])
            #print(missile_interception)
        if float(row[13]) < system_cost:
            system_cost = float(row[13])
            #print(system_cost)
        if probability_of_success < float(row[14]):
            probability_of_success = float(row[14])
        lm = lifetime_muat(float(row[8]), float(row[9]), float(row[10]))
        if lm > best_lifetime_value:
            best_lifetime_value = lm
        pm = success_muat(float(row[14]), float(row[12]))
        if pm > best_prob:
            best_prob = pm

            #print(probability_of_success)
    #print(area_monitored)
    #combine lifetime like metrics into single value for pareto analysis

    # Step 2: Identify architectures that are within 5% of at least 1 maximum
    print('step 2')
with open('cleaned_sample_archs_metrics.csv', 'r', newline='') as csvfile:
    csv_reader = islice(csv.reader(csvfile), 1, None)
    pareto_pool = []
    for row in csv_reader:
        if area_muat(float(row[7]), float(row[11])) >= best_area_value:
            pareto_pool.append(row)
        elif lifetime_muat(float(row[8]), float(row[9]), float(row[10])) >= best_lifetime_value*(1):
            pareto_pool.append(row)
        elif success_muat(float(row[14]), float(row[12])) > best_prob:
            pareto_pool.append(row)
        elif float(row[13]) <= system_cost*(1):
            pareto_pool.append(row)

if 1 == 1:
    print('step 3')
    print(len(pareto_pool))
    with open('pareto_front_metrics.csv', 'w', newline='') as csv_out:
        writer = csv.writer(csv_out)
        writer.writerow(
                    ['payload', 'platform', 'launch', 'monitors', 'sensor', 'spacecraft-orbits', 'hq', 'area_monitored',
                     'lifetime_to_first_replacement', 'avg_lifetime', 'replacement_costs', 'missile_range',
                     'missile_interception', 'system_cost', 'probability_of_success'])
        # Step 3: Filter out less dominant options
        # If there is an architecture better than arch_i in all metrics, remove arch_i
        for i, row in enumerate(pareto_pool):
            remove_i = 0
            for j, row_j in enumerate(pareto_pool):
                if j != i:
                    area_value = area_muat(float(row_j[7]), float(row_j[11]))
                    lifetime_value = lifetime_muat(float(row_j[8]), float(row_j[9]), float(row_j[10]))
                    prob = success_muat(float(row_j[14]), float(row_j[12]))
                    cost = float(row_j[13])
                    if area_muat(float(row[7]), float(row[11])) >= area_value:
                        remove_i += 1
                    if lifetime_muat(float(row[8]), float(row[9]), float(row[10])) >= lifetime_value:
                        remove_i += 1
                    if success_muat(float(row[14]), float(row[12])) >= prob:
                        remove_i += 1
                    if float(row[13]) <= cost:
                        remove_i += 1
                if remove_i >= 2:
                    break
                else:
                    remove_i = 0
            if remove_i >= 2:  # Then this value succeeds for 2 metrics and is indominatable
                writer.writerow(row)


