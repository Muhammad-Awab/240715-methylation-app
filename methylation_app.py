import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import streamlit as st

# Funktion zur Altersschätzung
def estimate_age(X_train, y_train, X_val, y_val, methylation_level):
    model = LinearRegression()
    model.fit(X_train, y_train)

    predicted_age = model.predict(np.array([[methylation_level]]))

    # Validierung des Modells
    y_pred = model.predict(X_val)
    mae = mean_absolute_error(y_val, y_pred)
    mse = mean_squared_error(y_val, y_pred)
    r2 = r2_score(y_val, y_pred)

    st.write(f"Validierungsmetriken für Modell: MAE={mae:.2f}, MSE={mse:.2f}, R^2={r2:.2f}")

    return predicted_age[0], mae, mse, r2

# Funktion zum Plotten der Daten
def plot_data(df, title):
    plt.figure()
    plt.scatter(df['B'], df['A'], c='blue')
    plt.xlabel('Methylierungsgrad')
    plt.ylabel('Alter')
    plt.title(title)
    st.pyplot(plt)

# Streamlit App
st.title('Altersschätzung basierend auf Methylierungswerten')

uploaded_file1 = st.file_uploader("Bitte wählen Sie die Datei für Protein 1 (ELOVL2) aus.", type=["xlsx"])
uploaded_file2 = st.file_uploader("Bitte wählen Sie die Datei für Protein 2 (FHL2) aus.", type=["xlsx"])
uploaded_file3 = st.file_uploader("Bitte wählen Sie die Datei für Protein 3 (PENK) aus.", type=["xlsx"])

if uploaded_file1 and uploaded_file2 and uploaded_file3:
    df1 = pd.read_excel(uploaded_file1, usecols="A:B", names=['A', 'B'])
    df2 = pd.read_excel(uploaded_file2, usecols="A:B", names=['A', 'B'])
    df3 = pd.read_excel(uploaded_file3, usecols="A:B", names=['A', 'B'])

    # Daten plotten
    plot_data(df1, 'Protein 1 (ELOVL2)')
    plot_data(df2, 'Protein 2 (FHL2)')
    plot_data(df3, 'Protein 3 (PENK)')

    # Aufteilen der Daten in Trainings- und Validierungsdaten
    X_train1, X_val1, y_train1, y_val1 = train_test_split(df1[['B']], df1['A'], test_size=0.2, random_state=42)
    X_train2, X_val2, y_train2, y_val2 = train_test_split(df2[['B']], df2['A'], test_size=0.2, random_state=42)
    X_train3, X_val3, y_train3, y_val3 = train_test_split(df3[['B']], df3['A'], test_size=0.2, random_state=42)

    # Methylierungswerte eingeben
    methylation_levels = {}
    methylation_levels['ELOVL2'] = st.number_input("Bitte geben Sie den Methylierungswert für ELOVL2 ein: ", min_value=0.0, format="%.2f")
    methylation_levels['FHL2'] = st.number_input("Bitte geben Sie den Methylierungswert für FHL2 ein: ", min_value=0.0, format="%.2f")
    methylation_levels['PENK'] = st.number_input("Bitte geben Sie den Methylierungswert für PENK ein: ", min_value=0.0, format="%.2f")

    if st.button("Alter schätzen"):
        # Alter schätzen und Validierung des Modells
        age_elovl2, mae_elovl2, mse_elovl2, r2_elovl2 = estimate_age(X_train1, y_train1, X_val1, y_val1, methylation_levels['ELOVL2'])
        age_fhl2, mae_fhl2, mse_fhl2, r2_fhl2 = estimate_age(X_train2, y_train2, X_val2, y_val2, methylation_levels['FHL2'])
        age_penk, mae_penk, mse_penk, r2_penk = estimate_age(X_train3, y_train3, X_val3, y_val3, methylation_levels['PENK'])

        # Durchschnittliches Alter
        estimated_age = np.mean([age_elovl2, age_fhl2, age_penk])

        st.write(f"   ")
        st.write(f"\nELOVL2 geschätztes Alter: {age_elovl2:.2f} Jahre")
        st.write(f"FHL2 geschätztes Alter: {age_fhl2:.2f} Jahre")
        st.write(f"PENK geschätztes Alter: {age_penk:.2f} Jahre")
        st.write(f"Durchschnittlich geschätztes Alter: {estimated_age:.2f} Jahre")
