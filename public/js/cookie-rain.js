function createCookieEmoji() {
  const cookie = document.createElement("div");
  cookie.innerHTML = "🍪";
  cookie.style.position = "fixed";
  cookie.style.left = Math.random() * 100 + "vw";
  cookie.style.top = "-20px";
  cookie.style.fontSize = Math.random() * 20 + 20 + "px";
  cookie.style.transform = "rotate(" + Math.random() * 360 + "deg)";
  cookie.style.opacity = "0.8";
  cookie.style.zIndex = "9999";
  cookie.style.pointerEvents = "none";
  cookie.classList.add("falling-cookie");

  document.body.appendChild(cookie);

  const duration = Math.random() * 3 + 3;
  cookie.style.animation = `fallCookie ${duration}s linear forwards`;

  setTimeout(() => {
    cookie.remove();
  }, duration * 1000);
}

function startCookieRain() {
  const interval = setInterval(() => {
    for (let i = 0; i < 3; i++) {
      createCookieEmoji();
    }
  }, 200);

  return interval;
}

let cookieRainInterval = null;

function initCookieRain() {
  const cookieHint = document.getElementById("cookie-hint");
  if (!cookieHint) return;

  cookieHint.addEventListener("mouseenter", () => {
    if (!cookieRainInterval) {
      cookieRainInterval = startCookieRain();
    }
  });

  cookieHint.addEventListener("mouseleave", () => {
    if (cookieRainInterval) {
      clearInterval(cookieRainInterval);
      cookieRainInterval = null;
    }
  });
}

document.addEventListener("astro:after-swap", initCookieRain);
document.addEventListener("DOMContentLoaded", initCookieRain);
