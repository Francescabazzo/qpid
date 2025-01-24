# 💘 QPID - Find your perfect match! 

## Table of contents: 
- [Overview](#overview)
- [Disclaimer](#disclaimer) 
- [Features](#features) 
- [Project structure](#structure)
- [Technologies used](#technologies) 
- [Usage](#usage)
- [Installation](#installation)
- [Future improvements](#future)

 <a id="overview"></a>
 ## 📌 Overview 
This repository contains the source code for **QPID**, a **dating web application** designed to help people find meaningful connections based on shared interests. 
Users need to register, fill out a profile with their information and interests and they will get results based on their characteristics and what they look for in a partner. 

<a id="disclaimer"></a>
## ⚠️ Disclaimer 
This is a **Proof-of-Concept Application** developed for a university project! 
We do not guarantee security standards, privacy policies compliance and constant bug fixing, so please do not consider using this software as a professional tool.

<a id="features"></a>
## ✨ Features
- **Smart Profile Matching**: Recommendations based on user activity and preferences.
- **Like/Dislike & Matching System**: Users can interact with suggested profiles and receive mutual match notifications.
- **Dynamic Match Reset & Search**: If users are unsatisfied with their suggestions, they can refresh and explore new matches instantly.
- **Authentication and Profile Management**: Personalized profile creation.

<a id="structure"></a>

## 📂 Project Structure  

```plaintext
qpid/
│── .github/
|   ├── workflows/
│   │   ├── python-app.yml
│── .streamlit/              
│   ├── config.toml
│── artifacts/              
│   ├── __init__.py
│   ├── calculate_scores.pkl 
│   ├── get_matches.pkl
│── backend/              
│   ├── README.md
│   ├── __init__.py
│   ├── backend.py
│   ├── exporter.py
│   ├── importer.py
│── data/            
│   ├── processed/
│   │   ├── dataset.csv
│   │   ├── dataset2.csv
│   │   ├── db_dump.json
│── notebooks/            
│   ├── backend.ipynb
│── pages/            
│   ├── login/
│   │   ├── __init__.py
│   │   ├── login.py
│   │   ├── registration.py
│   ├── profile/
│   │   ├── __init__.py
│   │   ├── profile_intos.py
│   │   ├── profile_me.py
│   ├── 1_Description.py
│   ├── 2_Profile.py
│   ├── 3_Matches.py
│   ├── 4_Likes&Dislikes.py
│   ├── __init__.py
│── utils/            
│   ├── db/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── queries.py
│   ├── images/
│   │   ├── logo.png
│   │   ├── profile_pic.png
│   ├── __init__.py
│   ├── converters.py
│   ├── logger.py
│   ├── utils.py
│── .gitignore
│── Home.py
│── README.md
│── requirements.text
``` 

<a id="technologies"></a>
## 💻Technologies used 

- **Programming Language**: Python 
- **Web Framework**: Streamlit
- **Database**: MySQL
- **Data visualization**: Pandas, Seaborn, Scikit-learn, Scipy, Plotly
- **Machine Learning**: Scikit-learn (HDBscan clustering, Nearest Neighbors), Scipy

<a id="usage"></a>
## 🔧 Usage 

1. **Registration**: Create an account by providing basic information. 
2. **Profile Setup**: Complete the profile to enable QPID to suggest matches based on interests preferences. 
3. **Match Suggestions**: View and interact with suggested profiles based on interests. 
4. **Like/Dislike**: Express interest in profiles or skip them. 
5. **Match Refresh**: Refresh match suggestions in real-time when needed.

<a id="installation"></a>
## 🛠️ Installation 

To run QPID locally, follow these steps:

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/qpid.git
   ```
2. Navigate into the project directory:
   ```bash
   cd qpid
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the application:
   ```bash
   streamlit run Home.py
   ```

<a id="future"></a>
## 🚀 Future Plans

- **Chat Feature**: Implement messaging capabilities for matched users. 
- **Analytics**: Collaboration with an analytics service. 
- **User Experience**: Improve the user experience by changing the web framework. 
