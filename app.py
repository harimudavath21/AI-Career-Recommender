
import re
from io import BytesIO
from urllib.parse import quote_plus

import fitz
import docx
import pandas as pd
import streamlit as st

from modules.career_predictor import (
    predict_careers,
    CAREER_PROFILES
)


# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="CareerCompass AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================================
# 2. PREMIUM DASHBOARD STYLING
# ==========================================================

st.markdown("""
<style>

/* GLOBAL BACKGROUND */

.stApp {
    background:
        radial-gradient(
            circle at 10% 5%,
            rgba(48, 83, 180, 0.18),
            transparent 32%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(117, 65, 190, 0.13),
            transparent 30%
        ),
        #0B1020;

    color: #E8EDFA;
}

/* MAIN CONTENT */

.block-container {
    max-width: 1250px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* HEADER */

.main-title {
    font-size: 43px;
    font-weight: 850;
    letter-spacing: -1.5px;
    text-align: center;

    background: linear-gradient(
        90deg,
        #60A5FA,
        #A78BFA,
        #60A5FA
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-bottom: 8px;
}

.subtitle {
    text-align: center;
    color: #94A3B8;
    font-size: 15px;
    letter-spacing: 0.4px;
    margin-bottom: 30px;
}

/* SECTION HEADINGS */

.section-title {
    font-size: 23px;
    font-weight: 750;
    color: #F1F5FF;
    padding: 12px 0;
    margin-top: 18px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.16);
}

/* DIVIDERS */

hr {
    border-color: rgba(148, 163, 184, 0.16) !important;
}

/* METRIC CARDS */

div[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        rgba(30, 43, 72, 0.95),
        rgba(19, 29, 52, 0.95)
    );

    border: 1px solid rgba(129, 155, 220, 0.2);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);

    transition: all 0.25s ease;
}

div[data-testid="stMetric"]:hover {
    border-color: #638BFF;
    transform: translateY(-3px);
}

div[data-testid="stMetricLabel"] {
    color: #A9B7D4 !important;
}

div[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-weight: 750;
}

/* BUTTONS */

.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(
        100deg,
        #4169E1,
        #7655D9
    );

    color: #FFFFFF;
    border: none;
    border-radius: 11px;
    padding: 11px 20px;
    font-weight: 650;
    min-height: 44px;

    transition: all 0.25s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: linear-gradient(
        100deg,
        #5B82F0,
        #906FF0
    );

    border: none;
    color: white;
    box-shadow: 0 5px 20px rgba(89, 105, 235, 0.3);
    transform: translateY(-2px);
}

/* FILE UPLOADER */

div[data-testid="stFileUploader"] {
    background: rgba(24, 36, 62, 0.75);
    border: 1px dashed #627DBD;
    border-radius: 16px;
    padding: 15px;
}

div[data-testid="stFileUploader"] section {
    background: transparent;
}

/* INPUTS */

.stTextInput input,
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #17223B !important;
    border-color: #34466B !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
}

/* EXPANDERS */

div[data-testid="stExpander"] {
    background: rgba(24, 36, 62, 0.75);
    border: 1px solid rgba(129, 155, 220, 0.2);
    border-radius: 14px;
    margin-bottom: 12px;
    overflow: hidden;
}

div[data-testid="stExpander"] summary {
    color: #E5EDFF;
    font-weight: 650;
    padding: 12px;
}

/* DATAFRAMES */

div[data-testid="stDataFrame"] {
    border: 1px solid rgba(129, 155, 220, 0.2);
    border-radius: 12px;
    overflow: hidden;
}

/* ALERTS */

div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* PROGRESS BAR */

div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(
        90deg,
        #4169E1,
        #A78BFA
    );
    border-radius: 20px;
}

/* LINKS */

a {
    color: #93B4FF !important;
    font-weight: 600;
}

/* FOOTER */

.dashboard-footer {
    text-align: center;
    color: #8493B0;
    padding: 25px;
    border-top: 1px solid rgba(148, 163, 184, 0.16);
    margin-top: 30px;
}

/* RESPONSIVE */

@media (max-width: 768px) {
    .main-title {
        font-size: 30px;
    }

    .section-title {
        font-size: 20px;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# 3. APPLICATION HEADER - ONLY ONCE
# ==========================================================

st.markdown(
    '<div class="main-title">🎯 CareerCompass AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your AI-powered career discovery and skill development platform'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================================
# 4. SKILL ALIASES
# ==========================================================

SKILL_ALIASES = {
    "Python": ["python", "python programming"],
    "SQL": ["sql", "mysql", "postgresql", "sqlite"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning", "dl"],
    "Artificial Intelligence": ["artificial intelligence", "ai"],
    "Generative AI": ["generative ai", "gen ai", "genai"],
    "NLP": ["nlp", "natural language processing"],
    "Computer Vision": ["computer vision"],
    "Statistics": ["statistics", "statistical analysis"],
    "Mathematics": ["mathematics", "math"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Matplotlib": ["matplotlib"],
    "Seaborn": ["seaborn"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "OpenCV": ["opencv", "cv2"],
    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"],
    "Excel": ["excel", "microsoft excel"],
    "Data Visualization": ["data visualization", "data visualisation"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Data Cleaning": ["data cleaning", "data preprocessing"],
    "Data Structures": ["data structures", "dsa"],
    "OOP": ["oop", "object oriented programming"],
    "Flask": ["flask"],
    "Django": ["django"],
    "FastAPI": ["fastapi"],
    "Streamlit": ["streamlit"],
    "HTML": ["html"],
    "CSS": ["css"],
    "JavaScript": ["javascript"],
    "React": ["react", "react.js"],
    "Node.js": ["node.js", "nodejs"],
    "Git": ["git", "github"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure", "microsoft azure"],
    "GCP": ["gcp", "google cloud platform"],
    "ETL": ["etl", "extract transform load"],
    "Apache Spark": ["apache spark", "pyspark"],
    "Hadoop": ["hadoop"],
    "MongoDB": ["mongodb"],
    "Snowflake": ["snowflake"],
    "Power BI DAX": ["dax"],
    "REST API": ["rest api", "restful api"],
    "LangChain": ["langchain"],
    "LlamaIndex": ["llamaindex", "llama index"],
    "Transformers": ["transformers", "hugging face"],
    "RAG": ["rag", "retrieval augmented generation"]
}


# ==========================================================
# 5. SKILL CURRICULUM
# ==========================================================

def curriculum(duration, level, topics, project, resource):

    return {
        "duration": duration,
        "level": level,
        "topics": topics,
        "project": project,
        "resource": resource
    }


SKILL_CURRICULUM = {

    "Python": curriculum(
        "2 weeks",
        "Beginner",
        [
            "Python syntax and variables",
            "Data types and operators",
            "Conditional statements and loops",
            "Functions and lambda functions",
            "Lists, tuples, sets and dictionaries",
            "Object-oriented programming",
            "Classes, objects and inheritance",
            "Exception handling",
            "File handling"
        ],
        "Build a Student Management System",
        "https://docs.python.org/3/tutorial/"
    ),

    "SQL": curriculum(
        "2 weeks",
        "Beginner to Intermediate",
        [
            "SQL fundamentals and database concepts",
            "DDL, DML and DQL commands",
            "WHERE, ORDER BY and GROUP BY",
            "Aggregate functions",
            "INNER JOIN, LEFT JOIN and RIGHT JOIN",
            "Subqueries and Common Table Expressions",
            "Window functions",
            "Indexes and query optimization"
        ],
        "Build a Sales Database and analyze business data",
        "https://www.w3schools.com/sql/"
    ),

    "Machine Learning": curriculum(
        "3 weeks",
        "Intermediate",
        [
            "Introduction to Machine Learning",
            "Supervised and unsupervised learning",
            "Linear regression and logistic regression",
            "Decision trees and random forests",
            "K-Nearest Neighbors",
            "Support Vector Machines",
            "Clustering algorithms",
            "Feature engineering",
            "Model evaluation and cross-validation"
        ],
        "Build a Customer Churn Prediction Model",
        "https://scikit-learn.org/stable/user_guide.html"
    ),

    "Deep Learning": curriculum(
        "3 weeks",
        "Advanced",
        [
            "Neural network fundamentals",
            "Perceptrons and activation functions",
            "Forward propagation and backpropagation",
            "Loss functions and optimizers",
            "Convolutional Neural Networks",
            "Recurrent Neural Networks",
            "Model training and evaluation"
        ],
        "Build an Image Classification Model",
        "https://www.tensorflow.org/tutorials"
    ),

    "Statistics": curriculum(
        "1 week",
        "Beginner",
        [
            "Mean, median and mode",
            "Variance and standard deviation",
            "Probability fundamentals",
            "Normal distribution",
            "Hypothesis testing",
            "Correlation and covariance",
            "Confidence intervals"
        ],
        "Perform Statistical Analysis on a Sales Dataset",
        "https://www.khanacademy.org/math/statistics-probability"
    ),

    "Mathematics": curriculum(
        "1 week",
        "Beginner to Intermediate",
        [
            "Linear algebra fundamentals",
            "Vectors and matrices",
            "Matrix operations",
            "Basic calculus",
            "Derivatives and gradients",
            "Probability concepts"
        ],
        "Implement mathematical operations used in Machine Learning",
        "https://www.khanacademy.org/math"
    ),

    "Pandas": curriculum(
        "1 week",
        "Beginner",
        [
            "Series and DataFrames",
            "Reading CSV and Excel files",
            "Selecting and filtering data",
            "Handling missing values",
            "GroupBy and aggregation",
            "Merging and joining DataFrames",
            "Data transformation"
        ],
        "Perform Exploratory Data Analysis on a CSV dataset",
        "https://pandas.pydata.org/docs/getting_started/"
    ),

    "NumPy": curriculum(
        "4 days",
        "Beginner",
        [
            "NumPy arrays",
            "Array indexing and slicing",
            "Array reshaping",
            "Mathematical operations",
            "Broadcasting",
            "Statistical operations"
        ],
        "Create a numerical data analysis application",
        "https://numpy.org/learn/"
    ),

    "Matplotlib": curriculum(
        "4 days",
        "Beginner",
        [
            "Line charts",
            "Bar charts",
            "Scatter plots",
            "Histograms",
            "Labels, titles and legends",
            "Subplots and chart customization"
        ],
        "Create a Data Visualization Dashboard",
        "https://matplotlib.org/stable/tutorials/"
    ),

    "Seaborn": curriculum(
        "4 days",
        "Beginner",
        [
            "Seaborn fundamentals",
            "Statistical data visualization",
            "Distribution plots",
            "Categorical plots",
            "Correlation heatmaps",
            "Pair plots"
        ],
        "Create a Statistical Data Visualization Report",
        "https://seaborn.pydata.org/tutorial.html"
    ),

    "Scikit-learn": curriculum(
        "2 weeks",
        "Intermediate",
        [
            "Data preprocessing",
            "Train-test splitting",
            "Feature scaling",
            "Encoding categorical variables",
            "Model training",
            "Model evaluation",
            "Pipelines and cross-validation",
            "Hyperparameter tuning"
        ],
        "Build an End-to-End ML Prediction Application",
        "https://scikit-learn.org/stable/user_guide.html"
    ),

    "TensorFlow": curriculum(
        "2 weeks",
        "Advanced",
        [
            "TensorFlow fundamentals",
            "Tensors and operations",
            "Building neural networks",
            "Keras Sequential API",
            "Model training and evaluation",
            "Saving and loading models"
        ],
        "Build a Neural Network Classification Model",
        "https://www.tensorflow.org/tutorials"
    ),

    "PyTorch": curriculum(
        "2 weeks",
        "Advanced",
        [
            "Tensors and tensor operations",
            "Autograd",
            "Building neural networks",
            "Loss functions and optimizers",
            "Training loops",
            "Saving and loading models"
        ],
        "Build an Image Classification Model",
        "https://pytorch.org/tutorials/"
    ),

    "NLP": curriculum(
        "2 weeks",
        "Advanced",
        [
            "Text preprocessing",
            "Tokenization",
            "Stopword removal",
            "Stemming and lemmatization",
            "Bag of Words and TF-IDF",
            "Word embeddings",
            "Text classification",
            "Transformer fundamentals"
        ],
        "Build a Resume Text Classification System",
        "https://www.nltk.org/book/"
    ),

    "Generative AI": curriculum(
        "2 weeks",
        "Advanced",
        [
            "Introduction to Generative AI",
            "Large Language Models",
            "Prompt engineering",
            "Tokens and embeddings",
            "Transformer architecture",
            "Retrieval-Augmented Generation",
            "LLM application development",
            "AI application evaluation"
        ],
        "Build an AI-powered Question Answering Application",
        "https://huggingface.co/learn"
    ),

    "Power BI": curriculum(
        "2 weeks",
        "Intermediate",
        [
            "Power BI Desktop fundamentals",
            "Importing and transforming data",
            "Power Query Editor",
            "Data modeling and relationships",
            "DAX fundamentals",
            "Measures and calculated columns",
            "Slicers and filters",
            "Dashboard design"
        ],
        "Build an Interactive Business Analytics Dashboard",
        "https://learn.microsoft.com/en-us/power-bi/"
    ),

    "Excel": curriculum(
        "1 week",
        "Beginner to Intermediate",
        [
            "Cell references and formatting",
            "Basic and aggregate functions",
            "IF and logical functions",
            "SUMIF and SUMIFS",
            "COUNTIF and COUNTIFS",
            "Lookup functions",
            "Sorting and filtering",
            "Charts and dashboards"
        ],
        "Build an Excel Sales Performance Dashboard",
        "https://support.microsoft.com/excel"
    ),

    "Flask": curriculum(
        "1 week",
        "Intermediate",
        [
            "Flask installation and setup",
            "Routes and URL handling",
            "Templates and forms",
            "Request and response handling",
            "REST API development",
            "Database integration",
            "Application deployment"
        ],
        "Build a Student Management Web Application",
        "https://flask.palletsprojects.com/"
    ),

    "Django": curriculum(
        "2 weeks",
        "Intermediate",
        [
            "Django project structure",
            "Models and database operations",
            "Views and URL routing",
            "Templates",
            "Forms and validation",
            "Authentication",
            "Django REST Framework fundamentals"
        ],
        "Build a Job Portal Application",
        "https://docs.djangoproject.com/en/stable/intro/"
    ),

    "FastAPI": curriculum(
        "1 week",
        "Intermediate",
        [
            "FastAPI fundamentals",
            "Path and query parameters",
            "Request and response models",
            "Pydantic validation",
            "CRUD API development",
            "Authentication",
            "API documentation"
        ],
        "Build a Student Records REST API",
        "https://fastapi.tiangolo.com/tutorial/"
    ),

    "Streamlit": curriculum(
        "4 days",
        "Beginner",
        [
            "Streamlit setup",
            "Text and display elements",
            "Input widgets",
            "Session state",
            "File uploads",
            "Dataframes",
            "Application deployment"
        ],
        "Build an Interactive Data Science Application",
        "https://docs.streamlit.io/"
    ),

    "OpenCV": curriculum(
        "2 weeks",
        "Intermediate",
        [
            "Image reading and display",
            "Image resizing and cropping",
            "Color spaces",
            "Image filtering",
            "Edge detection",
            "Contour detection",
            "Face detection"
        ],
        "Build a Real-Time Face Detection Application",
        "https://docs.opencv.org/"
    ),

    "Computer Vision": curriculum(
        "3 weeks",
        "Advanced",
        [
            "Image processing fundamentals",
            "Image classification",
            "Object detection",
            "Image segmentation",
            "Convolutional Neural Networks",
            "Transfer learning",
            "Model evaluation"
        ],
        "Build an Object Detection Application",
        "https://opencv.org/"
    ),

    "JavaScript": curriculum(
        "2 weeks",
        "Beginner to Intermediate",
        [
            "Variables and data types",
            "Functions and arrays",
            "Objects and DOM manipulation",
            "Events",
            "Promises and async/await",
            "Fetch API",
            "ES6 fundamentals"
        ],
        "Build an Interactive Web Application",
        "https://developer.mozilla.org/en-US/docs/Web/JavaScript"
    ),

    "HTML": curriculum(
        "3 days",
        "Beginner",
        [
            "HTML document structure",
            "Headings and paragraphs",
            "Links and images",
            "Tables and lists",
            "Forms and input elements",
            "Semantic HTML"
        ],
        "Build a Personal Portfolio Website",
        "https://developer.mozilla.org/en-US/docs/Web/HTML"
    ),

    "CSS": curriculum(
        "1 week",
        "Beginner",
        [
            "Selectors and properties",
            "Colors and typography",
            "Box model",
            "Flexbox",
            "CSS Grid",
            "Responsive design",
            "Media queries"
        ],
        "Design a Responsive Portfolio Website",
        "https://developer.mozilla.org/en-US/docs/Web/CSS"
    ),

    "React": curriculum(
        "2 weeks",
        "Intermediate",
        [
            "React fundamentals",
            "Components and JSX",
            "Props and state",
            "Event handling",
            "Hooks",
            "React Router",
            "API integration"
        ],
        "Build a React Job Search Interface",
        "https://react.dev/learn"
    ),

    "Node.js": curriculum(
        "2 weeks",
        "Intermediate",
        [
            "Node.js fundamentals",
            "Modules and packages",
            "Asynchronous programming",
            "Express.js basics",
            "REST API development",
            "Database connectivity",
            "Error handling"
        ],
        "Build a REST API for a Job Portal",
        "https://nodejs.org/en/learn"
    ),

    "Git": curriculum(
        "3 days",
        "Beginner",
        [
            "Git installation and configuration",
            "Repositories",
            "git add and git commit",
            "Branches and merging",
            "Remote repositories",
            "GitHub push and pull operations"
        ],
        "Upload and maintain a project on GitHub",
        "https://git-scm.com/doc"
    ),

    "Docker": curriculum(
        "1 week",
        "Intermediate",
        [
            "Container fundamentals",
            "Images and containers",
            "Dockerfile",
            "Building images",
            "Container networking",
            "Docker Compose"
        ],
        "Containerize a Python Application",
        "https://docs.docker.com/get-started/"
    ),

    "AWS": curriculum(
        "2 weeks",
        "Intermediate",
        [
            "Cloud computing fundamentals",
            "Identity and Access Management",
            "EC2",
            "S3",
            "Lambda fundamentals",
            "Cloud deployment",
            "Basic cloud security"
        ],
        "Deploy a Python Application on AWS",
        "https://skillbuilder.aws/"
    ),

    "ETL": curriculum(
        "1 week",
        "Intermediate",
        [
            "ETL fundamentals",
            "Data extraction",
            "Data transformation",
            "Data loading",
            "Data validation",
            "Pipeline scheduling",
            "Data quality checks"
        ],
        "Build a CSV-to-Database ETL Pipeline",
        "https://learn.microsoft.com/en-us/azure/data-factory/"
    ),

    "Apache Spark": curriculum(
        "2 weeks",
        "Advanced",
        [
            "Apache Spark architecture",
            "RDDs and DataFrames",
            "Spark SQL",
            "Data transformations",
            "Data processing operations",
            "Partitioning",
            "Performance optimization"
        ],
        "Build a Large-Scale Data Processing Pipeline",
        "https://spark.apache.org/docs/latest/"
    ),

    "MongoDB": curriculum(
        "1 week",
        "Intermediate",
        [
            "NoSQL database fundamentals",
            "Documents and collections",
            "CRUD operations",
            "Query operators",
            "Aggregation pipelines",
            "Indexes",
            "Database integration"
        ],
        "Build a MongoDB-powered Student Management API",
        "https://www.mongodb.com/docs/"
    ),

    "Snowflake": curriculum(
        "2 weeks",
        "Intermediate",
        [
            "Cloud data warehouse fundamentals",
            "Snowflake architecture",
            "Databases and schemas",
            "Virtual warehouses",
            "Data loading",
            "SQL transformations",
            "Time Travel fundamentals"
        ],
        "Build a Cloud Data Warehouse Analytics Pipeline",
        "https://docs.snowflake.com/"
    ),

    "REST API": curriculum(
        "1 week",
        "Intermediate",
        [
            "HTTP methods",
            "REST architecture",
            "API endpoints",
            "Request and response handling",
            "JSON data",
            "Authentication",
            "API testing"
        ],
        "Build a REST API for a Student Management System",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP"
    ),

    "LangChain": curriculum(
        "2 weeks",
        "Advanced",
        [
            "LangChain fundamentals",
            "Language model integration",
            "Prompt templates",
            "Chains and components",
            "Document loaders",
            "Retrievers",
            "Tool integration"
        ],
        "Build a Document Question Answering Application",
        "https://docs.langchain.com/"
    ),

    "LlamaIndex": curriculum(
        "1 week",
        "Advanced",
        [
            "LlamaIndex fundamentals",
            "Document loading",
            "Data indexing",
            "Embeddings",
            "Query engines",
            "Retrieval systems",
            "Response synthesis"
        ],
        "Build a Document Search and Question Answering System",
        "https://docs.llamaindex.ai/"
    ),

    "Transformers": curriculum(
        "2 weeks",
        "Advanced",
        [
            "Transformer architecture",
            "Attention mechanisms",
            "Tokenization",
            "Pretrained models",
            "Fine-tuning",
            "Text generation",
            "Model evaluation"
        ],
        "Build a Text Classification Application",
        "https://huggingface.co/docs/transformers/"
    ),

    "RAG": curriculum(
        "2 weeks",
        "Advanced",
        [
            "RAG fundamentals",
            "Document ingestion",
            "Text chunking",
            "Embedding generation",
            "Vector databases",
            "Similarity search",
            "Retrieval and generation",
            "RAG evaluation"
        ],
        "Build a PDF Question Answering Assistant",
        "https://huggingface.co/learn"
    ),

    "OOP": curriculum(
        "1 week",
        "Beginner to Intermediate",
        [
            "Classes and objects",
            "Constructors",
            "Inheritance",
            "Polymorphism",
            "Encapsulation",
            "Abstraction",
            "Method overriding"
        ],
        "Build a Library Management System using OOP",
        "https://docs.python.org/3/tutorial/classes.html"
    ),

    "Data Structures": curriculum(
        "2 weeks",
        "Intermediate",
        [
            "Arrays and strings",
            "Linked lists",
            "Stacks and queues",
            "Hash tables",
            "Trees and binary search trees",
            "Graphs",
            "Sorting and searching algorithms",
            "Time and space complexity"
        ],
        "Build a Data Structures Practice Application",
        "https://www.geeksforgeeks.org/data-structures/"
    ),

    "Data Analysis": curriculum(
        "2 weeks",
        "Beginner to Intermediate",
        [
            "Understanding datasets",
            "Data cleaning",
            "Exploratory data analysis",
            "Descriptive statistics",
            "Data aggregation",
            "Trend analysis",
            "Business insights"
        ],
        "Perform Business Analysis on a Sales Dataset",
        "https://pandas.pydata.org/docs/"
    ),

    "Data Cleaning": curriculum(
        "1 week",
        "Beginner",
        [
            "Identifying missing values",
            "Removing duplicate records",
            "Handling outliers",
            "Data type conversion",
            "String cleaning",
            "Data validation",
            "Data transformation"
        ],
        "Clean and prepare a real-world dataset",
        "https://pandas.pydata.org/docs/"
    ),

    "Data Visualization": curriculum(
        "1 week",
        "Beginner to Intermediate",
        [
            "Understanding chart types",
            "Bar and line charts",
            "Scatter plots",
            "Distribution charts",
            "Correlation visualization",
            "Dashboard design",
            "Data storytelling"
        ],
        "Build a Data Analysis Dashboard",
        "https://matplotlib.org/stable/tutorials/"
    ),

    "Artificial Intelligence": curriculum(
        "2 weeks",
        "Intermediate",
        [
            "AI fundamentals",
            "Intelligent agents",
            "Search algorithms",
            "Knowledge representation",
            "Machine learning fundamentals",
            "AI applications",
            "Responsible AI"
        ],
        "Build an Intelligent Recommendation Application",
        "https://www.ibm.com/think/topics/artificial-intelligence"
    ),

    "Azure": curriculum(
        "2 weeks",
        "Intermediate",
        [
            "Cloud computing fundamentals",
            "Azure portal",
            "Azure Storage",
            "Azure Virtual Machines",
            "Azure SQL",
            "Azure data services",
            "Application deployment"
        ],
        "Deploy a Data Application using Azure",
        "https://learn.microsoft.com/en-us/azure/"
    ),

    "GCP": curriculum(
        "2 weeks",
        "Intermediate",
        [
            "Google Cloud fundamentals",
            "Compute Engine",
            "Cloud Storage",
            "BigQuery",
            "Cloud Functions",
            "Data processing",
            "Cloud deployment"
        ],
        "Build a Data Analytics Solution on Google Cloud",
        "https://cloud.google.com/docs"
    ),

    "Tableau": curriculum(
        "2 weeks",
        "Intermediate",
        [
            "Tableau fundamentals",
            "Connecting data sources",
            "Dimensions and measures",
            "Calculated fields",
            "Filters and parameters",
            "Dashboard creation",
            "Data storytelling"
        ],
        "Build an Interactive Sales Dashboard",
        "https://help.tableau.com/"
    ),

    "Power BI DAX": curriculum(
        "1 week",
        "Intermediate",
        [
            "DAX fundamentals",
            "Calculated columns",
            "Measures",
            "SUM and AVERAGE",
            "CALCULATE and FILTER",
            "SUMX and COUNTX",
            "Time intelligence"
        ],
        "Create a DAX-powered Business Dashboard",
        "https://learn.microsoft.com/en-us/dax/"
    )
}


# ==========================================================
# 6. CURRICULUM FALLBACK
# ==========================================================

def get_skill_curriculum(skill):

    if skill in SKILL_CURRICULUM:
        return SKILL_CURRICULUM[skill]

    return curriculum(
        "1 week",
        "Based on your current knowledge",
        [
            f"Introduction to {skill}",
            f"Core concepts of {skill}",
            f"Important tools and techniques in {skill}",
            f"Practical applications of {skill}",
            f"Hands-on exercises using {skill}",
            f"Best practices and real-world usage of {skill}"
        ],
        f"Build a practical mini-project using {skill}",
        "https://www.google.com/search?q="
        + quote_plus(skill + " official documentation tutorial")
    )


# ==========================================================
# 7. RESUME EXTRACTION
# ==========================================================

def extract_resume(uploaded_file):

    extension = uploaded_file.name.lower().split(".")[-1]

    try:

        if extension == "pdf":

            pdf_document = fitz.open(
                stream=uploaded_file.getvalue(),
                filetype="pdf"
            )

            text = ""

            for page in pdf_document:
                text += page.get_text()

            pdf_document.close()

            return text

        elif extension == "docx":

            document = docx.Document(
                BytesIO(uploaded_file.getvalue())
            )

            return "\n".join(
                paragraph.text
                for paragraph in document.paragraphs
            )

        elif extension == "txt":

            return uploaded_file.getvalue().decode(
                "utf-8",
                errors="ignore"
            )

        else:

            st.error("Unsupported file format.")
            return ""

    except Exception as error:

        st.error(f"Resume extraction failed: {error}")
        return ""


# ==========================================================
# 8. SKILL EXTRACTION
# ==========================================================

def extract_skills(resume_text):

    if not resume_text:
        return []

    resume_lower = resume_text.lower()

    available_profile_skills = set()

    for profile in CAREER_PROFILES.values():

        available_profile_skills.update(
            profile.get("skills", {}).keys()
        )

    extracted_skills = []

    for skill in available_profile_skills:

        possible_names = [skill]

        if skill in SKILL_ALIASES:
            possible_names.extend(SKILL_ALIASES[skill])

        found = False

        for name in possible_names:

            pattern = (
                r"(?<!\w)"
                + re.escape(name.lower())
                + r"(?!\w)"
            )

            if re.search(pattern, resume_lower):

                found = True
                break

        if found:
            extracted_skills.append(skill)

    return sorted(extracted_skills)




# ==========================================================
# 9. ATS RESUME SCORE
# ==========================================================

def calculate_ats_score(resume_text, extracted_skills):
    """
    Calculate an indicative, rule-based ATS compatibility score.
    This is not a score from an actual employer ATS platform.
    """
    text = resume_text.lower()
    score = 0
    breakdown = {}
    suggestions = []

    # Contact Information - 20 points
    email_found = bool(
        re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', resume_text)
    )
    phone_found = bool(
        re.search(r'(?<!\d)(?:\+?\d[\d\s().-]{8,}\d)(?!\d)', resume_text)
    )

    contact_score = (10 if email_found else 0) + (10 if phone_found else 0)
    breakdown["Contact Information"] = {
        "score": contact_score,
        "maximum": 20
    }

    if not email_found:
        suggestions.append("Add a professional email address.")
    if not phone_found:
        suggestions.append("Add a valid contact phone number.")

    score += contact_score

    # Resume Sections - 25 points
    section_checks = {
        "Education": ["education", "academic background", "qualification"],
        "Experience": ["experience", "internship", "work history", "employment"],
        "Projects": ["projects", "project experience"],
        "Skills": ["skills", "technical skills", "core competencies"],
        "Certifications": ["certifications", "certificates", "courses"]
    }

    section_score = 0

    for section, keywords in section_checks.items():
        found = any(keyword in text for keyword in keywords)

        if found:
            section_score += 5
        else:
            suggestions.append(
                f"Consider adding a clearly labeled {section} section."
            )

    breakdown["Resume Sections"] = {
        "score": section_score,
        "maximum": 25
    }
    score += section_score

    # Technical Skills - 25 points
    skill_count = len(extracted_skills)

    if skill_count >= 10:
        skill_score = 25
    elif skill_count >= 7:
        skill_score = 20
    elif skill_count >= 4:
        skill_score = 15
    elif skill_count >= 2:
        skill_score = 10
    else:
        skill_score = 5 if skill_count else 0

    breakdown["Technical Skills"] = {
        "score": skill_score,
        "maximum": 25
    }

    if skill_count < 7:
        suggestions.append(
            "Add relevant technical skills that match your target role."
        )

    score += skill_score

    # Keyword Optimization - 20 points
    keyword_groups = {
        "Programming": [
            "python", "java", "javascript", "sql", "programming"
        ],
        "Tools and Technologies": [
            "git", "github", "docker", "aws", "azure", "mysql", "mongodb"
        ],
        "Professional Skills": [
            "communication", "problem solving", "teamwork", "analytical"
        ],
        "Project Evidence": [
            "developed", "implemented", "designed", "built", "created"
        ]
    }

    keyword_score = 0

    for category, keywords in keyword_groups.items():
        matches = sum(1 for keyword in keywords if keyword in text)

        if matches >= 3:
            keyword_score += 5
        elif matches >= 1:
            keyword_score += 3

    breakdown["Keyword Optimization"] = {
        "score": keyword_score,
        "maximum": 20
    }

    if keyword_score < 12:
        suggestions.append(
            "Include relevant role-specific keywords and describe your "
            "practical contributions."
        )

    score += keyword_score

    # Resume Content Length - 10 points
    word_count = len(resume_text.split())

    if 300 <= word_count <= 1000:
        length_score = 10
    elif 200 <= word_count < 300 or 1000 < word_count <= 1500:
        length_score = 7
    else:
        length_score = 3

    breakdown["Resume Content Length"] = {
        "score": length_score,
        "maximum": 10
    }

    if word_count < 300:
        suggestions.append(
            "Your resume appears short. Add relevant projects, skills and experience."
        )
    elif word_count > 1500:
        suggestions.append("Consider making your resume more concise.")

    score += length_score

    return {
        "score": min(score, 100),
        "breakdown": breakdown,
        "suggestions": suggestions,
        "word_count": word_count,
        "email_found": email_found,
        "phone_found": phone_found
    }


# ==========================================================
# 9. SESSION STATE
# ==========================================================

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "student_skills" not in st.session_state:
    st.session_state.student_skills = []

if "career_results" not in st.session_state:
    st.session_state.career_results = []

if "uploaded_resume_name" not in st.session_state:
    st.session_state.uploaded_resume_name = ""


# ==========================================================
# 10. RESUME UPLOAD SECTION
# ==========================================================

st.markdown(
    '<div class="section-title">📄 1. Upload Your Resume</div>',
    unsafe_allow_html=True
)

st.write(
    "Upload your resume to discover suitable career paths, "
    "analyze your skills and generate a personalized learning plan."
)

uploaded_file = st.file_uploader(
    "Choose your resume",
    type=["pdf", "docx", "txt"],
    help="Supported formats: PDF, DOCX and TXT",
    key="resume_uploader"
)

col1, col2 = st.columns([1, 5])

with col1:

    analyze_button = st.button(
        "🚀 Analyze Resume",
        type="primary",
        use_container_width=True
    )

with col2:

    if st.button("🔄 Reset Analysis"):

        st.session_state.resume_text = ""
        st.session_state.student_skills = []
        st.session_state.career_results = []
        st.session_state.uploaded_resume_name = ""

        st.rerun()


if analyze_button:

    if uploaded_file is None:

        st.warning("Please upload your resume first.")

    else:

        with st.spinner("Analyzing your resume..."):

            resume_text = extract_resume(uploaded_file)

            if resume_text.strip():

                extracted_skills = extract_skills(resume_text)

                career_results = predict_careers(
                    resume_text,
                    extracted_skills,
                    top_n=5
                )

                st.session_state.resume_text = resume_text
                st.session_state.student_skills = extracted_skills
                st.session_state.career_results = career_results
                st.session_state.uploaded_resume_name = uploaded_file.name

                st.success("Resume analyzed successfully!")

            else:

                st.error(
                    "No readable text found. "
                    "Please upload another resume."
                )


# ==========================================================
# 11. DISPLAY DASHBOARD RESULTS
# ==========================================================

if st.session_state.resume_text:

    # Always display no more than the five highest-ranked careers.
    results = st.session_state.career_results[:5]
    student_skills = st.session_state.student_skills

    st.divider()

    # ======================================================
    # SECTION 2 - RESUME ANALYSIS
    # ======================================================

    st.markdown(
        '<div class="section-title">📊 2. Resume Analysis</div>',
        unsafe_allow_html=True
    )

    st.write(
        f"**Uploaded Resume:** "
        f"{st.session_state.uploaded_resume_name}"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Skills Identified",
        len(student_skills)
    )

    col2.metric(
        "Career Recommendations",
        len(results)
    )

    col3.metric(
        "Resume Status",
        "Analyzed"
    )


    # ======================================================
    # SECTION 2A - ATS RESUME COMPATIBILITY SCORE
    # ======================================================

    st.subheader("📋 ATS Resume Compatibility Score")

    ats_result = calculate_ats_score(
        st.session_state.resume_text,
        student_skills
    )

    ats_score = ats_result["score"]

    ats_col1, ats_col2 = st.columns([1, 2])

    with ats_col1:
        st.metric("Overall ATS Score", f"{ats_score}/100")
        st.progress(ats_score / 100)

        if ats_score >= 80:
            st.success("Strong resume structure")
        elif ats_score >= 60:
            st.info("Good starting point - improvements recommended")
        else:
            st.warning("Resume needs improvement")

    with ats_col2:
        st.markdown("#### ATS Score Breakdown")

        ats_df = pd.DataFrame([
            {
                "Category": category,
                "Score": details["score"],
                "Maximum Score": details["maximum"]
            }
            for category, details in ats_result["breakdown"].items()
        ])

        st.dataframe(
            ats_df,
            use_container_width=True,
            hide_index=True
        )

    st.markdown("#### 🔍 ATS Improvement Suggestions")

    if ats_result["suggestions"]:
        for suggestion in ats_result["suggestions"]:
            st.warning(suggestion)
    else:
        st.success("No major improvements identified by these checks.")

    st.caption(
        "This is an indicative, rule-based resume assessment using "
        "structure, extracted skills, general keywords and content length. "
        "It is not an actual employer ATS score. Real ATS results vary by "
        "employer, role and job description."
    )

    st.divider()


    st.subheader("✅ Skills Identified in Your Resume")

    if student_skills:

        st.write(", ".join(student_skills))

    else:

        st.warning(
            "No matching skills were identified in your resume."
        )

    st.divider()

    # ======================================================
    # SECTION 3 - CAREER RECOMMENDATIONS
    # ======================================================

    st.markdown(
        '<div class="section-title">'
        '🎯 3. Top 5 Career Recommendations'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Career paths recommended based on your resume."
    )

    if results:

        for index, result in enumerate(results, start=1):

            compatibility = result.get("compatibility", 0)

            with st.container(border=True):

                col1, col2 = st.columns([4, 1])

                with col1:

                    st.markdown(
                        f"**{index}. {result['career']}**"
                    )

                with col2:

                    st.markdown(
                        f"### {compatibility}%"
                    )

    else:

        st.warning("No career recommendations were generated.")

    st.divider()

    # ======================================================
    # SECTION 4 - CAREER SKILL GAP ANALYSIS
    # ======================================================

    st.markdown(
        '<div class="section-title">'
        '📊 4. Career Skill Gap Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    if results:

        selected_career = st.selectbox(
            "Select a career to analyze your skill gap",
            [result["career"] for result in results],
            key="dashboard_career_selection"
        )

        selected_result = next(
            item for item in results
            if item["career"] == selected_career
        )

        career_profile = CAREER_PROFILES[selected_career]

        all_skills = list(
            career_profile.get("skills", {}).keys()
        )

        matched_skills = selected_result.get(
            "matched_skills",
            []
        )

        matched_normalized = {
            skill.lower() for skill in matched_skills
        }

        available_skills = [
            skill for skill in all_skills
            if skill.lower() in matched_normalized
        ]

        missing_skills = [
            skill for skill in all_skills
            if skill.lower() not in matched_normalized
        ]

        total_skills = len(all_skills)
        available_count = len(available_skills)
        missing_count = len(missing_skills)

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Required Skills",
            total_skills
        )

        col2.metric(
            "Skills You Have",
            available_count
        )

        col3.metric(
            "Skills To Learn",
            missing_count
        )

        readiness = (
            available_count / total_skills
            if total_skills else 0
        )

        st.subheader("Career Readiness")

        st.progress(readiness)

        st.write(
            f"**{readiness * 100:.1f}%** skill coverage "
            "based on your uploaded resume."
        )

        st.caption(
            "This measures skills identified in the resume. "
            "It does not verify practical proficiency."
        )

        # ----------------------------------------------
        # ALL REQUIRED SKILLS
        # ----------------------------------------------

        st.subheader("📚 All Required Career Skills")

        skill_data = []

        for skill, importance in career_profile["skills"].items():

            status = (
                "Available"
                if skill.lower() in matched_normalized
                else "To Learn"
            )

            importance_label = (
                "High" if importance >= 0.9
                else "Medium" if importance >= 0.7
                else "Supporting"
            )

            curriculum_data = get_skill_curriculum(skill)

            skill_data.append({
                "Required Skill": skill,
                "Importance": importance_label,
                "Your Status": status,
                "Learning Duration": curriculum_data["duration"]
            })

        skill_df = pd.DataFrame(skill_data)

        st.dataframe(
            skill_df,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------
        # AVAILABLE AND MISSING SKILLS
        # ----------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("✅ Skills You Have")

            if available_skills:

                for skill in available_skills:
                    st.success(f"✓ {skill}")

            else:

                st.info("No matching skills identified.")

        with col2:

            st.subheader("🎯 Skills To Learn")

            if missing_skills:

                for skill in missing_skills:
                    st.warning(f"📖 {skill}")

            else:

                st.success("All profile skills were identified.")

        st.divider()

        # ======================================================
        # SECTION 5 - PERSONALIZED LEARNING ROADMAP
        # ======================================================

        st.markdown(
            '<div class="section-title">'
            '🚀 5. Personalized Learning Roadmap'
            '</div>',
            unsafe_allow_html=True
        )

        st.write(
            f"Your learning roadmap for **{selected_career}** "
            "is based on the skills identified and missing "
            "from your resume."
        )

        # ----------------------------------------------
        # DETAILED SKILL-BY-SKILL LEARNING PLAN
        # ----------------------------------------------

        st.subheader("📖 Detailed Skill-by-Skill Learning Plan")

        st.write(
            "Expand each skill to view its learning topics, "
            "estimated duration, difficulty, resource and project."
        )

        ordered_skills = missing_skills + available_skills

        for skill in ordered_skills:

            curriculum_data = get_skill_curriculum(skill)

            is_missing = skill in missing_skills

            status_text = (
                "Priority: Learn"
                if is_missing
                else "Already identified in resume"
            )

            with st.expander(
                f"{'🎯' if is_missing else '✅'} "
                f"{skill} — {status_text}"
            ):

                col1, col2 = st.columns(2)

                col1.metric(
                    "Estimated Learning Duration",
                    curriculum_data["duration"]
                )

                col2.metric(
                    "Difficulty Level",
                    curriculum_data["level"]
                )

                st.markdown("#### 📌 Topics to Study")

                for index, topic in enumerate(
                    curriculum_data["topics"],
                    start=1
                ):

                    st.write(f"{index}. {topic}")

                st.markdown("#### 🛠️ Practical Project")

                st.info(curriculum_data["project"])

                st.markdown("#### 🌐 Recommended Learning Resource")

                st.markdown(
                    f"[Open Learning Resource]"
                    f"({curriculum_data['resource']})"
                )

        st.divider()

        # ======================================================
        # THREE LEARNING STAGES
        # ======================================================

        st.subheader("🗺️ Step-by-Step Learning Journey")

        stage_1_skills = missing_skills[:2]
        stage_2_skills = missing_skills[2:4]
        stage_3_skills = missing_skills[4:]

        # ----------------------------------------------
        # STAGE 1 - FUNDAMENTALS
        # ----------------------------------------------

        with st.expander(
            "📘 Stage 1 - Fundamentals",
            expanded=True
        ):

            st.write(
                "Build a strong foundation in the essential skills "
                "required for your selected career."
            )

            if stage_1_skills:

                for skill in stage_1_skills:

                    curriculum_data = get_skill_curriculum(skill)

                    st.markdown(f"### {skill}")

                    st.write(
                        f"**Duration:** {curriculum_data['duration']}"
                    )

                    st.write("**Topics:**")

                    for topic in curriculum_data["topics"][:4]:
                        st.write(f"- {topic}")

                    st.write(
                        f"**Practical Project:** "
                        f"{curriculum_data['project']}"
                    )

                    st.markdown(
                        f"[Learning Resource]"
                        f"({curriculum_data['resource']})"
                    )

                    st.divider()

            else:

                st.success(
                    "Your resume already identifies the foundational "
                    "skills in this career profile."
                )

                st.markdown("""
                - Revise the fundamentals of your existing skills.
                - Practice basic coding and problem-solving exercises.
                - Solve beginner-level real-world problems.
                - Strengthen your understanding through hands-on practice.
                """)

        # ----------------------------------------------
        # STAGE 2 - INTERMEDIATE SKILLS
        # ----------------------------------------------

        with st.expander(
            "📗 Stage 2 - Intermediate Skills",
            expanded=True
        ):

            st.write(
                "Develop practical knowledge and learn how to apply "
                "your skills to real-world problems."
            )

            if stage_2_skills:

                for skill in stage_2_skills:

                    curriculum_data = get_skill_curriculum(skill)

                    st.markdown(f"### {skill}")

                    st.write(
                        f"**Duration:** {curriculum_data['duration']}"
                    )

                    st.write("**Topics:**")

                    for topic in curriculum_data["topics"][4:]:
                        st.write(f"- {topic}")

                    st.write(
                        f"**Practical Project:** "
                        f"{curriculum_data['project']}"
                    )

                    st.markdown(
                        f"[Learning Resource]"
                        f"({curriculum_data['resource']})"
                    )

                    st.divider()

            else:

                st.success(
                    "Your existing skill profile provides a foundation "
                    "for intermediate-level development."
                )

                st.markdown("""
                - Combine two or more existing skills in one application.
                - Practice intermediate-level coding problems.
                - Work with real-world datasets or practical use cases.
                - Improve code quality, debugging and problem-solving.
                """)

                st.info(
                    "**Suggested Mini Project:** Build a practical "
                    "application that combines your existing career skills."
                )

        # ----------------------------------------------
        # STAGE 3 - ADVANCED SKILLS
        # ----------------------------------------------

        with st.expander(
            "📕 Stage 3 - Advanced Skills",
            expanded=True
        ):

            st.write(
                "Develop advanced problem-solving abilities and "
                "demonstrate your knowledge through projects."
            )

            if stage_3_skills:

                for skill in stage_3_skills:

                    curriculum_data = get_skill_curriculum(skill)

                    st.markdown(f"### {skill}")

                    st.write(
                        f"**Duration:** {curriculum_data['duration']}"
                    )

                    st.write("**Topics:**")

                    for topic in curriculum_data["topics"]:
                        st.write(f"- {topic}")

                    st.write(
                        f"**Practical Project:** "
                        f"{curriculum_data['project']}"
                    )

                    st.markdown(
                        f"[Learning Resource]"
                        f"({curriculum_data['resource']})"
                    )

                    st.divider()

            else:

                st.success(
                    "You have covered the skills identified as missing "
                    "in your resume. Now focus on advanced implementation "
                    "and project development."
                )

                st.markdown("""
                - Build an end-to-end career-specific project.
                - Work with larger or more complex datasets where relevant.
                - Apply optimization and best practices.
                - Test, document and deploy your application.
                - Publish your project on GitHub.
                """)

                st.info(
                    "**Suggested Capstone Project:** Develop a complete "
                    "industry-oriented application demonstrating your "
                    "existing career skills."
                )

        # ======================================================
        # DOWNLOAD COMPLETE LEARNING ROADMAP
        # ======================================================

        st.divider()

        st.subheader("📥 Download Your Complete Learning Roadmap")

        download_rows = []

        for skill, importance in career_profile["skills"].items():

            curriculum_data = get_skill_curriculum(skill)

            status = (
                "Available"
                if skill.lower() in matched_normalized
                else "To Learn"
            )

            importance_label = (
                "High" if importance >= 0.9
                else "Medium" if importance >= 0.7
                else "Supporting"
            )

            download_rows.append({
                "Career": selected_career,
                "Required Skill": skill,
                "Importance": importance_label,
                "Your Status": status,
                "Duration": curriculum_data["duration"],
                "Difficulty Level": curriculum_data["level"],
                "Learning Topics": "; ".join(
                    curriculum_data["topics"]
                ),
                "Practical Project": curriculum_data["project"],
                "Learning Resource": curriculum_data["resource"]
            })

        download_df = pd.DataFrame(download_rows)

        st.download_button(
            label="📥 Download Complete Learning Roadmap",
            data=download_df.to_csv(index=False),
            file_name=(
                f"{selected_career.replace(' ', '_')}_Learning_Roadmap.csv"
            ),
            mime="text/csv"
        )

    st.divider()

    # ======================================================
    # PREMIUM FOOTER
    # ======================================================

    st.markdown("""
    <div class="dashboard-footer">
        <h4 style="color:#A5BFFF;">🎯 CareerCompass AI</h4>
        <p>Discover your potential. Develop your skills. Build your future.</p>
        <p style="font-size:12px;">
            AI-Powered Career Discovery & Personalized Learning Platform
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================================
# 12. INITIAL DASHBOARD STATE
# ==========================================================

else:

    st.info(
        "👆 Upload your resume and click Analyze Resume "
        "to display your personalized career dashboard."
    )

    st.markdown("### What CareerCompass AI provides")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.markdown("#### 🎯 Career Discovery")

            st.markdown("""
            - Top 5 career recommendations
            - Resume-based career matching
            - Project and education evidence
            """)

    with col2:

        with st.container(border=True):

            st.markdown("#### 📊 Skill Gap Analysis")

            st.markdown("""
            - Existing skills
            - Missing skills
            - Career readiness
            """)

    col3, col4 = st.columns(2)

    with col3:

        with st.container(border=True):

            st.markdown("#### 🚀 Learning Roadmap")

            st.markdown("""
            - Detailed skill topics
            - Learning duration and difficulty
            - Recommended learning resources
            - Practical projects
            """)

    with col4:

        with st.container(border=True):

            st.markdown("#### 📥 Export")

            st.markdown("""
            - Complete downloadable roadmap
            - Career-specific skill report
            - Learning resource links
            """)
