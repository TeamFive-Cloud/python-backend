import express from 'express';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';
import cors from 'cors'; // 引入 CORS 中间件
import newsRoutes from './routes/news.js';

dotenv.config(); // 确保在应用程序启动时加载环境变量

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

// 验证 dotenv 是否正确加载
console.log('Environment variable TEST_VAR:', process.env.TEST_VAR);

// Middleware to log all requests
app.use((req, res, next) => {
  console.log(`Request Method: ${req.method}, Request URL: ${req.url}`);
  next();
});

// Middleware to log all responses
app.use((req, res, next) => {
  const originalSend = res.send;
  res.send = function (body) {
    console.log(`Response Status: ${res.statusCode}, Response Body: ${body}`);
    originalSend.apply(this, arguments);
  };
  next();
});

// Enable CORS for all routes
app.use(cors());

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, 'public')));

// Define a simple route for the root path
app.get('/', (req, res) => {
  res.send('Welcome to the backend server!');
});

// Use the news routes
app.use('/api/news', newsRoutes);

// Catch-all route for handling 404 errors
app.use((req, res, next) => {
  res.status(404).send('This localhost page can’t be found');
  console.error(`404 Error - Page not found: ${req.url}`);
});

// 移除 app.listen 部分
// const PORT = process.env.PORT || 5000;
// app.listen(PORT, () => {
//   console.log(`Server running on port ${PORT}`);
// });

export default app;