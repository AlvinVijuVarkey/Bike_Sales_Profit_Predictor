import joblib

# load your existing model
model = joblib.load("bike_sales_model.pkl")

# save compressed version
joblib.dump(model, "bike_sales_model_compressed.pkl", compress=3)

print("Model compressed successfully!")
