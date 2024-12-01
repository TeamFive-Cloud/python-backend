import express from 'express';
import { exec } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import fs from 'fs';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const router = express.Router();

const pythonPath = process.env.PYTHON_PATH || 'python';
const newsScriptPath = path.resolve(__dirname, '../newsRequirement.py'); // 确保路径正确
const pitchforkScriptPath = path.resolve(__dirname, '../pitchforkScraper.py'); // 确保路径正确
const freeScoresScriptPath = path.resolve(__dirname, '../freeScoresScraper.py'); // 确保路径正确

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

router.get('/scrape-pitchfork', (req, res) => {
  console.log('Attempting to scrape Pitchfork reviews...');
  exec(`${pythonPath} ${pitchforkScriptPath}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing script: ${error}`);
      return res.status(500).send('Error executing script');
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
    res.send('Pitchfork reviews scraping completed');
  });
});

router.get('/scrape-freescores', (req, res) => {
  console.log('Attempting to scrape Free Scores...');
  exec(`${pythonPath} ${freeScoresScriptPath}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing script: ${error}`);
      return res.status(500).send('Error executing script');
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
    res.send('Free Scores scraping completed');
  });
});

router.get('/all-news', (req, res) => {
  console.log('Fetching all news...');
  const filePath = path.resolve(__dirname, '../allNews.json');
  console.log(`Reading file from path: ${filePath}`);
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error(`Error reading file: ${err}`);
      return res.status(500).send('Error reading file');
    }
    console.log('File read successfully');
    res.setHeader('Content-Type', 'application/json');
    res.send(data);
  });
});

router.get('/pitchfork-reviews', (req, res) => {
  console.log('Fetching Pitchfork reviews...');
  const filePath = path.resolve(__dirname, '../pitchforkReviews.json');
  console.log(`Reading file from path: ${filePath}`);
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error(`Error reading file: ${err}`);
      return res.status(500).send('Error reading file');
    }
    console.log('File read successfully');
    console.log(`Data: ${data}`);
    res.setHeader('Content-Type', 'application/json');
    res.send(data);
  });
});

router.get('/freescores', (req, res) => {
  console.log('Fetching Free Scores...');
  const filePath = path.resolve(__dirname, '../freeScores.json');
  console.log(`Reading file from path: ${filePath}`);
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error(`Error reading file: ${err}`);
      return res.status(500).send('Error reading file');
    }
    console.log('File read successfully');
    console.log(`Data: ${data}`);
    res.setHeader('Content-Type', 'application/json');
    res.send(data);
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