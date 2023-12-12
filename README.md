# WhatsApp Chatbot with React Flow Visualization

## Project Overview
This project consists of a WhatsApp chatbot implemented using `whatsapp-web.js` and a web application for visualizing chatbot flows using `React Flow`. The chatbot interacts with users on WhatsApp, handling specific commands and responding accordingly. The web application allows visualizing and exporting the chatbot flow to JSON format.

## Key Features
- WhatsApp chatbot integration using `whatsapp-web.js`.
- Flow visualization in a web interface using `React Flow`.
- Backend API for handling chatbot flow data and user interactions.

## Prerequisites
- Node.js and npm
- Python (for the Flask backend)
- A WhatsApp account for testing the chatbot

## Installation

## 1. Setting up the Backend (Flask API):
   cd api
   flask run
   
## 2. Setting up the WhatsApp Chatbot
   cd api/whatsapp-chatbot
   npm i nodemon
   nodemon bot.js
   
## 3. Setting up the React Frontend
   cd front
   npm install
   npm run dev
