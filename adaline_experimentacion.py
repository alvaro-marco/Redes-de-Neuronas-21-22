import preparacion_datos
import adaline

# Load the data set

bc = preparacion_datos.dataf
X = bc.data
y = bc.target

#

# Create training and test split

#

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

#

# Instantiate CustomPerceptron

#

adaline = adaline.CustomAdaline(n_iterations = 10)

#

# Fit the model

#

adaline.fit(X_train, y_train)

#

# Score the model

#

adaline.score(X_test, y_test)