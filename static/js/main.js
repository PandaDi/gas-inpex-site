// ===== Scroll to Top Button + WhatsApp Form =====
document.addEventListener("DOMContentLoaded", function () {
  // Scroll to Top
  var scrollTopBtn = document.getElementById("scrollTopBtn");
  if (scrollTopBtn) {
    scrollTopBtn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
    window.addEventListener("scroll", function () {
      scrollTopBtn.style.display = window.scrollY > 400 ? "flex" : "none";
    });
  }

  // WhatsApp Contact Form (contacts.html)
  var contactForm = document.querySelector("form.contact-form");
  if (contactForm) {
    contactForm.addEventListener("submit", function (event) {
      event.preventDefault();
      var text =
        "Здравствуйте! Хочу оставить заявку на сайте Gas Inpex.\n\nИмя: " +
        this.name.value +
        "\nТелефон: " +
        this.phone.value +
        "\nEmail: " +
        (this.email.value || "не указан") +
        "\nСообщение: " +
        this.message.value;
      window.open(
        "https://wa.me/77213567890?text=" + encodeURIComponent(text),
        "_blank"
      );
    });
  }

  // Hero Slider — Vanilla JS
  initHeroSlider();
});

// ===== Hero Slider (Vanilla JS) =====
function initHeroSlider() {
  var section = document.getElementById("hero-slider-section");
  if (!section) return;

  var slides = section.querySelectorAll(".hero-slide");
  var dots = section.querySelectorAll(".hero-dot");
  var prevBtn = section.querySelector(".hero-prev");
  var nextBtn = section.querySelector(".hero-next");
  var current = 0;
  var timer = null;

  function showSlide(index) {
    slides.forEach(function (slide, i) {
      slide.classList.remove("hero-slide-active", "hero-slide-inactive");
      slide.classList.add(i === index ? "hero-slide-active" : "hero-slide-inactive");
    });
    dots.forEach(function (dot, i) {
      dot.classList.toggle("bg-red-brand", i === index);
      dot.classList.toggle("w-8", i === index);
      dot.classList.toggle("bg-white/40", i !== index);
      dot.classList.toggle("w-3", i !== index);
    });
    current = index;
  }

  function nextSlide() {
    showSlide((current + 1) % slides.length);
    restartTimer();
  }

  function prevSlide() {
    showSlide((current - 1 + slides.length) % slides.length);
    restartTimer();
  }

  function goToSlide(index) {
    showSlide(index);
    restartTimer();
  }

  function startTimer() {
    timer = setInterval(nextSlide, 5000);
  }

  function pauseTimer() {
    clearInterval(timer);
    timer = null;
  }

  function restartTimer() {
    clearInterval(timer);
    startTimer();
  }

  // Event bindings
  if (prevBtn) prevBtn.addEventListener("click", prevSlide);
  if (nextBtn) nextBtn.addEventListener("click", nextSlide);
  dots.forEach(function (dot) {
    dot.addEventListener("click", function () {
      goToSlide(parseInt(dot.dataset.slideIndex));
    });
  });
  section.addEventListener("mouseenter", pauseTimer);
  section.addEventListener("mouseleave", function () {
    if (!timer) startTimer();
  });

  startTimer();
}

// ===== Alpine.js Data Components =====
document.addEventListener("alpine:init", function () {
  // Counter
  Alpine.data("counter", function (target) {
    return {
      value: 0,
      display: 0,
      startCounter: function () {
        var self = this;
        this.value = 0;
        var step = Math.ceil(target / 80);
        var interval = setInterval(function () {
          self.value += step;
          if (self.value >= target) {
            self.value = target;
            clearInterval(interval);
          }
          self.display = self.value;
        }, 25);
      },
    };
  });
});
