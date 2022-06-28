#Project description
This is a "pet-project" which I work on in order to internalize the knowledge I acquire from courses and other resources. I scrape input data and create ML models for real estate price prediction.

**Goals**:

1)	Scrape a real estate listing website, which is the input data for the model. The code is “re-usable” so the data can be updated each couple of months. The raw data is pre-cleaned and stored in SQL and in a JSON file (pretty redundant atm.) – **Mostly done**
2)	Prepare the raw input data for the machine learning models. Including prefiltering unusable predictors, outlier censoring, impute missing values and normalizing/1-hot-encoding the features. – **Mostly done**
3)	Process textual data: e.g. create TF-IDF to get keywords or use clustering/other processing technique to reduce dimensionality. Process image data - **Close future/more distant future**
4)	Build both a “hand-written” ANN model which has the sole purpose of practicing so that I understand what I am doing. Then use TensorFlow to create a more optimized model. – **Currently working on it**
5)	Create a small webapp where a pre-trained model can be used to predict prices for individual samples (flats/houses). - **Distant future**

**Folder structure**
[scraper]( https://github.com/horn1994/realestate/tree/main/scraper): functions related to data gathering
[models]( https://github.com/horn1994/realestate/tree/main/models): functions related to ML models