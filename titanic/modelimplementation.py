import pandas as pd
import statsmodels.formula.api as smf
from sklearn.linear_model import LogisticRegression

#linear regression predicts ages
def linear_regression_age(df):
    results = smf.ols('Age~Pclass + Sex + SibSp + Parch + Fare + Embarked', data=df).fit()
    return dict(results.params)

#combine coefficients with data to get age
def age_predictor(predictors, coefs):
    age = coefs["Intercept"]
    if predictors[0] == "male":
        age += coefs["Sex[T.male]"]
    if predictors[1] == 'Q':
        age += coefs["Embarked[T.Q]"]
    if predictors[1] == 'S':
        age += coefs["Embarked[T.S]"]
    age += predictors[2]*coefs["Pclass"]
    age += predictors[3]*coefs["SibSp"]
    age += predictors[4]*coefs["Parch"]
    age += predictors[5]*coefs["Fare"]
    if age <= 1:
        age = 1
    age = round(age)
    return age

#applies age_predictor missing values only
def approx_age(column, coefs):
    age = column[0]
    predictors = (column[1:])
    if pd.isnull(age):
        age = age_predictor(predictors, coefs)
    return age

#processes dataframe
def fill_missing_ages(df):
    coefs = linear_regression_age(df)
    df['Age'] = df[['Age', 'Sex', 'Embarked', 'Pclass', 'SibSp', 'Parch', 'Fare']].apply(lambda column: approx_age(column, coefs), axis=1)
    return df

def clean_train_data(titanic):
    #Drop four non-predictive columns (categorical identifying data)
    titanic_data = titanic.drop(['PassengerId','Name','Ticket','Cabin'], 1)
    #Call fill_missing_ages from input_age script to approximate 177 missing values
    titanic_data = fill_missing_ages(titanic_data)
    #drop two rows with missing "embarked" data, leaves us with 889 rows, 0 missing values
    titanic_data.dropna(inplace=True)
    #replace categorical variables with numeric dummy variables
    gender = pd.get_dummies(titanic_data['Sex'],drop_first=True)
    embark_location = pd.get_dummies(titanic_data['Embarked'],drop_first=True)
    titanic_data.drop(['Sex', 'Embarked'],axis=1,inplace=True)
    titanic_data = pd.concat([titanic_data,gender,embark_location],axis=1)
    #At this point, we note that Fare and Pclass are not independent and drop Fare
    titanic_data.drop(['Fare'],axis=1,inplace=True)
    return titanic_data


def clean_test_data(titanic):
    #Drop four non-predictive columns (categorical identifying data)
    titanic_data = titanic.drop(['PassengerId','Name','Ticket','Cabin'], 1)
    #Call fill_missing_ages from input_age script to approximate 177 missing values
    titanic_data = fill_missing_ages(titanic_data)
    #drop two rows with missing "embarked" data, leaves us with 889 rows, 0 missing values
    titanic_data.dropna(inplace=True)
    #replace categorical variables with numeric dummy variables
    gender = pd.get_dummies(titanic_data['Sex'],drop_first=True)
    embark_location = pd.get_dummies(titanic_data['Embarked'],drop_first=True)
    titanic_data.drop(['Sex', 'Embarked'],axis=1,inplace=True)
    titanic_data = pd.concat([titanic_data,gender,embark_location],axis=1)
    #At this point, we note that Fare and Pclass are not independent and drop Fare
    titanic_data.drop(['Fare'],axis=1,inplace=True)
    #add a column of zeros to the beginning to be filled in later
    survived = list([0 for x in range(len(titanic_data.index))])
    titanic_data.insert(0, 'Survived', survived)
    return titanic_data

def make_logistic_regression(titanic):
    #Use seaborn to visualize data
    #sb.set(style="darkgrid")
    #sb.factorplot(x="Survived", hue="Sex", col="Pclass", data=titanic, kind="count", size=4, aspect=.6)

    titanic_data = clean_train_data(titanic)

    #define lists of predictor and response variables
    Predictors = titanic_data.iloc[:,1:8].values
    Response = titanic_data.iloc[:,0].values

    #Use sklearn.linear_model to perform logistic regression
    LogReg = LogisticRegression()
    LogReg.fit(Predictors, Response)
    return LogReg

def predict_survival(train, test):
    log_reg = make_logistic_regression(train)
    test_data = clean_test_data(test)
    test_predictors = test_data.iloc[:, 1:8].values
    test_response = log_reg.predict(test_predictors)
    test_data["Survived"] = test_response
    return test_data

if __name__ == "__main__":
    #global scope
    titanic_train = pd.read_csv("../data/train.csv")
    titanic_test = pd.read_csv("../data/test.csv")
    print(predict_survival(titanic_train, titanic_test))
