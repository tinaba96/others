/**
 * Here is our array of messages our 8ball will store!
 *  
 * Add all the possible fortunes we can get
 * from the Magic 8-Ball! 
 */
const messages = ["It is certain", "It is decidedly so", "Without a doubt", "Yes – definitely", "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes", "Don’t count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful", "Reply hazy, try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again"];

// build a function that
// gets a random message.
// I'll get that nth index inside of the
// array, and then i'll return it!

function getEightballMessage() {
  // To get the message,
  // Pick a random number between 1 and however
  // long that array is.
  let messagesSize = messages.length;
  let randomNumber = Math.floor(Math.random() * messagesSize);
  return messages[randomNumber];
}

// Somehow, we need to do the following:
function changeMessage() {
  // Somehow it should clear the eight ball message
  let eightEl = document.getElementById('eight');
  eightEl.textContent = '';

  // We want to get our getEightballMessage...
  let answerEl = document.getElementById('answer');

  // ...and put the message into the <p id="answer">.
  answerEl.textContent = getEightballMessage();
}

// We want a way to call changeMessage()
// when we click on the shake button!
let buttonEl = document.getElementById('button');
buttonEl.addEventListener('click', changeMessage);
