
# Data Collection
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# %matplotlib inline

!gdown --id "1wGD2leYR24xpxYbihVfyjFSo9Ir_iFJu"

df = pd.read_csv("/content/Medicalpremium.csv")
df.head(10)

"""# Data Understanding & Removing Outlier

"""

df.shape

df.info()

df.describe()

"""# Handling Missing Value

"""

df.isnull().sum()

df.isnull().sum().sum()

"""# Handling Outliers

"""

sns.boxplot(x=df['Age'])

sns.boxplot(x=df['Height'])

sns.boxplot(x=df['Weight'])

sns.boxplot(x=df['NumberOfMajorSurgeries'])

Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR=Q3-Q1
insurance=df[~((df<(Q1-1.5*IQR))|(df>(Q3+1.5*IQR))).any(axis=1)]

# Cek ukuran dataset setelah kita drop outliers
insurance.shape

"""# Univariate Analysis

"""

cat_features = ['Diabetes', 'BloodPressureProblems', 'AnyTransplants', 'AnyChronicDiseases', 'KnownAllergies', 'HistoryOfCancerInFamily']
num_features = ['Age', 'Height', 'Weight', 'NumberOfMajorSurgeries', 'PremiumPrice']

"""**Categorical Features**"""

plt.subplots(2, 2, figsize=(20, 16))

for i, col in enumerate(cat_features):
  plt.subplot(2, 3, i + 1)
  df.groupby(col).size().plot(kind='bar', rot=0)

feature = cat_features[0]
count = df[feature].value_counts()
percent = 100*df[feature].value_counts(normalize=True)
df0 = pd.DataFrame({'jumlah sampel':count, 'persentase':percent.round(1)})
print(df0)
count.plot(kind='bar', title=feature);

feature = cat_features[1]
count = df[feature].value_counts()
percent = 100*df[feature].value_counts(normalize=True)
df1 = pd.DataFrame({'jumlah sampel':count, 'persentase':percent.round(1)})
print(df1)
count.plot(kind='bar', title=feature);

feature = cat_features[2]
count = df[feature].value_counts()
percent = 100*df[feature].value_counts(normalize=True)
df2 = pd.DataFrame({'jumlah sampel':count, 'persentase':percent.round(1)})
print(df2)
count.plot(kind='bar', title=feature);

feature = cat_features[3]
count = df[feature].value_counts()
percent = 100*df[feature].value_counts(normalize=True)
df3 = pd.DataFrame({'jumlah sampel':count, 'persentase':percent.round(1)})
print(df3)
count.plot(kind='bar', title=feature);

feature = cat_features[4]
count = df[feature].value_counts()
percent = 100*df[feature].value_counts(normalize=True)
df4 = pd.DataFrame({'jumlah sampel':count, 'persentase':percent.round(1)})
print(df4)
count.plot(kind='bar', title=feature);

feature = cat_features[5]
count = df[feature].value_counts()
percent = 100*df[feature].value_counts(normalize=True)
df5 = pd.DataFrame({'jumlah sampel':count, 'persentase':percent.round(1)})
print(df5)
count.plot(kind='bar', title=feature);

"""**Numerical Features**"""

df.hist(bins=50, figsize=(20,15))
plt.show()

"""# Multivariate Analysis

**Categorical Features**
"""

cat_features = df.select_dtypes(include='object').columns.to_list()

for col in cat_features:
  sns.catplot(x=col, y="PremiumPrice", kind="bar", dodge=False, height = 4, aspect = 3,  data=df, palette="Set3")
  plt.title("Rata-rata 'PremiumPrice' Relatif terhadap - {}".format(col))

"""**Numerical Features**"""

sns.pairplot(df, diag_kind = 'kde')

plt.figure(figsize=(10, 8))
correlation_matrix = df.corr().round(2)

# Untuk print nilai di dalam kotak, gunakan parameter anot=True
sns.heatmap(data=correlation_matrix, annot=True, cmap='PiYG' )
plt.title("Correlation Matrix untuk Fitur Numerik ", size=20)

"""# Data Preparation"""

