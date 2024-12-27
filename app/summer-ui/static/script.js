window.onload = function () {
    fetch(window.location.origin + "/news")
      .then((response) => response.json())
      .then((data) => {
        document.getElementById("loader").style.display = "none";
        document.getElementById("news-container").style.display = "block";
  
        const summaryElement = document.getElementById("summary");
        const imagesElement = document.getElementById("images");
  
        summaryElement.innerHTML = data.summary.split("\n").join("<br>");
  
        data.images.forEach((image, index) => {
          const img = document.createElement("img");
          img.className = "photo";
          img.src = image.url;
          img.alt = image.caption;
          img.style.width = "150px";
          img.style.height = "150px";
  
          if (index % 3 === 0) {
            img.style.gridColumnEnd = "span 2";
            img.style.gridRowEnd = "span 2";
          }
  
          imagesElement.appendChild(img);
        });
      })
      .catch((err) => console.error(err.message));
  
    function formatDate(date) {
      const options = {
        weekday: "long",
        month: "long",
        day: "numeric",
        year: "numeric",
      };
      return date.toLocaleDateString("en-US", options);
    }
  
    const today = new Date();
    document.getElementById("date").textContent = formatDate(today);
  };
  