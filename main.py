from fastapi import FastAPI, Request,Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
import pickle
from preprocess import preprocess
from fastapi.staticfiles import StaticFiles




templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

model = load_model('Models/lstm_model.h5')

with open('Tokenizer/tokenizer.pickle','rb') as file:
    tokenizer = pickle.load(file)

# ID to label mab
id2label = {0: 'EG', 1: 'LB', 2: 'LY', 3: 'MA', 4: 'SD'}

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("predict_page.html", {"request": request})

# predict route
@app.post("/predict", response_class=HTMLResponse)
def predict_dialect(request: Request, text: str = Form(...)):
    processed_text = preprocess(text)
    tokens = tokenizer.texts_to_sequences([processed_text])
    padded_tokens = tf.keras.utils.pad_sequences(tokens, maxlen=32, padding='post')
    prediction = tf.argmax(model.predict(padded_tokens), axis=1)
    prediction_label = id2label[prediction.numpy()[0]]
    
    # Render the prediction page with the result
    return templates.TemplateResponse("predict_page.html", {
        "request": request, 
        "result": prediction_label,
        "original_text": text
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


    

    


