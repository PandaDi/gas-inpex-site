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
});

// ===== Alpine.js Data Components =====
document.addEventListener("alpine:init", function () {
  // Hero Slider
  Alpine.data("heroSlider", function () {
    return {
      current: 0,
      slides: [
        {
          title: "Инжиниринг и Автоматизация",
          desc: "Проектирование и внедрение систем автоматизации технологических процессов (АСУ ТП) для промышленных объектов любой сложности.",
          tag: "АСУ ТП",
          bg: "url(static/images/hero-industrial.webp) center/cover no-repeat",
        },
        {
          title: "Поставка газового оборудования",
          desc: "Широкий ассортимент промышленного и бытового газового оборудования от ведущих мировых производителей.",
          tag: "Оборудование",
          bg: "url(static/images/hero-supply.webp) center/cover no-repeat",
        },
        {
          title: "Проектирование систем Умного дома",
          desc: "Комплексные решения автоматизации жилых помещений: климат-контроль, освещение, безопасность и мультимедиа.",
          tag: "Smart Home",
          bg: "url(static/images/hero-smarthome.webp) center/cover no-repeat",
        },
        {
          title: "Гарантийное и сервисное обслуживание",
          desc: "Оперативное сервисное обслуживание, ремонт и техническая поддержка всего поставляемого оборудования.",
          tag: "Сервис",
          bg: "url(static/images/hero-service.webp) center/cover no-repeat",
        },
      ],
      timer: null,
      autoInterval: 5000,

      init: function () {
        this.startAutoTimer();
      },
      startAutoTimer: function () {
        var self = this;
        this.timer = setInterval(function () {
          self.next();
        }, this.autoInterval);
      },
      next: function () {
        this.current = (this.current + 1) % this.slides.length;
      },
      prev: function () {
        this.current =
          (this.current - 1 + this.slides.length) % this.slides.length;
      },
      nextSlide: function () {
        this.next();
        this.restartTimer();
      },
      prevSlide: function () {
        this.prev();
        this.restartTimer();
      },
      goToSlide: function (index) {
        this.current = index;
        this.restartTimer();
      },
      restartTimer: function () {
        clearInterval(this.timer);
        this.startAutoTimer();
      },
      pauseTimer: function () {
        clearInterval(this.timer);
      },
      resumeTimer: function () {
        this.startAutoTimer();
      },
    };
  });

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