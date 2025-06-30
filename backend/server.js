const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const app = express();
const PORT = 5000;

// Middleware
app.use(cors());
app.use(express.json()); // for parsing application/json

// Route
app.post('/chat', (req, res) => {
    const query = req.body.query;

    if (!query) {
        return res.status(400).json({ error: "Missing 'query' in request body." });
    }

    // Safely format the command
    const command = `python chatbot.py "${query.replace(/"/g, '\\"')}"`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error("Error running Python script:", error.message);
            return res.status(500).json({ response: "Error processing your request." });
        }
        if (stderr) {
            console.error("Python stderr:", stderr);
        }

        res.json({ response: stdout.trim() });
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`✅ Server is running at http://localhost:${PORT}`);
});
