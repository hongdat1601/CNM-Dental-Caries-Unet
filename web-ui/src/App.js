import React from 'react';
import Prediction from './components/Prediction';
import './App.css';
import Area from './components/Area';

function App() {
    return (
        <div className="App">
            <header className="header">
                <h1>CHUẨN ĐOÁN SÂU RĂNG</h1>
            </header>
            <div className="content">
                <div className="container">
                    <Area title="">
                        <Prediction />
                    </Area>
                </div>
            </div>
            <footer className="footer">
                <span>Copyright &copy; 2022 Nhóm 4</span>
            </footer>
        </div>
    );
}

export default App;
