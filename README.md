# Samples of data visualization code
I included only the code for the visualizations themselves, and didn't include any scripts for data processing. I also didn't include any input files, so I included what the output plots look like for real data sets here. I included first code I've written for my job as research assistant, and then code I've written for classes.

## Data visualization as research assistant

### Output of sps_plots.py
Density plots of scores for different classes
![image](https://github.com/ldups/code-viz-sample/assets/38325402/eb7e1222-f910-4277-a256-c30775572643)

### Output of var_res_density.py
Density plots comparing scores for different training approaches filtered by resistance
![image](https://github.com/ldups/code-viz-sample/assets/38325402/f61204bd-5210-4041-95b9-97d650b97b7e)

### Output of var_res_violin.py
Violin plots comparing scores for different classes
![image](https://github.com/ldups/code-viz-sample/assets/38325402/2ecfcf07-d96c-43dd-8dee-b6ba81dbab7e)

### Output of enrichment_test.py
Bar plot comparing results of enrichment tests
![image](https://github.com/ldups/code-viz-sample/assets/38325402/7ced9717-a63c-43bd-840c-ccb3becc9653)

## Data visualization for classes

### Output of integration.py
Script to compare accuracy of different integration techniques
![image](https://github.com/ldups/code-viz-sample/assets/38325402/81fda979-7d2b-4562-b989-7efdadb80b6f)

### Code written for machine learning course
This code was written in a jupyter notebook, so I included samples inline.

Investigating correlation between variables in data set during data preprocessing:

```sns.pairplot(data=df)```

![image](https://github.com/ldups/code-viz-sample/assets/38325402/8da1b292-d112-4a0a-800b-c5615499c9b2)

Results of fitting linear regression model:
```from sklearn.preprocessing import StandardScaler, MinMaxScaler
numerical_features = df[["Income","HouseAge","NumberOfRooms","AreaNumberOfBedrooms", "Population", "Price"]]
numerical_features.head()
scaler = StandardScaler()
normalized_df = scaler.fit_transform(numerical_features)
normalized_df = pd.DataFrame(normalized_df, index = df.index, columns = ["Income","HouseAge","NumberOfRooms","AreaNumberOfBedrooms", "Population", "Price"] )
normalized_df.head()
Xarray = normalized_df['Income'].values
Yarray = normalized_df['Price'].values
X = Xarray.reshape(-1, 1)
Y = Yarray.reshape(-1, 1)
model = LinearRegression()
model.fit(X, Y)
Y_pred = model.predict(X)
plt.scatter(X, Y,  color='gray')
plt.plot(X, Y_pred, color='red', linewidth=2, label='Best Fit Line')
plt.xlabel('Income')
plt.ylabel('House Price')
plt.legend()
plt.show()
```

![image](https://github.com/ldups/code-viz-sample/assets/38325402/e93c2bf2-967c-4a14-b591-9b0c25272197)

Investigation correlation between categorical variables:

```sns.countplot(x='had_affair',hue='occupation_husb',data=df,palette='rainbow')```

![image](https://github.com/ldups/code-viz-sample/assets/38325402/80364064-497c-4ee9-b5a0-3b67f4e2cbe9)
