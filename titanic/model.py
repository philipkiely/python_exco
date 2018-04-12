import statsmodels.formula.api as smf
import pandas

#impute ages using given predictors and coefficients
def age_predictor(predictors, parameter_dictionary):
    age = parameter_dictionary["Intercept"]
    age += predictors['pclass'] * parameter_dictionary['pclass']
    if predictors['sex'] == 'male':
        age += parameter_dictionary['sex[T.male]']
    age += predictors['sibsp'] * parameter_dictionary['sibsp']
    age += predictors['parch'] * parameter_dictionary['parch']
    age += predictors['fare'] * parameter_dictionary['fare']
    if age < 1:
        age = 1
    age = round(age)
    return age

#convert dataframe object into object that we can fill ages in
def convert_data(columns, predictors, parameter_dictionary):
    age = columns['age']
    if pandas.isnull(age):
        age = age_predictor(columns, parameter_dictionary)
    return age


#impute missing ages
def fill_missing_ages(df):
    linear_predictor = smf.ols('age~pclass + sex + sibsp + parch + fare', data=df).fit()
    parameter_dictionary = dict(linear_predictor.params)
    predictors = df[['pclass', 'sex', 'sibsp', 'parch', 'fare']]
    df['age'] = df.apply(lambda column: convert_data(column, predictors, parameter_dictionary), axis=1)
    return df

#clean data for modelling
def clean_data(df):
    df = df.drop(['ticket', 'name', 'embarked', 'cabin'], 1)
    df = fill_missing_ages(df)
    return df

#create a logistic regression object
def make_logistic_regression(df):
    pass

#use the logistic regression object to predict passenger survival
def predict_survival(train, test):
    pass

if __name__ == "__main__":
    train = pandas.read_csv("data/train.csv")
    test = pandas.read_csv("data/test.csv")
    train = clean_data(train)
    test = clean_data(test)
