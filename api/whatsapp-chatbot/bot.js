const axios = require('axios');
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

const fetchDataFromAPI = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5000/get-flow');
        return response.data;
      } catch (error) {
        console.error('Error getting flow:', error);
        // Handle errors here
      }
};

const postUserInteraction = async (userName, phoneNumber, action) => {
    const apiUrl = 'http://127.0.0.1:5000/user-interaction'; 
    const data = {
        whatsapp_user_name: userName,
        phone_number: phoneNumber,
        action: action,
        date: new Date().toLocaleDateString(), // Format of the date as YYYY-MM-DD
        time: new Date().toLocaleTimeString()// Current time
    };

    try {
        const response = await axios.post(apiUrl, data);
        console.log(response.data.message); // Log the response from the API
    } catch (error) {
        console.error('Error posting user interaction:', error);
    }
};


const client = new Client({
    authStrategy: new LocalAuth()
});

client.on('qr', qr => {
    qrcode.generate(qr, {small: true});
});

client.on('ready', async () => {
    console.log('Client is ready!');
});

client.on('message', async message => {
    const data = await fetchDataFromAPI();
    if (data && data.nodes && data.nodes.length > 0) {
        const phoneNumber = message.from; // The sender's phone number
        const userName = message.notifyName; // User's name (if available and in contacts)
        const currentDate = new Date(); // Current date and time
        const formattedDate = currentDate.toLocaleDateString();
        const formattedTime = currentDate.toLocaleTimeString(); 

        if (message.body === data.nodes[1].label) {
            client.sendMessage(phoneNumber, data.nodes[2].label);
            action = 'Request Consultation';

        } else if (message.body === data.nodes[3].label || message.body === data.nodes[4].label) {
            client.sendMessage(phoneNumber, data.nodes[5].label);
            action = (message.body===data.nodes[3].label) ? 'позвонить': 'написать';
            // Information to send
            const info = `Такой-то человек (${userName}, ${phoneNumber}) оставил заявку на получение консультации ${action}. Дата и время заявки: ${formattedDate} ${formattedTime}. Необходимо с ним связаться.`;
            client.sendMessage('7076344538@c.us', info); 
            postUserInteraction(userName, phoneNumber, action);

        }
        
        else {
            client.sendMessage(phoneNumber, 'Неизвестная комманда');
        }
        console.log(message.body);
    }
});

client.initialize();
