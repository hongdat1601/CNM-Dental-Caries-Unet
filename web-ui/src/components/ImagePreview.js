import React, { useEffect, useRef } from 'react';
import styles from './ImagePreview.module.css';

function ImagePreview(props) {
    const imgRef = useRef();
    const titleRef = useRef();

    useEffect(() => {}, []);

    return (
        <div className={styles.imageReview}>
            <img
                src={props.src}
                alt={props.name}
                ref={imgRef}
                hidden={props.src.length <= 0}
            />
            <span ref={titleRef} hidden={props.src.length > 0}>
                {props.name}
            </span>
        </div>
    );
}

export default ImagePreview;
