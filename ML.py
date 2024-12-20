from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
class ML:
    def __init__(self, df):
        self.df = df
    def Regression_Model(self):
        # Gender-based recovery rate and healthcare access
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        sns.boxplot(x='Gender', y='Recovery Rate (%)', data=self.df, ax=axes[0], palette='Set1')
        axes[0].set_title("Recovery Rate by Gender")
        axes[0].set_xlabel("Gender")
        axes[0].set_ylabel("Recovery Rate (%)")

        sns.boxplot(x='Gender', y='Healthcare Access (%)', data=self.df, ax=axes[1], palette='Set2')
        axes[1].set_title("Healthcare Access by Gender")
        axes[1].set_xlabel("Gender")
        axes[1].set_ylabel("Healthcare Access (%)")

        plt.tight_layout()
        plt.show()
        # Group data by Disease Category and Age Group
        grouped_data = self.df.groupby(['Disease Category', 'Age Group'])['Mortality Rate (%)'].mean().unstack()

        # Heatmap for visualization
        plt.figure(figsize=(14, 8))
        sns.heatmap(grouped_data, annot=True, fmt=".1f", cmap='YlGnBu', linewidths=0.5)
        plt.title("Average Mortality Rate (%) by Disease Category and Age Group")
        plt.xlabel("Age Group")
        plt.ylabel("Disease Category")
        plt.tight_layout()
        plt.show()
        yearly_trends = self.df.groupby('Year')[['Mortality Rate (%)', 'Recovery Rate (%)', 'Healthcare Access (%)']].mean()

        # Plot trends
        yearly_trends.plot(figsize=(12, 6), marker='o')
        plt.title("Yearly Trends of Key Metrics")
        plt.xlabel("Year")
        plt.ylabel("Percentage")
        plt.legend(title="Metrics")
        plt.grid()
        plt.show()

        # # Prepare time-series data
        # time_series = self.df.groupby('Year')['Average Treatment Cost (USD)'].mean()
        #
        # # Decompose the series
        # decomposition = seasonal_decompose(time_series, model='additive', period=1)
        #
        # # Plot the decomposition
        # fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 8))
        # decomposition.observed.plot(ax=ax1, title='Observed')
        # decomposition.trend.plot(ax=ax2, title='Trend')
        # decomposition.seasonal.plot(ax=ax3, title='Seasonality')
        # decomposition.resid.plot(ax=ax4, title='Residual')
        # plt.tight_layout()
        # plt.show()

        features = ['Doctors per 1000', 'Hospital Beds per 1000', 'Recovery Rate (%)',
                    'Per Capita Income (USD)', 'Healthcare Access (%)']
        target = 'Average Treatment Cost (USD)'

        X = self.df[features]
        y = self.df[target]

        # Step 3: Normalize the data
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Step 4: Split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        # Step 5: Train Random Forest Regressor
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)

        # Step 6: Get feature importance
        importances = rf_model.feature_importances_

        # Create a DataFrame to display feature importance
        importance_df = pd.DataFrame({'Feature': features, 'Importance': importances})
        importance_df = importance_df.sort_values(by='Importance', ascending=False)

        # Step 7: Plot feature importance
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Importance', y='Feature', data=importance_df, palette='viridis')
        plt.title("Feature Importance in Random Forest")
        plt.xlabel("Importance")
        plt.ylabel("Features")
        plt.show()

