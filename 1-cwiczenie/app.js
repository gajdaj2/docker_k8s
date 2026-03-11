const http = require("http");

const server = http.createServer((req, res) => {
  res.end("Hello from Docker!");
});

server.listen(3000, () => {
  console.log("Serwer działa na porcie 3000");
});
