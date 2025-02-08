import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler , LabelEncoder
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Load and preprocess the dataset
file_path = r"Superstore.csv"
df = pd.read_csv(file_path, encoding='Windows-1252')
df = df.ffill().bfill()  # Fill missing values

# Separate numerical columns
numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns

# Encode non-numerical columns
non_numerical_columns = df.select_dtypes(exclude=['int64', 'float64']).columns
for column in non_numerical_columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])

# Scale numerical data
data = df[numerical_columns].values
scaler = StandardScaler()
data = scaler.fit_transform(data)


# Fitness function
def fitness_function(centroids, data):
    distances = np.linalg.norm(data[:, None] - centroids, axis=2)
    labels = np.argmin(distances, axis=1)
    fitness = -np.sum(np.min(distances, axis=1))  # Negative sum of minimum distances
    return fitness, labels

# Population initialization
def initialize_population(n_clusters, n_features, population_size):
    data_min, data_max = data.min(axis=0), data.max(axis=0)
    return np.random.uniform(data_min, data_max, size=(population_size, n_clusters, n_features))

# Crossover
def crossover(parent1, parent2):
    point = np.random.randint(1, parent1.shape[0])
    child1 = np.vstack((parent1[:point], parent2[point:]))
    child2 = np.vstack((parent2[:point], parent1[point:]))
    return child1, child2

# Mutation
def mutation(child, data_min, data_max, mutation_rate=0.1):
    if np.random.rand() < mutation_rate:
        i = np.random.randint(child.shape[0])
        j = np.random.randint(child.shape[1])
        child[i, j] += np.random.normal()
        child[i, j] = np.clip(child[i, j], data_min[j], data_max[j])  # Ensure bounds
    return child

# Genetic algorithm
def genetic_algorithm(data, n_clusters, n_generations=50, population_size=10, mutation_rate=0.1):
    n_features = data.shape[1]
    population = initialize_population(n_clusters, n_features, population_size)
    best_solution = None
    best_fitness = -np.inf
    data_min, data_max = data.min(axis=0), data.max(axis=0)

    for generation in range(n_generations):
        fitness_scores = []
        for individual in population:
            fitness, labels = fitness_function(individual, data)
            fitness_scores.append((fitness, individual, labels))
            if fitness > best_fitness:
                best_fitness = fitness
                best_solution = (individual, labels)
        
        fitness_scores.sort(reverse=True, key=lambda x: x[0])
        next_population = []

        for i in range(0, population_size, 2):
            parent1, parent2 = fitness_scores[i][1], fitness_scores[i+1][1]
            child1, child2 = crossover(parent1, parent2)
            next_population.append(mutation(child1, data_min, data_max, mutation_rate))
            next_population.append(mutation(child2, data_min, data_max, mutation_rate))
        
        population = np.array(next_population)
    
    return best_solution

# Run the genetic algorithm
n_clusters = 3
centroids, labels = genetic_algorithm(data, n_clusters)

# Compare with K-Means
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans_labels = kmeans.fit_predict(data)

# Evaluate clustering performance
ga_silhouette = silhouette_score(data, labels)
kmeans_silhouette = silhouette_score(data, kmeans_labels)
print(f"Silhouette Score (GA): {ga_silhouette}")
print(f"Silhouette Score (K-Means): {kmeans_silhouette}")

# Visualize clustering results
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.scatter(data[:, 0], data[:, 1], c=labels, cmap='viridis')
plt.title("Genetic Algorithm Clustering")
plt.subplot(1, 2, 2)
plt.scatter(data[:, 0], data[:, 1], c=kmeans_labels, cmap='viridis')
plt.title("K-Means Clustering")
plt.show()
