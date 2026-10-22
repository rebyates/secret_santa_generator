# secret_santa_generator
A quick streamlit app for randomly allocating names in a group for Secret Santa.

## Running the app

```bash
pip install -r requirements.txt
streamlit run app.py
```

Enter a list of names and click **Generate**. Each person is randomly allocated
someone else in the list: nobody gets themselves, and every name is allocated
exactly once.
