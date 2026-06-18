// FontAwesome → local SVG sprite loader
// Replaces <i class="fas fa-xxx"> with inline SVG <use> elements
(function() {
  // Sprite URL (relative to page)
  var spriteUrl = 'static/images/fa-sprite.svg';
  
  // Find all FA icon elements
  var icons = document.querySelectorAll('i[class*="fa-"]');
  for (var i = 0; i < icons.length; i++) {
    var el = icons[i];
    var cls = el.className || '';
    var match = cls.match(/fa-([a-zA-Z0-9-]+)/);
    if (!match) continue;
    
    var iconName = match[1];
    // Skip size/utility modifiers
    if (['ul', 'li', 'stack', 'fw', 'lg', '2x', '3x', '4x', '5x'].indexOf(iconName) >= 0) continue;
    
    // Create SVG element
    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('class', cls + ' fa-svg');
    svg.setAttribute('width', '1em');
    svg.setAttribute('height', '1em');
    svg.setAttribute('fill', 'currentColor');
    svg.setAttribute('aria-hidden', 'true');
    
    var use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
    use.setAttribute('href', spriteUrl + '#fa-' + iconName);
    svg.appendChild(use);
    
    // Replace <i> with <svg>
    el.parentNode.replaceChild(svg, el);
  }
})();