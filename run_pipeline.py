import subprocess

print("Step 1: Cleaning and importing data...")
subprocess.run(["python", "main.py"], check=True)

print("Step 2: Training churn prediction model...")
subprocess.run(["python", "train_model.py"], check=True)

print("Step 3: Generating AI retention recommendations...")
subprocess.run(["python", "generate_recommendations.py"], check=True)

print("Pipeline complete.")