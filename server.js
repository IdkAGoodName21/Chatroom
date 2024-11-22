const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const XLSX = require('xlsx');

const app = express();
app.use(bodyParser.json());

const FILE_PATH = './data.xlsx';

function loadWorkbook() {
  if (!fs.existsSync(FILE_PATH)) {
    const workbook = XLSX.utils.book_new();
    workbook.SheetNames.push('Users', 'Messages');
    XLSX.utils.book_append_sheet(workbook, XLSX.utils.aoa_to_sheet([['Username', 'Email', 'Password', 'Room ID']]), 'Users');
    XLSX.utils.book_append_sheet(workbook, XLSX.utils.aoa_to_sheet([['Room ID', 'Sender', 'Message', 'Timestamp']]), 'Messages');
    XLSX.writeFile(workbook, FILE_PATH);
  }
  return XLSX.readFile(FILE_PATH);
}

function saveWorkbook(workbook) {
  XLSX.writeFile(workbook, FILE_PATH);
}

app.post('/save-user', (req, res) => {
  const { username, email, password, roomId } = req.body;
  const workbook = loadWorkbook();
  const sheet = workbook.Sheets['Users'];
  const data = XLSX.utils.sheet_to_json(sheet, { header: 1 });

  data.push([username, email, password, roomId]);
  workbook.Sheets['Users'] = XLSX.utils.aoa_to_sheet(data);
  saveWorkbook(workbook);

  res.send('User saved successfully');
});

app.post('/save-message', (req, res) => {
  const { roomId, sender, message } = req.body;
  const workbook = loadWorkbook();
  const sheet = workbook.Sheets['Messages'];
  const data = XLSX.utils.sheet_to_json(sheet, { header: 1 });

  data.push([roomId, sender, message, new Date().toISOString()]);
  workbook.Sheets['Messages'] = XLSX.utils.aoa_to_sheet(data);
  saveWorkbook(workbook);

  res.send('Message saved successfully');
});

app.listen(3000, () => console.log('Server running on port 3000'));

