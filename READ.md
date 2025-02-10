Here is a well-structured `README.md` file for your project:

---

# **📌 Financial Reconciliation Agent**

## **📖 Problem Statement**
ZenStatement’s platform ingests financial data from multiple sources (such as SFTP, APIs, and manual uploads) and performs data reconciliation. The goal of this project is to develop an **intelligent agent** that can:
1. **Categorize financial discrepancies** based on predefined categories.
2. **Process and filter transaction data** to focus on specific issues such as `"Not Found-SysB"`.
3. **Automate resolution handling**, using an **LLM-based assistant** to classify cases as `Resolved` or `Unresolved`.
4. **Upload categorized data** to a specified folder or trigger automated emails for unresolved cases.
5. **Identify resolution patterns** for closed cases to reduce manual intervention.

---

## **🧑‍💻 Approach**
The project follows a structured approach:
1. **Data Preprocessing**: Clean, filter, and categorize transactions with discrepancies.
2. **File Upload Automation**: Move categorized data to the appropriate folder or send via email.
3. **Resolution Handling**:
   - Classify financial discrepancies using **Ollama's LLM**.
   - Generate **summary & next steps** for unresolved cases.
   - Detect **resolution patterns** to automate closure of similar future cases.
4. **Scalability & Deployment**:
   - Supports **Dockerized execution**.
   - Can be deployed **serverless on AWS Lambda / Azure Functions**.

---

## **🛠 Environment Setup**
### **🔹 1. Prerequisites**
Ensure the following are installed:
- Python **3.9+**
- Docker (if running in a container)
- AWS CLI (if deploying on AWS Lambda)
- Azure CLI (if deploying on Azure)

---

### **🔹 2. Installation**
#### **A. Local Setup**
1️⃣ **Clone the Repository**
```sh
git clone https://github.com/yourusername/financial-reconciliation-agent.git
cd financial-reconciliation-agent
```

2️⃣ **Create a Virtual Environment**
```sh
python3 -m venv env
source env/bin/activate  # MacOS/Linux
env\Scripts\activate     # Windows
```

3️⃣ **Install Dependencies**
```sh
pip install -r requirements.txt
```

---

#### **B. Docker Setup**
1️⃣ **Build the Docker Image**
```sh
docker build -t financial-agent .
```

2️⃣ **Run the Container**
```sh
docker run financial-agent --step preprocessing
docker run financial-agent --step upload
docker run financial-agent --step resolution
```

---

## **🚀 Running the Code**
### **1️⃣ Preprocessing (Filtering & Cleaning Data)**
This step extracts relevant fields from the raw transaction dataset.
```sh
python src/preprocessing.py --input data/recon_data_raw.csv --output data/recon_data_processed.csv
```

### **2️⃣ File Upload**
Once the data is processed, it can be uploaded to a specific location.
```sh
python src/file_upload.py --file data/recon_data_processed.csv
```

### **3️⃣ Resolution Handling**
This script processes resolution comments, categorizes cases, and suggests next steps.
```sh
python src/resolution_handling.py --resolution_file data/recon_data_reply.csv
```

---

## **📊 Model Choice & Preprocessing Steps**
### **📌 Model Choice**
We use **Ollama's LLM (Llama3.1:8b)** to:
- **Classify financial issues** as `"Resolved"` or `"Unresolved"`.
- **Generate summaries** for unresolved cases.
- **Suggest next steps** for unresolved issues.
- **Identify resolution patterns** to automate similar cases in the future.

### **📌 Preprocessing Steps**
1. **Filter Transactions**:
   - Extract transactions with `recon_status == "Not Found"`.
   - Ensure correct handling of missing or malformed data.
  
2. **Extract JSON Fields**:
   - Some fields (`amount`, `fee`) are stored as JSON strings.
   - We extract these values correctly while handling errors.

3. **Format Output**:
   - Save the cleaned data as a CSV for further processing.

---

## **📈 Model Evaluation**
### **🔹 How We Test the Model**
1. **Manual Testing**:
   - Check the output CSV files for correctness.
   - Run sample LLM prompts and verify responses.

3. **Performance Metrics**:
   - Measure **accuracy of classification** (Resolved/Unresolved).
   - Evaluate **pattern recognition efficiency** (how many cases are auto-closed).

---

## **☁️ Deployment Options**
### **🚀 Deploying on AWS Lambda**
1️⃣ **Create a Lambda Zip Package**
```sh
python -m pip install --target ./package -r requirements.txt
cd package
zip -r ../lambda_function.zip .
cd ..
zip -g lambda_function.zip src/*
```

2️⃣ **Deploy to AWS Lambda**
```sh
aws lambda create-function \
    --function-name FinancialAgent \
    --runtime python3.9 \
    --role arn:aws:iam::123456789012:role/lambda-role \
    --handler src.main.lambda_handler \
    --zip-file fileb://lambda_function.zip
```

---

### **🚀 Deploying on Azure Functions**
1️⃣ **Login to Azure**
```sh
az login
```

2️⃣ **Create Function App**
```sh
az functionapp create --resource-group myResourceGroup --consumption-plan-location westus --runtime python --runtime-version 3.9 --name financial-reconciliation-agent
```

3️⃣ **Deploy Code**
```sh
func azure functionapp publish financial-reconciliation-agent
```

---

## **📌 Conclusion**
This project **automates financial reconciliation** by leveraging:
- **LLMs for intelligent classification**.
- **Automation for file handling & uploads**.
- **Scalability with Docker & Serverless deployment**.

---

## **📜 License**
This project is licensed under the [MIT License](LICENSE).

---

## **🤝 Contributing**
Feel free to fork this repository and submit PRs for improvements. 🚀

---

## **🙌 Acknowledgements**
Special thanks to **ZenStatement** for providing the challenge and inspiration for this project.

---
