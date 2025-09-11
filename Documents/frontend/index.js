const express = require('express');
const fetch = require('node-fetch');
const app = express();
app.get('/', (req, res) => res.send('AudEasy Frontend'));
app.get('/api', async (req, res) => {
    const response = await fetch('http://127.0.0.1:8000/audit');
    const data = await response.json();
    res.json({ message: 'AudEasy API', audit: data });
});
app.listen(3000, () => console.log('AudEasy server running on port 3000'));
