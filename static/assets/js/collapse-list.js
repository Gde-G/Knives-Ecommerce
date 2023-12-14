$(document).ready(function() {
  // Handle the click event on any button with the class 'collapse-btn'
  $('.collapse-btn').on('click', function() {
    // Get the parent 'li' element of the clicked button
    const parentLi = $(this).closest('.list-group-item');

    // Get the target 'ul' element to collapse/expand based on the data-bs-target attribute of the parent 'li'
    const targetSelector = parentLi.data('bs-target');
    const targetList = $(targetSelector);

    // Toggle the collapse state of the target 'ul' element
    targetList.collapse('toggle');

    const chevronDown = parentLi.find('.fa-circle-chevron-down');
    const chevronUp = parentLi.find('.fa-circle-chevron-up');
    chevronDown.toggleClass('d-none');
    chevronUp.toggleClass('d-block');
  });
});