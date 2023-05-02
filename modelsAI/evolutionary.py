import copy
import numpy as np


class Organism():
    def __init__(self, dimensions, use_bias=True, output='softmax'):
        self.layers = []
        self.biases = []
        self.use_bias = use_bias
        self.output = self._activation(output)
        for i in range(len(dimensions) - 1):
            shape = (dimensions[i], dimensions[i + 1])
            std = np.sqrt(2 / sum(shape))
            layer = np.random.normal(0, std, shape)
            bias = np.random.normal(0, std, (1, dimensions[i + 1])) * use_bias
            self.layers.append(layer)
            self.biases.append(bias)

    def _activation(self, output):
        if output == 'softmax':
            return lambda X: np.exp(X) / np.sum(np.exp(X), axis=1).reshape(-1, 1)
        if output == 'sigmoid':
            return lambda X: (1 / (1 + np.exp(-X)))
        if output == 'linear':
            return lambda X: X

    def predict(self, X):
        if not X.ndim == 2:
            raise ValueError(f'Input has {X.ndim} dimensions, expected 2')
        if not X.shape[1] == self.layers[0].shape[0]:
            raise ValueError(f'Input has {X.shape[1]} features, expected {self.layers[0].shape[0]}')
        for index, (layer, bias) in enumerate(zip(self.layers, self.biases)):
            X = X @ layer + np.ones((X.shape[0], 1)) @ bias
            if index == len(self.layers) - 1:
                X = self.output(X)  # output activation
            else:
                X = np.clip(X, 0, np.inf)  # ReLU

        return X

    def predict_choice(self, X, deterministic=True):
        probabilities = self.predict(X)
        if deterministic:
            return np.argmax(probabilities, axis=1).reshape((-1, 1))
        if any(np.sum(probabilities, axis=1) != 1):
            raise ValueError(f'Output values must sum to 1 to use deterministic=False')
        if any(probabilities < 0):
            raise ValueError(f'Output values cannot be negative to use deterministic=False')
        choices = np.zeros(X.shape[0])
        for i in range(X.shape[0]):
            U = np.random.rand(X.shape[0])
            c = 0
            while U > probabilities[i, c]:
                U -= probabilities[i, c]
                c += 1
            else:
                choices[i] = c
        return choices.reshape((-1, 1))

    def mutate(self, stdev=0.03):
        for i in range(len(self.layers)):
            self.layers[i] += np.random.normal(0, stdev, self.layers[i].shape)
            if self.use_bias:
                self.biases[i] += np.random.normal(0, stdev, self.biases[i].shape)

    def mate(self, other, mutate=True):
        if self.use_bias != other.use_bias:
            raise ValueError('Both parents must use bias or not use bias')
        if not len(self.layers) == len(other.layers):
            raise ValueError('Both parents must have same number of layers')
        if not all(self.layers[x].shape == other.layers[x].shape for x in range(len(self.layers))):
            raise ValueError('Both parents must have same shape')

        child = copy.deepcopy(self)
        for i in range(len(child.layers)):
            pass_on = np.random.rand(1, child.layers[i].shape[1]) < 0.5
            child.layers[i] = pass_on * self.layers[i] + ~pass_on * other.layers[i]
            child.biases[i] = pass_on * self.biases[i] + ~pass_on * other.biases[i]
        if mutate:
            child.mutate()
        return child


class Ecosystem():
    def __init__(self, original_f, scoring_function, population_size=100, holdout='sqrt', mating=True):
        """
        original_f must be a function to produce Organisms, used for the original population
        scoring_function must be a function which accepts an Organism as input and returns a float
        """
        self.population_size = population_size = 100
        self.population = [original_f() for _ in range(population_size)]
        self.scoring_function = scoring_function
        if holdout == 'sqrt':
            self.holdout = max(1, int(np.sqrt(population_size)))
        elif holdout == 'log':
            self.holdout = max(1, int(np.log(population_size)))
        elif holdout > 0 and holdout < 1:
            self.holdout = max(1, int(holdout * population_size))
        else:
            self.holdout = max(1, int(holdout))
        self.mating = True

    def generation(self, repeats=1, keep_best=True):
        rewards = [np.mean([self.scoring_function(x) for _ in range(repeats)]) for x in self.population]
        self.population = [self.population[x] for x in np.argsort(rewards)[::-1]]
        new_population = []
        for i in range(self.population_size):
            parent_1_idx = i % self.holdout
            if self.mating:
                parent_2_idx = min(self.population_size - 1, int(np.random.exponential(self.holdout)))
            else:
                parent_2_idx = parent_1_idx
            offspring = self.population[parent_1_idx].mate(self.population[parent_2_idx])
            new_population.append(offspring)
        if keep_best:
            new_population[-1] = self.population[0]  # Ensure best organism survives
        self.population = new_population

    def get_best_organism(self, repeats=1, include_reward=False):
        rewards = [np.mean(self.scoring_function(x)) for _ in range(repeats) for x in self.population]
        if include_reward:
            best = np.argsort(rewards)[-1]
            return self.population[best], rewards[best]
        else:
            return self.population[np.argsort(rewards)[-1]]