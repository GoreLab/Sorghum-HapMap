
##------------------------------------------------Modules----------------------------------------------------##

# Import tensorflow and keras
import tensorflow as tf
from keras import backend as sess
import keras

# Processors parameters:
GPU = False
CPU = True
num_cores = 12

# Conditional if it is going to use GPus or not:
if GPU:
    num_GPU = 1
    num_CPU = 1
else:
    num_CPU = 1
    num_GPU = 0

# Set the processors configuration:
config = tf.ConfigProto(intra_op_parallelism_threads=num_cores,\
        inter_op_parallelism_threads=num_cores, allow_soft_placement=True,\
        device_count = {'CPU' : num_CPU, 'GPU' : num_GPU})
session = tf.Session(config=config)
sess.set_session(session)

# Import libraries:
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
from sklearn.metrics import mean_squared_error
from math import sqrt
from math import ceil
import matplotlib.pyplot as plt
import matplotlib
import os
import pickle
import seaborn as sns

# Import keras tools:
from keras.models import Sequential, Model, Input
from keras.layers import MaxPooling1D, Conv1D, Dropout, Flatten, Dense, BatchNormalization, Activation
from keras.optimizers import Adam


##---------------------------------------Loading the data for analysis---------------------------------------##

# Read and impute data frame:
def read_impute_df(file_name, dir_proj, dir_out):
    # Set directory:
    os.chdir(dir_proj + "data")
    # Load data:
    df = pd.read_csv(file_name, sep="\t")
    # Imputing data frame by mean:
    df = df.fillna(df.mean())
    # Return data frame:
    return(df)

# Split data into different sets:
def split_cv(df, seed):
    # Split data again into train and a subset:
    trn_df, dev_df = train_test_split(df, test_size=0.2, random_state=seed)
    # Split the subset into dev and test:
    dev_df, tst_df = train_test_split(dev_df, test_size=0.5, random_state=seed)
    # Return data frames:
    return(trn_df, dev_df, tst_df)

# To remove feature from the data frame:
def rem_feat(df, feature):
    # Copy the data frame:
    df = df.copy(deep=True)
    # Eliminate the feature from the data frame:
    if feature!='none':
      mask = df.columns.isin([feature])
      df.iloc[:,mask] = 0
    # Return the data frame:
    return(df)


##--------------------------------------------Data processing-----------------------------------------------##

# Standarlize data frame:
def process_input(raw_input):
    # Initialize the scalers:
    scaler = StandardScaler()
    # Scale features:
    scaler.fit(raw_input)
    std_input = scaler.transform(raw_input)
    # Return processed input:
    return(std_input, scaler)

# Get target and features:
def get_inputs(df, target):
    n_class = len(df[target].unique())
    y = keras.utils.to_categorical(df[target], n_class)
    x = df.iloc[:, df.columns != target].values
    return(y, x)


##-----------------------------1D deep residual convolution neural network model----------------------------##

# Function to create a residual block:
def ResBlock1D(x,filters,pool=False):
    res = x
    if pool:
        x = MaxPooling1D(pool_size=2)(x)
        res = Conv1D(filters=filters, kernel_size=1, activation= 'relu', strides=2, padding="same")(res)
    out = BatchNormalization()(x)
    out = Conv1D(filters=filters, kernel_size=3, activation= 'relu', strides=1, padding="same")(out)
    out = BatchNormalization()(out)
    out = Conv1D(filters=filters, kernel_size=3, activation= 'relu', strides=1, padding="same")(out)
    out = keras.layers.add([res,out])
    return(out)

# Create the model architecture:
def DeepEvolution1D(input_shape, n_class):
    input_ = Input(input_shape)
    net = Conv1D(filters=2, kernel_size=3, activation= 'relu', strides=1, padding="same")(input_)
    net = ResBlock1D(net,2)
    net = ResBlock1D(net,4, pool=True)
    net = ResBlock1D(net,8, pool=True)
    net = Flatten()(net)
    net = Dense(2, activation= 'relu')(net)
    net = Dense(2, activation= 'relu')(net)
    net = BatchNormalization()(net)
    net = Dense(units=n_class, activation="softmax") (net) 
    model = Model(inputs=input_,outputs=net)
    return(model)

# To train the model:
def train_DeepEvolution1D(y_train, x_train, y_dev, x_dev, epochs):
    # Define the model:
    model = DeepEvolution1D(input_shape = (x_train.shape[1], 1), n_class=y_train.shape[1])
    # Compile the model:
    model.compile(optimizer=Adam(0.001), loss='categorical_crossentropy')
    # Fit the model:
    model.fit(x=x_train,
              y=y_train,
              validation_data=[x_dev, y_dev],
              epochs=epochs,
              verbose=1)
    # Return the model:
    return(model)


##------------------------------------------------ Metrics--------------------------------------------------##

# Function to compute the root mean squared error:
def rmse(y_true, y_pred):
    return(sqrt(mean_squared_error(y_true, y_pred)))


##-------------------------Training the deep residual convolution neural network model----------------------##

# Prefix where the project is in:
dir_proj_ = "/home/jhonathan/Documents/Sorghum-HapMap/CNN/"

# Variable to predict:
target_ = 'frac' 

# Seed:
seed_ = 1234

