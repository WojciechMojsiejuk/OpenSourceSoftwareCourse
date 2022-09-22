def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if not line.startswith('#'):  # We don't read lines which are starting with a comment sign
                line = line.split(', ')
                f_list = [float(x) for x in line]
                data.append(f_list)
    return data


def add_weighted_average(data, weight):
    for row in data:
        midterm = row[0]
        final = row[1]
        total = weight[0]*midterm + weight[1]*final
        row.append(total)


def analyze_data(data):
    data_length = len(data)
    mean = sum(data)/data_length
    var = sum([(x - mean)**2 for x in data])/data_length
    sorted_data = sorted(data)
    median = (sorted_data[data_length//2] + sorted_data[data_length//2 + 1]) / 2 if data_length % 2 == 0 else sorted_data[data_length//2]
    return mean, var, median, min(data), max(data)


if __name__ == '__main__':
    data = read_data('data/class_score_en.csv')
    if data and len(data[0]) == 2: # Check 'data' is valid
        add_weighted_average(data, [40/125, 60/100])
        if len(data[0]) == 3:      # Check 'data' is valid
            print('### Individual Score')
            print()
            print('| Midterm | Final | Total |')
            print('| ------- | ----- | ----- |')
            for row in data:
                print(f'| {row[0]} | {row[1]} | {row[2]:.3f} |')
            print()

            print('### Examination Analysis')
            col_n = len(data[0])
            col_name = ['Midterm', 'Final', 'Total']
            colwise_data = [ [row[c] for row in data] for c in range(col_n) ]
            for c, score in enumerate(colwise_data):
                mean, var, median, min_, max_ = analyze_data(score)
                print(f'* {col_name[c]}')
                print(f'  * Mean: **{mean:.3f}**')
                print(f'  * Variance: {var:.3f}')
                print(f'  * Median: **{median:.3f}**')
                print(f'  * Min/Max: ({min_:.3f}, {max_:.3f})')