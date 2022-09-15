def normalize_data(n_cases, n_people, scale):
    norm_cases = []     # TODO: Calculate the number of cases per its population
    for idx, n in enumerate(n_cases):
        norm_cases.append(n / (n_people[idx]/scale))
    return norm_cases

regions  = ['Seoul', 'Gyeongi', 'Busan', 'Gyeongnam', 'Incheon', 'Gyeongbuk', 'Daegu', 'Chungnam', 'Jeonnam', 'Jeonbuk', 'Chungbuk', 'Gangwon', 'Daejeon', 'Gwangju', 'Ulsan', 'Jeju', 'Sejong']
n_people = [9550227,  13530519, 3359527,     3322373,   2938429,     2630254, 2393626,    2118183,   1838353,   1792476,    1597179,   1536270,   1454679,   1441970, 1124459, 675883,   365309] # 2021-08
n_covid  = [    644,       529,      38,          29,       148,          28,      41,         62,        23,        27,         27,        33,        16,        40,      20,      5,        4] # 2021-09-21

sum_people = 0 # TODO: The total number of people

for region_population in n_people:
    sum_people += region_population

sum_covid  = 0 # TODO: The total number of new cases

for region_covid in n_covid:
    sum_covid += region_covid
norm_covid = normalize_data(n_covid, n_people, 1000000) # The new cases per 1 million people

# Print population by region
print('### Korean Population by Region')
print('* Total population:', sum_people)
print() # Print an empty line
print('| Region | Population | Ratio (%) |')
print('| ------ | ---------- | --------- |')
for idx, pop in enumerate(n_people):
    ratio = pop*100/sum_people  # TODO: The ratio of region population to the total
    print('| %s | %d | %.1f |' % (regions[idx], pop, ratio))
print()

# TODO: Print COVID-19 new cases by region

# Print population by region
print('### Korean COVID-19 New Cases by Region')
print('* Total new cases:', sum_covid)
print() # Print an empty line
print('| Region | New Cases | Ratio (%) | New Cases / 1M |')
print('| ------ | ---------- | --------- |')

cases_by_one_million = normalize_data(n_covid, n_people, scale=10**6)

for idx, cases in enumerate(n_covid):
    ratio = cases*100/sum_covid  # TODO: The ratio of region population to the total
    print('| %s | %d | %.1f | %.1f |' % (regions[idx], cases, ratio, cases_by_one_million[idx]))
print()
