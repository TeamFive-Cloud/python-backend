import express from 'express';
import { exec } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const router = express.Router();

const pythonPath = process.env.PYTHON_PATH || 'python';
const newsScriptPath = path.resolve(__dirname, '../newsRequirement.py'); // 确保路径正确

router.get('/scrape-news', (req, res) => {
  console.log('Attempting to scrape news...');
  exec(`${pythonPath} ${newsScriptPath}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing script: ${error}`);
      return res.status(500).send('Error executing script');
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
    res.send('News scraping completed');
  });
});

router.get('/test-connection', (req, res) => {
  const testUrl = 'http://localhost:5000/';
  console.log(`Testing connection to ${testUrl}`);
  exec(`curl -I ${testUrl}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error testing connection: ${error}`);
      return res.status(500).send('Error testing connection');
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
    res.send(`Connection test completed: ${stdout}`);
  });
});

export default router;