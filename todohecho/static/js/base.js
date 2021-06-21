// Navbar Burger

    var burger = document.querySelector('.burger');
    var nav = document.querySelector('#'+burger.dataset.target);

    burger.addEventListener('click', function(){
      burger.classList.toggle('is-active');
      nav.classList.toggle('is-active');
    });

  // Index - Fade in animation 

  preload = document.getElementById("preload")
  const remove = function() {
    preload.classList.toggle("preload");
  };
  remove(preload)

  const fade1 = document.getElementById("fade-1")
  const fade2 = document.getElementById("fade-2")
  const fade3 = document.getElementById("fade-3")
  const fade4 = document.getElementById("fade-4")
  const fade_1 = function(fade1) {
    fade1.classList.toggle("fade");
    
  }
  

  const fadeout = function(fadeitem) {
    fadeitem.classList.toggle("fade-out");
  }

  // let complete = document.querySelector('.complete')

  // complete.addEventListener('click', function(){
  //   complete.classList.toggle('fade-out');
  // })
