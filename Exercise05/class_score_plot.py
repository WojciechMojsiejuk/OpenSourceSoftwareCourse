import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TKAgg')

def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            if not line.startswith('#'): # If 'line' is not a header
                data.append([int(word) for word in line.split(',')])
    return data

if __name__ == '__main__':
    # Load score data
    class_kr = read_data('data/class_score_kr.csv')
    class_en = read_data('data/class_score_en.csv')

    # TODO) Prepare midterm, final, and total scores
    midtm_kr = [midtm for (midtm, _) in class_kr]
    final_kr = [final for (_, final) in class_kr]
    total_kr = [40/125*midtm + 60/100*final for (midtm, final) in class_kr]

    midtm_en, final_en = zip(*class_en)

    total_en = [40/125*midtm + 60/100*final for (midtm, final) in class_en]

    # TODO) Plot midterm/final scores as points
    plt.figure(1)
    plt.plot(midtm_en, final_en, 'b+', label='English')
    plt.plot(midtm_kr, final_kr, 'r.', label='Korean')
    plt.grid()
    plt.xlim(0, 125)
    plt.xlabel('Midterm scores')
    plt.ylim(0, 100)
    plt.ylabel('Final scores')
    plt.legend()
    plt.show()

    # TODO) Plot total scores as a histogram

    plt.figure(2)
    plt.hist(total_en,
             range=(0, 100),
             bins=20,
             color="blue",
             alpha=0.5,
             label='English')  # bin width = histogram range / number of bins
    plt.hist(total_kr,
             range=(0, 100),
             bins=20,
             color="red",
             alpha=0.5,
             label='Korean')   # 5 = 100 / bins -> bins = 20
    plt.xlabel('Total scores')
    plt.ylabel('The number of students')
    plt.legend()
    plt.show()