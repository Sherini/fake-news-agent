import os
import pandas as pd

data = []

# ✅ YOUR PATHS
fake_path = r"C:\Users\dudek\OneDrive\Projects\FakeNewsDetection\dataset\fake"
real_path = r"C:\Users\dudek\OneDrive\Projects\FakeNewsDetection\dataset\real"

# -------- FAKE NEWS --------
for filename in os.listdir(fake_path):
    file_path = os.path.join(fake_path, filename)

    if filename.endswith(".txt"):  # only read txt files
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read().strip()

                if text:
                    data.append([text, 0])  # fake = 0

        except Exception as e:
            print("Error reading:", file_path)

# -------- REAL NEWS --------
for filename in os.listdir(real_path):
    file_path = os.path.join(real_path, filename)

    if filename.endswith(".txt"):
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read().strip()

                if text:
                    data.append([text, 1])  # real = 1

        except Exception as e:
            print("Error reading:", file_path)

# -------- CREATE CSV --------
df = pd.DataFrame(data, columns=["text", "label"])

# Save CSV inside dataset folder
output_path = r"C:\Users\dudek\OneDrive\Projects\FakeNewsDetection\dataset\news.csv"
df.to_csv(output_path, index=False)

print("✅ Dataset created successfully!")
print("📊 Total samples:", len(df))