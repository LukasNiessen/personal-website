function generateThemeParticles(n, color) {
  let value = `${getRandom(2560)}px ${getRandom(2560)}px ${color}`;
  for (let i = 2; i <= n; i++) {
    value += `, ${getRandom(2560)}px ${getRandom(2560)}px ${color}`;
  }
  return value;
}

function getRandom(max) {
  return Math.floor(Math.random() * max);
}

function initBG() {
  // Get the current theme mode
  const isDarkMode = document.documentElement.classList.contains("dark");
  const particleColor = isDarkMode ? "#fff" : "#000";

  // Generate particles for both light and dark mode (same effect, different colors)
  const particlesSmall = generateThemeParticles(1000, particleColor);
  const particlesMedium = generateThemeParticles(500, particleColor);
  const particlesLarge = generateThemeParticles(250, particleColor);

  // First set of particles
  const particles1 = document.getElementById("particles1");
  const particles2 = document.getElementById("particles2");
  const particles3 = document.getElementById("particles3");

  if (particles1) {
    particles1.style.cssText = `
      width: 1px;
      height: 1px;
      border-radius: 50%;
      box-shadow: ${particlesSmall};
      animation: animateParticle 180s linear infinite;
      `;
  }

  if (particles2) {
    particles2.style.cssText = `
      width: 1.5px;
      height: 1.5px;
      border-radius: 50%;
      box-shadow: ${particlesMedium};
      animation: animateParticle 240s linear infinite;
      `;
  }

  if (particles3) {
    particles3.style.cssText = `
      width: 2px;
      height: 2px;
      border-radius: 50%;
      box-shadow: ${particlesLarge};
      animation: animateParticle 300s linear infinite;
      `;
  }

  // Second set of particles (same animation, just slightly offset)
  const moreParticlesSmall = generateThemeParticles(1000, particleColor);
  const moreParticlesMedium = generateThemeParticles(500, particleColor);
  const moreParticlesLarge = generateThemeParticles(250, particleColor);

  const stars1 = document.getElementById("stars1");
  const stars2 = document.getElementById("stars2");
  const stars3 = document.getElementById("stars3");

  if (stars1) {
    stars1.style.cssText = `
      width: 1px;
      height: 1px;
      border-radius: 50%;
      box-shadow: ${moreParticlesSmall};
      animation: animateParticle 210s linear infinite;
      `;
  }

  if (stars2) {
    stars2.style.cssText = `
      width: 1.5px;
      height: 1.5px;
      border-radius: 50%;
      box-shadow: ${moreParticlesMedium};
      animation: animateParticle 270s linear infinite;
      `;
  }

  if (stars3) {
    stars3.style.cssText = `
      width: 2px;
      height: 2px;
      border-radius: 50%;
      box-shadow: ${moreParticlesLarge};
      animation: animateParticle 330s linear infinite;
      `;
  }
}

// Initialize background on page load and theme toggle
document.addEventListener("astro:after-swap", initBG);
document.addEventListener("DOMContentLoaded", initBG);

// Listen for theme changes
document.addEventListener("astro:theme-change", initBG);

// Special manual theme change detection as a fallback
const observer = new MutationObserver(function (mutations) {
  mutations.forEach(function (mutation) {
    if (
      mutation.attributeName === "class" &&
      (mutation.target.classList.contains("dark") ||
        !mutation.target.classList.contains("dark"))
    ) {
      initBG();
    }
  });
});

// Start observing the document with the configured parameters
observer.observe(document.documentElement, { attributes: true });

// Initial initialization
initBG();
