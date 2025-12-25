        // Image sources for the popup slideshow
        const images = [
            'image1.jpg', 'image2.jpg', 'image3.jpg',
            'image4.jpg', 'image5.jpg', 'image6.jpg'
          ];
  
          let currentIndex = 0;
        
    
          function openPopup(index) {
            currentIndex = index;
            document.getElementById('popupImage').src = images[currentIndex];
            document.getElementById('popupOverlay').style.display = 'flex';
          }
        
   
          function closePopup() {
            document.getElementById('popupOverlay').style.display = 'none';
          }

          function changeSlide(direction) {
            currentIndex = (currentIndex + direction + images.length) % images.length;
            document.getElementById('popupImage').src = images[currentIndex];
          }


          document.addEventListener("DOMContentLoaded", function() {
            const questions = document.querySelectorAll(".question");
            questions.forEach(question => {
                question.addEventListener("click", function() {
                    const answer = this.nextElementSibling;
                    answer.style.display = answer.style.display === "none" ? "block" : "none";
                });
            });
        });

      function openPopup_1() {
          document.getElementsByClassName("servicePopup").style.display = 'flex';
      }
  
      function closePopup_1() {
          document.getElementsByClassName("servicePopup").style.display = "none";
      }
  
