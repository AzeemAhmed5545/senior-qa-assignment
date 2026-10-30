// Quantity field improvement - product details page (automationexercise.com/product_details/<id>)
// Paste into the DevTools console on any product page. Nothing on the server is changed.
//
// 1. Connects the visible "Quantity:" label to the input (accessible name).
// 2. Checks the quantity before "Add to cart". Whole numbers from 1 upwards are allowed.
//    Anything else is blocked, the field is marked invalid and a message is shown.
// 3. Valid quantities are passed through to the site's own add-to-cart code unchanged.

(function () {
  var qty = document.getElementById('quantity');
  var addBtn = document.querySelector('.product-information button.cart');
  if (!qty || !addBtn) {
    console.warn('Quantity improvement: not a product details page, nothing changed.');
    return;
  }

  // 1. Label
  var label = qty.parentNode.querySelector('label');
  if (label && !label.htmlFor) {
    label.htmlFor = 'quantity';
  }

  // Error message, linked to the input so screen readers read it with the field
  var error = document.getElementById('quantity-error');
  if (!error) {
    error = document.createElement('p');
    error.id = 'quantity-error';
    error.setAttribute('role', 'alert');
    error.style.cssText = 'color:#c0392b;font-size:14px;margin:8px 0 0;';
    error.hidden = true;
    addBtn.insertAdjacentElement('afterend', error);
  }
  qty.setAttribute('aria-describedby', 'quantity-error');

  function isValid(value) {
    return /^\d+$/.test(value) && Number(value) >= 1;
  }

  function showError() {
    error.textContent = 'Enter a quantity of 1 or more.';
    error.hidden = false;
    qty.setAttribute('aria-invalid', 'true');
    qty.focus();
  }

  function clearError() {
    error.hidden = true;
    error.textContent = '';
    qty.removeAttribute('aria-invalid');
  }

  // 2. Runs in the capture phase, before the site's jQuery click handler in cart.js.
  // Stopping the event here means the add_to_cart request is never sent.
  document.addEventListener('click', function (e) {
    if (!addBtn.contains(e.target)) return;
    if (!isValid(qty.value.trim())) {
      e.stopPropagation();
      e.preventDefault();
      showError();
    } else {
      clearError();
    }
  }, true);

  qty.addEventListener('input', function () {
    if (isValid(qty.value.trim())) clearError();
  });

  console.log('Quantity improvement applied.');
})();
