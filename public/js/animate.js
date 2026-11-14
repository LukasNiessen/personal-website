(() => {
  let observer;
  const motion = window.matchMedia("(prefers-reduced-motion: reduce)");

  function animate() {
    observer?.disconnect();
    document.querySelectorAll(".reveal-pending").forEach((element) => {
      element.classList.remove("reveal-pending");
    });
    if (motion.matches || !("IntersectionObserver" in window)) return;

    observer = new IntersectionObserver((entries) => {
      entries.forEach(({ target, isIntersecting }) => {
        if (isIntersecting) {
          target.classList.remove("reveal-pending");
          observer.unobserve(target);
        }
      });
    }, { rootMargin: "0px 0px 32px 0px" });

    document.querySelectorAll(".animate").forEach((element) => {
      // Above-the-fold content is immediately readable, including without JavaScript.
      if (element.getBoundingClientRect().top > window.innerHeight + 32) {
        element.classList.add("reveal-pending");
        observer.observe(element);
      }
    });
  }

  document.addEventListener("DOMContentLoaded", animate);
  document.addEventListener("astro:after-swap", animate);
  motion.addEventListener("change", animate);
})();
