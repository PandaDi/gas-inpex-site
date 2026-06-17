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
          bg: "url(images/hero-industrial.jpg) center/cover no-repeat",
        },
        {
          title: "Поставка газового оборудования",
          desc: "Широкий ассортимент промышленного и бытового газового оборудования от ведущих мировых производителей.",
          tag: "Оборудование",
          bg: "url(images/hero-supply.jpg) center/cover no-repeat",
        },
        {
          title: "Проектирование систем Умного дома",
          desc: "Комплексные решения автоматизации жилых помещений: климат-контроль, освещение, безопасность и мультимедиа.",
          tag: "Smart Home",
          bg: "url(images/hero-smarthome.jpg) center/cover no-repeat",
        },
        {
          title: "Гарантийное и сервисное обслуживание",
          desc: "Оперативное сервисное обслуживание, ремонт и техническая поддержка всего поставляемого оборудования.",
          tag: "Сервис",
          bg: "url(images/hero-service.jpg) center/cover no-repeat",
        },
      ],
      timer: null,
      init: function () {
        this.startTimer();
      },
      startTimer: function () {
        var self = this;
        this.timer = setInterval(function () {
          self.next();
        }, 3000);
      },
      next: function () {
        clearInterval(this.timer);
        this.current = (this.current + 1) % this.slides.length;
        this.startTimer();
      },
      prev: function () {
        clearInterval(this.timer);
        this.current =
          (this.current - 1 + this.slides.length) % this.slides.length;
        this.startTimer();
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