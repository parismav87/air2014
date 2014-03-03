# REMBO

import numpy as np
import math

import acquisition_function as acq
import create_random_matrix as crm
import chooseBoundedRegion as cbr

D = 10 # number of features
d = 3 # reducted dimension

n_training = 10
n_test = 1
max_iter = 1000 # maximum number of iterations
sigma_0 = 0.1

regionBound = math.sqrt(d)
regionBoundStepSize = 0.1


# Sample training input and ouput
ytrain = np.matrix(np.random.uniform(-5, 5, (n_training, D)))
fytrain = acq.sample_training_output(ytrain)


# Step 1
# Generate random matrix
A = crm.random_matrix(D, d)

# Step 2
# Choose bounded region set
Y = cbr.chooseBoundedRegion(d, -regionBound, regionBound, regionBoundStepSize)

#define initial mu and sigma
mu =0
sigma = 1 
# Step 3 - 6
for t in range(0, max_iter):
  # Select points from bounded box to be tested
  ytest =Y
  #ytest = acq.select_test_set(n_test, Y)

  # Get mu and sigma
  mu, sigma = acq.gp_posterior(ytrain,sigma, ytest, fytrain, sigma_0, n_test, A)

  # Find ybest
  ybest = acq.gp_optimize(ytest, t, D, mu, sigma, n_test)

  # Augment the data
  ytrain, fytrain = acq.augment_data(ytrain, fytrain, ybest, A)

  print ybest