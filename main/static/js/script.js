function toggleFullscreen(imageURL) {
    var fullscreenElement = document.createElement("div");
    fullscreenElement.classList.add("fullscreen");

    var imgElement = document.createElement("img");
    imgElement.src = imageURL; // Use the URL passed from HTML

    fullscreenElement.appendChild(imgElement);
    document.body.appendChild(fullscreenElement);

    setTimeout(function() {
        fullscreenElement.remove();
    }, 5000); // 5 seconds
}

function playSound(soundId) {
    var audio = document.getElementById(soundId);
    audio.play();
}
