import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D # For the custom legend
from sklearn import (metrics, linear_model, naive_bayes, neural_network, neighbors, svm, tree, ensemble)
from matplotlib.colors import LinearSegmentedColormap

def load_wdbc_data(filename):
    class WDBCData:
        data = []
        target = []
        target_names = ['benign', 'malignant']
        feature_names = ['mean radius', 'mean texture', 'mean perimeter', 'mean area', 'mean smoothness', 'mean compactness', 'mean concavity', 'mean concave points', 'mean symmetry', 'mean fractal dimension',
                         'radius error', 'texture error', 'perimeter error', 'area error', 'smoothness error', 'compactness error', 'concavity error', 'concave points error', 'symmetry error', 'fractal dimension error',
                         'worst radius', 'worst texture', 'worst perimeter', 'worst area', 'worst smoothness', 'worst compactness', 'worst concavity', 'worst concave points', 'worst symmetry', 'worst fractal dimension']
    wdbc = WDBCData()
    with open(filename) as f:
        for idx, line in enumerate(f.readlines()):
            items = line.split(',')
            wdbc.target.append(1 if items[1] == 'M' else 0)
            wdbc.data.append(items[2:])
        wdbc.data = np.array(wdbc.data).astype(float)
    return wdbc

if __name__ == '__main__':
    # Load a dataset
    # wdbc = datasets.load_breast_cancer()
    wdbc = load_wdbc_data('data/wdbc.data')

    # Train a model

    models = [
        {'name': 'svm.SVC()', 'obj': svm.SVC()},
        {'name': 'linear_model.SGD', 'obj': linear_model.SGDClassifier()},
        {'name': 'naive_bayes.Gaussian', 'obj': naive_bayes.GaussianNB()},
        {'name': 'neural_network.MLP', 'obj': neural_network.MLPClassifier()},
        {'name': 'neighbors.KNN', 'obj': neighbors.KNeighborsClassifier()},

        {'name': 'svm.LinearSVC', 'obj': svm.LinearSVC()},
        {'name': 'svm.SVC(poly,2)', 'obj': svm.SVC(kernel='poly', degree=2)},
        {'name': 'svm.SVC(poly,3)', 'obj': svm.SVC(kernel='poly')},
        {'name': 'svm.SVC(poly,4)', 'obj': svm.SVC(kernel='poly', degree=4)},
        {'name': 'svm.SVC(rbf)', 'obj': svm.SVC(kernel='rbf')},
        {'name': 'svm.SVC(rbf,$\gamma$=1)', 'obj': svm.SVC(kernel='rbf', gamma=1)},
        {'name': 'svm.SVC(rbf,$\gamma$=4)', 'obj': svm.SVC(kernel='rbf', gamma=4)},
        {'name': 'svm.SVC(rbf,$\gamma$=16)', 'obj': svm.SVC(kernel='rbf', gamma=16)},
        {'name': 'svm.SVC(rbf,$\gamma$=64)', 'obj': svm.SVC(kernel='rbf', gamma=64)},

        {'name': 'tree.DecisionTree(2)', 'obj': tree.DecisionTreeClassifier(max_depth=2)},
        {'name': 'tree.DecisionTree(4)', 'obj': tree.DecisionTreeClassifier(max_depth=4)},
        {'name': 'tree.DecisionTree(N)', 'obj': tree.DecisionTreeClassifier()},
        {'name': 'tree.ExtraTree', 'obj': tree.ExtraTreeClassifier()},

        {'name': 'ensemble.RandomForest(10)', 'obj': ensemble.RandomForestClassifier(n_estimators=10)},
        {'name': 'ensemble.RandomForest(100)', 'obj': ensemble.RandomForestClassifier()},
        {'name': 'ensemble.ExtraTrees(10)', 'obj': ensemble.ExtraTreesClassifier()},
        {'name': 'ensemble.ExtraTrees(100)', 'obj': ensemble.ExtraTreesClassifier()},
        {'name': 'ensemble.AdaBoost(DTree)', 'obj': ensemble.AdaBoostClassifier(tree.DecisionTreeClassifier())},
    ]

    accuracy = []
    for model in models:
        model['obj'].fit(wdbc.data, wdbc.target)

        # Test the model
        predict = model['obj'].predict(wdbc.data)
        n_correct = sum(predict == wdbc.target)
        accuracy.append(n_correct / len(wdbc.data))

    plt.figure()
    x = np.arange(len(accuracy))
    plt.stem(x, accuracy, bottom=accuracy[0])
    plt.xticks(x, [model['name'] for model in models], rotation = 90)
    plt.xlabel('Method')
    plt.ylabel('Accuracy improvement')
    plt.title('Benchmark of accuracy of models in comparison to SVM.SVC')
    plt.tight_layout()
    plt.show()

    # Many methods achieve 1.0 in accuracy
    # By Occham razor lets choose the simples among them
    # and compare them with SVC

    models = [
        {'name': 'svm.SVC()', 'obj': svm.SVC()},
        {'name': 'svm.SVC(rbf,$\gamma$=1)', 'obj': svm.SVC(kernel='rbf', gamma=1)},
        {'name': 'tree.DecisionTree(N)', 'obj': tree.DecisionTreeClassifier()},
    ]

    for model in models:

        model['obj'].fit(wdbc.data, wdbc.target)

        # Test the model
        predict = model['obj'].predict(wdbc.data)
        n_correct = sum(predict == wdbc.target)
        accuracy = n_correct / len(wdbc.data)

        conf_mat = metrics.confusion_matrix(wdbc.target, predict)
        conf_dis = metrics.ConfusionMatrixDisplay(conf_mat, display_labels=wdbc.target_names)
        plt.figure()
        conf_dis.plot()

        # Visualize testing results
        cmap = np.array([(1, 0, 0), (0, 1, 0)])
        clabel = [Line2D([0], [0], marker='o', lw=0, label=wdbc.target_names[i], color=cmap[i]) for i in range(len(cmap))]
        for (x, y) in [(i, i+1) for i in range(0, 2, 2)]: # Not mandatory, but try [(i, i+1) for i in range(0, 30, 2)]

            x_min, x_max = wdbc.data[:, x].min() - 1, wdbc.data[:, x].max() + 1
            y_min, y_max = wdbc.data[:, y].min() - 1, wdbc.data[:, y].max() + 1
            xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100))
            xy = np.vstack((xx.flatten(), yy.flatten())).T

            model['obj'].fit(wdbc.data[:, x:y+1], wdbc.target)
            zz = model['obj'].predict(xy)

            plt.figure()
            plt.contourf(xx, yy, zz.reshape(xx.shape), alpha=0.2, cmap=LinearSegmentedColormap.from_list(name='RedGreen', colors=cmap))

            plt.title(f'Classifier {model["name"]} ({n_correct}/{len(wdbc.data)}={accuracy:.3f})')
            plt.scatter(wdbc.data[:, x], wdbc.data[:, y], c=cmap[wdbc.target], edgecolors=cmap[predict])
            plt.xlabel(wdbc.feature_names[x])
            plt.ylabel(wdbc.feature_names[y])
            plt.legend(handles=clabel, framealpha=0.5)
            plt.show()
