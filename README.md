# SecretsinSourceCode


https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9027350


Private and public git repositories often contain
unintentional sensitive information in the source code. Many tools
have been developed to scan repositories looking for potential
secrets and credentials committed in the code base, inadvertently
or intentionally, for taking corrective action once these secrets
and credentials are found. However, most of these existing works
either target a specific type of secret or generate a large number
of false positives. Our research aims to create a generalized
framework to detect all kinds of secrets – which includes API
keys, asymmetric private keys, client secrets, generic passwords
– using an extensive regular expression list. We then apply
machine learning models to intelligently distinguish between a
real secret from a false positive. The combination of regular
expression based approach and machine learning allows for the
identification of different types of secrets, specifically generic
passwords which are ignored by existing works, and subsequent
reduction of possible false positives. We also evaluate our machine
learning model using a precision-recall curve that can be used
by an operator to find the optimal trade-off between the number
of false positives and false negatives depending on their specific
application. Using a Voting Classifier (combination of Logistic
Regression, Na¨ıve Bayes and SVM) we are able to reduce the
number of false positives considerably.



Keywords—Automated software tool, hard-coded secrets,
source code, security
