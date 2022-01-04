$(function() {
  $(".drop_items .empty").droppable({
    drop: function(event, ui) {
      var dropped = ui.draggable;
      var droppedOn = $(this);
      $(this).addClass("c-drop-target--correct").droppable("disable");
      dropped.detach().css({
        top: 0,
        left: 0
      }).appendTo(droppedOn).draggable("disable");
    }
  });

  $(".drag_items .fill").draggable({
    revert: "invalid"
  });
});

function transValue() {
  //const arr = Array(8).fill().map(() => Array(8).fill(0));
  let arr = Array(8).fill().map(() => Array(8));
  var div = document.getElementsByClassName('drop_items');
  var divs = div[0].getElementsByTagName('div');
  for (var i = 0; i < divs.length; i += 1) {

    if (divs[i].getElementsByClassName("fill")[0]){
      console.log(divs[i].getElementsByClassName("fill")[0].className);
      var locationid = divs[i].id;
      var locationidint = parseInt(locationid);
      var mappingid;
      var valueid = divs[i].getElementsByClassName('fill')[0].className;
      const classes = valueid.split(' ');
      valueid = classes[1];
      switch(valueid) {
        case "wking":
          mappingid = -6;
          break;

        case "wqueen":
          mappingid = -5;
          break;

        case "wrook":
          mappingid = -4;
          break;
        case "wbishop":
          mappingid = -3;
          break;  

        case "wknight":
          mappingid = -2;
          break;  

        case "wpawn":
          mappingid = -1;
          break;  
          
        case "bking":
          mappingid = 6;
          break;

        case "bqueen":
          mappingid = 5;
          break;

        case "brook":
          mappingid = 4;
          break;

        case "bbishop":
          mappingid = 3;
          break;  
  
        case "bknight":
          mappingid = 2;
          break;  
  
        case "bpawn":
          mappingid = 1;
          break;  

        default:
          mappingid = 0;
      }
      
      var y = Math.trunc(locationidint/10) - 1;
      var x = (locationidint % 10) - 1;
      arr[y][x] = mappingid;
      
    }
  }
  console.log(arr);
  var boardout = document.getElementById("boardoutput");
  var boardoutval = boardout.value;
  console.log(boardoutval);
  document.getElementById("boardoutput").value = arr;
  document.getElementById("confirmation").submit();
  //postData(arr);
}

/*function postData(inarr) {
  $.ajax({
      type: "POST",
      url: "/result",
      contentType: "application/json",
      data: JSON.stringify(inarr),
      dataType: "json",
      success: function (response) {
          console.log(response);
      },
      error: function (err) {
          console.log(err);
      }
  })
}*/
// dropdown menu
const menuButton = document.querySelector('.fa-bars')
const menu = document.querySelector('.dropdown')
const menuLink = document.querySelectorAll('.dropLink')

menuButton.addEventListener('click', function () {
  menuButton.classList.toggle('fa-times');
  menu.classList.toggle('is-active');
})

menuLink.forEach(function(element) {
  console.log('test')
  element.addEventListener('click', goAway);
})

function goAway() {
  menu.classList.toggle('is-active')
  menuButton.classList.toggle('fa-times');
}

// countdown 
const countdown = () => {
  const countDate = new Date('Oct 26, 2021 13:00:00').getTime();
  const now = new Date().getTime();
  const gap = countDate - now;

  const second = 1000;
  const minute = second * 60;
  const hour = minute * 60;
  const day = hour * 24;

  const textDay = Math.floor(gap / day);
  const textHour = Math.floor((gap % day) / hour);
  const textMinute = Math.floor((gap % hour) / minute);
  const textSecond = Math.floor((gap % minute) / second);
  
  document.querySelector(".day").innerText = textDay;
  document.querySelector(".hour").innerText = textHour;
  document.querySelector(".minute").innerText = textMinute;
  document.querySelector(".second").innerText = textSecond;

  if (gap < 100) {
    const textSecond = 0;
    const textMinute = 0;
    const textHour = 0;
    const textDay = 0;

    document.querySelector(".day").innerText = textDay;
    document.querySelector(".hour").innerText = textHour;
    document.querySelector(".minute").innerText = textMinute;
    document.querySelector(".second").innerText = textSecond;
  }
}

// setInterval(countdown, 1000);


// smooth scroll
$(function() {
  $('a').smoothScroll();
});
