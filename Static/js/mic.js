const searchInput = document.getElementById('search');
const micButton = document.querySelector('.mic');

micButton.addEventListener('click', () => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (SpeechRecognition) {
    const recognition = new SpeechRecognition();

    recognition.onstart = () => {
      micButton.innerHTML = '<img src="/static/assets/wave_8109659.png" alt="">';
      console.log('Speech recognition started');
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      searchInput.value = transcript;
    };

    recognition.onerror = (event) => {
      console.log('Speech recognition error:', event.error);
    };

    recognition.onend = () => {
      micButton.innerHTML = '<span class="material-symbols-outlined">mic</span>';
    };

    recognition.start();
  } else {
    console.log('SpeechRecognition API is not supported in this browser.');
  }
});

const searchedInput = document.getElementById('searches');
const miecButton = document.querySelector('.miec');

miecButton.addEventListener('click', () => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (SpeechRecognition) {
    const recognition = new SpeechRecognition();

    recognition.onstart = () => {
      miecButton.innerHTML = '<img src="/static/assets/wave_8109659.png" alt="">';
      console.log('Speech recognition started');
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      searchedInput.value = transcript;
    };

    recognition.onerror = (event) => {
      console.log('Speech recognition error:', event.error);
    };

    recognition.onend = () => {
      miecButton.innerHTML = '<span class="material-symbols-outlined">mic</span>';
    };

    recognition.start();
  } else {
    console.log('SpeechRecognition API is not supported in this browser.');
  }
});