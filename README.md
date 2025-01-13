# Stroke Bot: AI-Powered Stroke Risk Prediction and Explainability Tool

## Overview

Stroke Bot is an AI-driven tool designed for healthcare professionals to predict stroke risk and provide clear explanations of the results. It is a proof of concept and not a fully deployable application. The application integrates a pre-trained Artificial Neural Network (ANN) for stroke risk calculation with GPT for natural language interaction and SHAP (SHapley Additive Explanations) for interpretability. This tool could support clinicians in making informed decisions by combining predictive accuracy with transparency, but it should be considered a prototype for testing and conceptual exploration.

## Features

1. **Stroke Risk Prediction**:

   - Utilizes a trained ANN model optimized with GridSearchCV.
   - Handles structured clinical data for prediction accuracy.

2. **Explainability with SHAP**:

   - Provides feature-level insights into predictions using SHAP visualizations such as:
     - **Force plots**: Show how each feature pushes the prediction towards or away from stroke risk.
     - **Waterfall plots**: Break down cumulative feature contributions.
     - **Decision plots**: Illustrate the combined trajectory of features affecting the prediction.

3. **GPT Integration**:

   - Interprets natural language input from users.
   - Structures  data for model predictions.
   - Provides interactive responses, explanations, and SHAP visualizations.

## How to Use

### Input Example:

**Important:** In its current state, all variables used during the training of the ANN model must be provided to ensure accurate predictions. These include `gender`, `age`, `hypertension`, `heart_disease`, `ever_married`, `work_type`, `Residence_type`, `avg_glucose_level`, `bmi`, and `smoking_status`.

Provide patient data in natural language. For example:

> "Patient is 45 years old, has an average glucose level of 120 mg/dL, BMI of 25, hypertension: yes, heart disease: no..."

1. **Data Interpretation**: GPT will structure the input into a dictionary format for the ANN model.
2. **Risk Calculation**: The ANN will calculate the probability of stroke.
3. **Explainability**: Upon request, the tool will provide SHAP values and generate visualizations to explain the prediction.

### Note:

- The application is **not a substitute for medical evaluation** and should be used strictly as a decision-support tool and proof of concept for exploring AI's potential in clinical decision-making.
- It is part of a Master's thesis project for the **Universitat Oberta de Catalunya**.
- The ANN model is trained on the [Stroke Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset/data?select=healthcare-dataset-stroke-data.csv).

## Future Enhancements

- **Enhanced Transparency**: Enable explanations of the ANN architecture and training processes.
- **Advanced Interaction**: Improve GPT's ability to interpret and explain visual outputs such as SHAP graphs.
- **Expanded Modalities**: Integrate multimodal data inputs, including medical imaging.
- **Local Deployment**: Reduce reliance on external APIs by enabling offline functionality.

## License and Acknowledgments

This project is licensed under the Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0). The ANN model was trained using the Stroke Prediction Dataset from Kaggle. This work forms part of the Master's thesis in Bioinformatics and Biostatistics at the Universitat Oberta de Catalunya.

---

For any inquiries or issues, please contact [hhgalvez@uoc.edu](mailto\:hhgalvez@uoc.edu).
