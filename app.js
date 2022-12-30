let score = 0;

function updateScore(additionalScore) {
  score += additionalScore;
  $("#score").text(`SCORE: ${score}`);
}

function startTimer(time_remaining) {
  const timer = setInterval(()=>{
    time_remaining--;
    $("#timer").text(time_remaining);
    if (time_remaining == 0) {
      clearInterval(timer);
      stopGame();
    }
  }, 1000)
}

function stopGame() {
  $("#guess-submit-form").before("<div>Time's up!<div>");
  $("#guess-submit-form").remove();
  postScore();
}

function postScore() {
  axios.post("/high-score", data={score: score})
  .then(res => {
    console.log(res.data);
  })
}

$("document").ready(function(){

  updateScore(0);
  startTimer(60);

  $("#guess-submit-form").submit(function(e) {
    e.preventDefault();
    const guess = $("#guess-word")[0].value
    $("#guess-word")[0].value = ""
    axios.post("/guess", {
      guess: guess
    }).then((res) => {
      let message;
      switch (res.data.result) {
        case "ok":
          message = `${guess} is on the board!`;
          updateScore(guess.length)
          break;
        case "not-on-board":
          message = `${guess} is not on the board.`;
          break;
        case "not-word":
          message = `${guess} is not a word.`;
          break;
        case "repeat-guess":
          message = `You've already guessed ${guess}`;
          break;
        default:
          message = "Something went wrong."
      }
      $("#message-area").text(message);

    })
  })
})

