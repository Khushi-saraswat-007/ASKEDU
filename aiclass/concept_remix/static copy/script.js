let utterance;

function speakOutput(format = "plain") {
  if (utterance && speechSynthesis.speaking) {
    speechSynthesis.cancel();
  }

  const text = document.querySelector(".output pre").innerText;
  utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-US";

  switch (format) {
    case "poem":
      utterance.rate = 0.9;
      utterance.pitch = 1.4;
      break;
    case "song":
      utterance.rate = 1.2;
      utterance.pitch = 1.6;
      break;
    case "comic":
      utterance.rate = 1.1;
      utterance.pitch = 1.3;
      break;
    case "meme":
      utterance.rate = 1.4;
      utterance.pitch = 1.2;
      break;
    default:
      utterance.rate = 1.0;
      utterance.pitch = 1.0;
  }

  speechSynthesis.speak(utterance);
}

function stopSpeaking() {
  if (speechSynthesis.speaking) {
    speechSynthesis.cancel();
  }
}

function copyToClipboard() {
  const text = document.querySelector(".output pre").innerText;
  navigator.clipboard.writeText(text).then(() => {
    alert("Copied to clipboard!");
  });
}
window.speechSynthesis.onvoiceschanged = () => {
  const voices = speechSynthesis.getVoices();
  console.log("Available voices:", voices);
};
