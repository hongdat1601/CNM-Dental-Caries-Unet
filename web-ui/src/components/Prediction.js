import React, { useState } from 'react';
import { HiArrowNarrowRight } from 'react-icons/hi';
import instanceApi from '../api/instanceApi';
import ImagePreview from './ImagePreview';
import styles from './Prediction.module.css';

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
                .catch(() => {
                    setSrcPred('');
                    alert('Có gì đó sai sai!');
                });
        } else {
            alert('Hãy chọn ảnh trước khi chuẩn đoán!');
        }
    };

    return (
        <div className={styles.prediction}>
            <div>
                <input
                    className={styles.fileInput}
                    type="file"
                    onChange={fileHandle}
                />
                <ImagePreview src={srcImg} name="Original Image" />
            </div>
            <div>
                <HiArrowNarrowRight className={styles.predictIcon} />
                <button className="btn btn-primary" onClick={predictHandle}>
                    Chuẩn đoán
                </button>
            </div>
            <div>
                <ImagePreview src={srcPred} name="Prediction Image" />
                <div className={styles.title}>
                    <span className="text-danger">Kết quả:</span> {titlePred}
                </div>
            </div>
        </div>
    );
}

export default Prediction;
