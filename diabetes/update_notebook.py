import json

with open("ML.ipynb", "r") as f:
    nb = json.load(f)

# Cell 39: Logistic Regression 6 features
nb["cells"][39]["source"].extend([
    "\n",
    "import pickle\n",
    "with open('logistic_regression.sav', 'wb') as f:\n",
    "    pickle.dump(log_regress_6, f)\n"
])

# Cell 41: KNN 6 features
nb["cells"][41]["source"].extend([
    "\n",
    "import pickle\n",
    "with open('knn.sav', 'wb') as f:\n",
    "    pickle.dump(knn_6, f)\n"
])

# Cell 43: Linear SVM 6 features
nb["cells"][43]["source"].extend([
    "\n",
    "import pickle\n",
    "with open('linear_svm.sav', 'wb') as f:\n",
    "    pickle.dump(linear_svm_6, f)\n"
])

# Cell 45: RBF SVM 6 features
nb["cells"][45]["source"].extend([
    "\n",
    "import pickle\n",
    "with open('rbf_svm.sav', 'wb') as f:\n",
    "    pickle.dump(rbf_svm_6, f)\n"
])

with open("ML.ipynb", "w") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
    f.write("\n")
