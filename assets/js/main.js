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
}
