import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TKAgg')

if __name__ == '__main__':
    midterm_range = np.array([0, 125])
    final_range = np.array([0, 100])

    # Load score data
    class_kr = np.loadtxt('data/class_score_kr.csv', delimiter=',')
    class_en = np.loadtxt('data/class_score_en.csv', delimiter=',')
    data = np.vstack((class_kr, class_en))
    x = data[:, 0]  # y = wx + b
    y = data[:, 1]

    A = np.vstack((x, np.ones(x.shape))).T

    # Estimate a line, final = slope * midterm + y_intercept
    line = np.linalg.pinv(A) @ y # TODO: Please find the best [slope, y_intercept] from 'data'

    # Predict scores
    final = lambda midterm: line[0] * midterm + line[1]
    while True:
        given = input('Q) Please input your midterm score (Enter or -1: exit)? ')
        if given == '' or float(given) < 0:
            break
        print(f'A) Your final score is expected to {final(float(given)):.3f}.')

    # Plot scores and the estimated line
    plt.figure()
    plt.plot(data[:,0], data[:,1], 'r.', label='The given data')
    plt.plot(midterm_range, final(midterm_range), 'b-', label='Prediction')
    plt.xlabel('Midterm scores')
    plt.ylabel('Final scores')
    plt.xlim(midterm_range)
    plt.ylim(final_range)
    plt.grid()
    plt.legend()
    plt.show()