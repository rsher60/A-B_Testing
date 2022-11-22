1) the total error is the summation of the error due to the bias and the variance if you consider 
model complexity and the error on x and y axis respectively. The bias comes from underfitting and the 
variance comes from overfitting.
2) hyperparamters in Xgboost :
   1) number of training rounds:
   2) ETA : learning rate , more the learning rate , the more chances of the model being biased
   3) min child weight : relates to the sum of weights into each observation.Low values can mean that 
   there arent many observations in the round
   4) Max depth :how big should a tree be? bigger trees go into more details.(lower the learning rate --> bigger
   the tree whereas higher the learning rate --> smaller the tree)
   5) Gamma : how fast the tree should be split?
   6) Subsample : Share of the observations in each tree?
   7) Col sample by tree : How much of the tree should be analyzed per round?
   8) n_estimators : a small amount of estimators goes well with a higher learning rate