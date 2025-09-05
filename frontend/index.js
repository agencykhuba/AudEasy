const express = require('express');
const app = express();
app.get('/', (req, res) => res.send('AudEasy Frontend'));
app.get('/api', (req, res) => res.json({ message: 'AudEasy API' }));
app.listen(3000, () => console.log('AudEasy server running on port 3000'));
