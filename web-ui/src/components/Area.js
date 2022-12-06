import React from 'react';
import styles from './Area.module.css';

function Area(props) {
    return (
        <div className={styles.area}>
            <h2 className={styles.title}>{props.title}</h2>
            <div className={styles.children}>{props.children}</div>
        </div>
    );
}

export default Area;