#One Hot Encoding
data_cat =  pd.get_dummies(df[['Diabetes', 'BloodPressureProblems', 'AnyTransplants', 'AnyChronicDiseases', 'KnownAllergies', 'HistoryOfCancerInFamily']])

data_cat

# Concenate Dataframe
df = pd.concat([df,data_cat],axis=1)

df.drop(columns=['Diabetes', 'BloodPressureProblems', 'AnyTransplants', 'AnyChronicDiseases', 'KnownAllergies', 'HistoryOfCancerInFamily'],inplace=True)

# Split Dataset
from sklearn.model_selection import train_test_split

X = df.drop(['PremiumPrice'],axis =1)
y = df['PremiumPrice']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 123)

print(f'Total # of sample in whole dataset: {len(X)}')
print(f'Total # of sample in train dataset: {len(X_train)}')
print(f'Total # of sample in test dataset: {len(X_test)}')

print(f'Total # of sample in whole dataset: {len(y)}')
print(f'Total # of sample in train dataset: {len(y_train)}')
print(f'Total # of sample in test dataset: {len(y_test)}')

"""# Model Development"""

# Dataframe untuk menyimpan hasil
result = pd.DataFrame(index=['train_mse', 'test_mse','eval_train','eval_test'],
                      columns=['Huber', 'SVR'])

from sklearn.linear_model import HuberRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error

# Train Model Huber
hr = HuberRegressor()
hr.fit(X_train, y_train)

result.loc['train_mse','Huber'] = mean_squared_error(y_pred = hr.predict(X_train), y_true=y_train)

# Train Model SVR
svr = SVR()
svr.fit(X_train, y_train)

result.loc['train_mse','SVR'] = mean_squared_error(y_pred = svr.predict(X_train), y_true=y_train)

# Prediksi data testing dan simpan hasil ke dataframe
result.loc['test_mse','Huber'] = mean_squared_error(y_pred = hr.predict(X_test), y_true=y_test)
result.loc['test_mse','SVR'] = mean_squared_error(y_pred = svr.predict(X_test), y_true=y_test)

result

"""# Model Evaluation"""

result.plot(kind='bar')

from sklearn.model_selection import GridSearchCV

# Hyperparams Menggunakan Grid Search pada Huber
hr_eval = HuberRegressor()
param_grid = { #Setup Params
    'epsilon': [1.0, 1.5, 2.0],
    'alpha': [0.0001, 0.001, 0.01],
    'max_iter': [100, 200, 300]
}

grid_search_huber = GridSearchCV(hr_eval, param_grid, scoring='neg_mean_squared_error', cv=5)

# Train Model dengan hyperparam
grid_search_huber.fit(X_train, y_train)

print("Best hyperparameters:", grid_search_huber.best_params_)
print("Best Score:", grid_search_huber.best_score_)

# Data Testing
result.loc['eval_train','Huber'] = mean_squared_error(y_pred = grid_search_huber.predict(X_train), y_true=y_train)
result.loc['eval_test','Huber'] = mean_squared_error(y_pred = grid_search_huber.predict(X_test), y_true=y_test)

# Hyperparams Menggunakan Grid Search pada SVR
svr_eval = SVR()
param_grid_svr = { #Setup Params
    'kernel': ['linear', 'rbf'],
    'C': [0.1, 1, 10],
    'epsilon': [0.1, 0.2, 0.3]
}
# Train models menggunakan hyperparams
grid_search_svr = GridSearchCV(svr_eval, param_grid_svr, scoring='neg_mean_squared_error', cv=5)
grid_search_svr.fit(X_train, y_train)

print("Best hyperparameters:", grid_search_svr.best_params_)
print("Best Score:", grid_search_svr.best_score_)

# Data Testing
result.loc['eval_train','SVR'] = mean_squared_error(y_pred = grid_search_svr.predict(X_train), y_true=y_train)
result.loc['eval_test','SVR'] = mean_squared_error(y_pred = grid_search_svr.predict(X_test), y_true=y_test)

result

result.plot(kind='bar')