# Number of epochs:
epochs_ = 50

# Name of the file:
file_name_ = 'NN.table'

# Read the data and impute missing values:
df_ = read_impute_df(file_name=file_name_, dir_proj=dir_proj_, dir_out=dir_proj_)

# Getting the features names, and 'none' pattern to do not eliminate features at each run:
mask = ~df_.columns.isin([target_])
feat_list = ['none'] + df_.columns[mask].tolist()

# Initialize table to receive the metrics:
columns_df = ['removed_feature', 'set', 'rep', 'rmse', 'AUC']
feat_metrics_table =  pd.DataFrame(columns=columns_df)

# Number of replicates:
n_rep = 10

for r in range(n_rep):
    for f in feat_list:
        # Remove the feature to determine its importance in the data frame:
        df_tmp = rem_feat(df = df_, feature = f)
        # Split data into train, dev and test sets:
        trn_df, dev_df, tst_df = split_cv(df_tmp, seed = (seed_ + r))
        # Get input variables:
        trn_y, trn_x = get_inputs(df = trn_df, target = target_)
        dev_y, dev_x = get_inputs(df = dev_df, target = target_)
        tst_y, tst_x = get_inputs(df = tst_df, target = target_)
        # Standarlize data frame:
        trn_std_x, scaler_trn_x = process_input(raw_input = trn_x)
        dev_std_x, scaler_dev_x = process_input(raw_input = dev_x)
        tst_std_x, scaler_tst_x = process_input(raw_input = tst_x)
        # Reshape feature matrices:
        trn_std_x = trn_std_x.reshape(trn_std_x.shape[0], trn_std_x.shape[1], 1)
        dev_std_x = dev_std_x.reshape(dev_std_x.shape[0], dev_std_x.shape[1], 1)
        tst_std_x = tst_std_x.reshape(tst_std_x.shape[0], tst_std_x.shape[1], 1)
        # Train the model:
        model = train_DeepEvolution1D(y_train = trn_y,
                                      x_train = trn_std_x,
                                      y_dev = dev_y,
                                      x_dev = dev_std_x,
                                      epochs = epochs_)
        # Get prediction:
        trn_y_hat =  model.predict(trn_std_x)
        dev_y_pred = model.predict(dev_std_x)
        tst_y_pred = model.predict(tst_std_x)
        # Compute metrics and storing information from the current run:
        trn_out = pd.DataFrame([[f, 'trn', r, rmse(trn_y, trn_y_hat), roc_auc_score(trn_y, trn_y_hat)]], columns=columns_df)
        dev_out = pd.DataFrame([[f, 'dev', r, rmse(dev_y, dev_y_pred), roc_auc_score(dev_y, dev_y_pred)]], columns=columns_df)
        tst_out = pd.DataFrame([[f, 'tst', r, rmse(tst_y, tst_y_pred), roc_auc_score(tst_y, tst_y_pred)]], columns=columns_df)
        if (trn_out.AUC[0] < 0.4999 or trn_out.AUC[0] < 0.5009)or np.isnan(trn_out.AUC[0]):
            continue
        # Store to the final output object:
        feat_metrics_table = feat_metrics_table.append(trn_out)
        feat_metrics_table = feat_metrics_table.append(dev_out)
        feat_metrics_table = feat_metrics_table.append(tst_out)
        # Print current run:
        print('Removing {} feature at the replication {}'.format(f, r))
        print(feat_metrics_table)


##--------------------------------------------------Outputs-------------------------------------------------##

# Get the summary of the model:
model.summary()

# Print the output table:
print(feat_metrics_table)
feat_metrics_table.groupby(['removed_feature'], as_index=False)['rmse'].mean()
feat_metrics_table.groupby(['removed_feature'], as_index=False)['AUC'].mean()

# Set directory:
os.chdir(dir_proj_ + "output")

# Save pickler:
with open('frac_feat_selection_out.pkl', 'wb') as f:
  pickle.dump(feat_metrics_table, f, protocol=-1)

# Save on csv format:
feat_metrics_table.to_csv('frac_feat_selection_out.csv', header=True, index=False)

# Change codification for boxplot:
feat_metrics_table['set'].replace('trn', 'Train',inplace=True)
feat_metrics_table['set'].replace('dev', 'Development',inplace=True)
feat_metrics_table['set'].replace('tst', 'Test',inplace=True)

# Change the name of the column for plot:
feat_metrics_table = feat_metrics_table.rename(columns={'set': 'Sets'})

# Plot the faeture importance for prediction:
import seaborn as sns
sns.set(rc={'figure.figsize':(7.48, 6.3)})

with sns.plotting_context(font_scale=1):
    ax = sns.boxplot(x="removed_feature", y="AUC", hue="Sets",
                     data=feat_metrics_table, palette="Set3")
    ax.set_ylabel('Predictive ability')    
    ax.set_xlabel('Removed features')
    ax.set_xticklabels(labels = feat_metrics_table.removed_feature.unique(),
                       rotation = 30)
    ax.tick_params(labelsize=6)

# Save the figure png format:
ax.figure.savefig('frac_feat_selection_out.png', dpi=350)

# Save the figure pdf format:
ax.figure.savefig('frac_feat_selection_out.pdf', dpi=350)
