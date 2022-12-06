import numpy as np

def predict_img(model, img):
    new_img = np.expand_dims(img, axis=0)
    res = (model.predict(new_img)[0, :, :, 0] > 0.5).astype("uint8")
    return res

def get_title(img):
    if np.any(img):
        return "Răng sâu"
    
    return "Răng thường"

def overlay_img(img, mask):
    new_img = np.array(img).copy()
    pred = np.array(mask)

    for i in range(pred.shape[0]):
        for j in range(pred.shape[1]):
            if pred[i, j]:
                new_img[i, j] = np.mean([new_img[i, j], [0, 255, 0]], axis=0)

    return new_img