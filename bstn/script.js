/**
 * Here is our array of messages our 8ball will store!
 *  
 * FIXME: 
 * Add all the possible fortunes we can get
 * from the Magic 8-Ball! 
 */
const message = ["It is certain", "It is decidedly so", "Without a doubt", "Yes – definitely", "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes", "Don’t count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful", "Reply hazy, try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again","FIXME", "FIXME"];

/**
 * Returns a random eight ball message
 */
function getEightBallMessage() {
  // FIXME:
  // Make a variable messageSize which gets the length
  // of the array (or counts the amount of messages inside
  // of that array)
  let messageSize = message.lengh;

  console.log(messageSize)

  // FIXME:
  // Make a variable randomIndex, and set it to a random
  // number from 0 to the length of the array. 
  let randomIndex = Math.floor(Math.random()*messageSize)

  // FIXME:
  // Get the randomIndexth message from our array!
  // Let's call it fortuneStr.

  let fortuneStr = message[randomIndex]

  return fortuneStr;
}


/**
 * Takes an eightball message and places it inside
 * the ball
 */
function changeMessage() {

  // Use JavaScript to get the <div id="eight"> tag!
  const eightEl = document.getElementById('eight');

  // FIXME:
  // What do you think we can do to use JS to get
  // the <div id="answer"> tag? Name it answerEl.
  const answerEl = document.getElementById('answer')


  // This "clears" the eight ball message
  eightEl.textContent = '';

  // We want the 8Ball to pick a random fortune for us!

  // FIXME:
  // fill in the message with our fortune!
  answerEl.textContent = getEightBallMessage()

}

// Use JavaScript to get the <div id="button"> tag!
const buttonEl = document.getElementById('button');

// Tell our browser to make sure the message
// changes when we click on the "SHAKE" button.
// "When we click on the button, let's run the
// changeMessage function above!"
buttonEl.addEventListener('click', changeMessage);