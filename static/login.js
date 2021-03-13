
let message = document.getElementById('message').textContent;
message = message.replace(/\r?\n|\r/g,'');
message = message.replaceAll('                                                    ', '');
document.getElementById('message').textContent = message;