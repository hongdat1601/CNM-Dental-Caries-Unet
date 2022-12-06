import React, { useState } from 'react';
import instanceApi from '../api/instanceApi';
import ImagePreview from './ImagePreview';
import './Prediction.css';

function Prediction() {
    const [srcImg, setSrcImg] = useState('');
    const [srcPred, setSrcPred] = useState('');
    const [file, setFile] = useState();
    const [titlePred, setTitlePred] = useState('None');

    const fileHandle = (file) => {
        let img_file = file.target.files[0];
        if (img_file) {
            setFile(img_file);
            const objectURL = URL.createObjectURL(img_file);
            setSrcImg(objectURL);
        }
    };

    const predictHandle = () => {
        if (file) {
            setSrcPred(
                'https://upload.wikimedia.org/wikipedia/commons/b/b9/Youtube_loading_symbol_1_(wobbly).gif'
            );
            let formData = new FormData();
            formData.append('file', file);

            instanceApi
                .post('/predict', formData)
                .then((data) => {
                    setSrcPred('data:image/jpeg;base64,' + data.data.data);
                    setTitlePred(data.data.title);
                })
                .catch(() => setSrcPred(''));
        } else {
            alert('Hãy chọn ảnh trước khi chuẩn đoán!');
        }
    };

    return (
        <div className="prediction">
            <div>
                <input type="file" onChange={fileHandle} />
                <ImagePreview src={srcImg} name="Original Image" />
            </div>
            <div>
                <button onClick={predictHandle}>Chuẩn đoán</button>
            </div>
            <div>
                <ImagePreview src={srcPred} name="Prediction Image" />
                <span>Kết quả: {titlePred}</span>
            </div>
        </div>
    );
}

export default Prediction;
