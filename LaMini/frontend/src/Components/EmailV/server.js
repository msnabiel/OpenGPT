const express = require('express');
const nodemailer = require('nodemailer');
const bodyParser = require('body-parser'); // Use body-parser to parse incoming data
const cors = require('cors'); // Enable CORS for requests from React frontend (if necessary)

const app = express();
const port = process.env.PORT || 3000; // Use environment variable for port or default to 5000

// Configure email transport (replace with your actual email credentials and service provider)
const transporter = nodemailer.createTransport({
  service: 'gmail', // Replace with your service provider (e.g., 'gmail', 'outlook', etc.)
  auth: {
    user: 'syednabielm@gmail.com',
    pass: 'Nabiel123',
  },
});

app.use(cors()); // Enable CORS if necessary
app.use(bodyParser.json()); // Parse JSON data from React frontend

app.post('/api/send-email', async (req, res) => {
  const { name, email, message } = req.body;

  const mailOptions = {
    from: 'syednabielm@gmail.com',
    to: 'msyednabiel@gmail.com', // Replace with recipient email address
    subject: `Email from ${name} - Contact Form`,
    html: `
      <h3>Name: ${name}</h3>
      <p>Email: <span class="math-inline">\{email\}</p\>
<p\>Message\:</p\>
<p\></span>{message}</p>
    `,
  };

  try {
    await transporter.sendMail(mailOptions);
    res.json({ message: 'Email sent successfully!' });
  } catch (error){
    // Handle errors here (e.g., log error, send error response)
    console.error(error); // Log the error to the console for debugging
  }
});
