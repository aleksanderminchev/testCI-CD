var carousel = document.querySelector('.carousel');
var cells = carousel.querySelectorAll('.carousel__cell');
var cellCount; // cellCount set from cells-range input value
var selectedIndex = 0;
var selectedImg = 0;
var cellWidth = carousel.offsetWidth;
var cellHeight = carousel.offsetHeight;
var isHorizontal = true;
var rotateFn = isHorizontal ? 'rotateY' : 'rotateX';
var radius, theta;
var img_id = 0;
var img_id_left = 14;
var img_id_left2 = 13;
var img_id_left3 = 12;
var imd_id_right = 1;
var imd_id_right2 = 2;
var imd_id_right3 = 3;
// var img_id_left4 = 11;
// var img_id_right4 = 4;

function rotateCarousel() {
    var angle = theta * selectedIndex * -1;
    carousel.style.transform = 'translateZ(' + -radius + 'px) ' + 
        rotateFn + '(' + angle + 'deg)';
}

var prevButton = document.querySelector('.previous-button');
    prevButton.addEventListener( 'click', function() {
    
    selectedIndex--;
    selectedImg--;


    if (selectedImg == -15) {
        selectedImg=0;
    }

    if (selectedImg < 0) {
        img_id = 15 - selectedImg * -1;
    }
    else {
        img_id = selectedImg;
    }

    img_id_left = img_id - 1;
    if (img_id_left < 0) {
        img_id_left = 14;
    }

    img_id_right = img_id + 1;
    if (img_id_right == 15) {
        img_id_right = 0;
    }

    img_id_left2 = img_id_left - 1;
    if (img_id_left2 == -1) {
        img_id_left2 = 14;
    }

    img_id_right2 = img_id_right + 1;
    if (img_id_right2 == 15) {
        img_id_right2 = 0;
    }

    img_id_left3 = img_id_left2 - 1;
    if (img_id_left3 == -1) {
        img_id_left3 = 14;
    }

    img_id_right3 = img_id_right2 + 1;
    if (img_id_right3 == 15) {
        img_id_right3 = 0;
    }
    
    $("#cell-" + img_id.toString()).removeClass("semi-active");
    $("#cell-" + img_id.toString()).addClass("active");

    $("#cell-" + img_id_left.toString()).removeClass("semi-inactive");
    $("#cell-" + img_id_left.toString()).addClass("semi-active");

    $("#cell-" + img_id_right.toString()).removeClass("active");
    $("#cell-" + img_id_right.toString()).addClass("semi-active");

    $("#cell-" + img_id_left2.toString()).removeClass("inactive");
    $("#cell-" + img_id_left2.toString()).addClass("semi-inactive");

    $("#cell-" + img_id_right2.toString()).removeClass("semi-active");
    $("#cell-" + img_id_right2.toString()).addClass("semi-inactive");

    $("#cell-" + img_id_left3.toString()).removeClass("semi-inactive");
    $("#cell-" + img_id_left3.toString()).addClass("inactive");

    $("#cell-" + img_id_right3.toString()).removeClass("semi-inactive");
    $("#cell-" + img_id_right3.toString()).addClass("inactive");

    rotateCarousel();
});

var nextButton = document.querySelector('.next-button');
    nextButton.addEventListener( 'click', function() {
    selectedIndex++;
    selectedImg++;

    if (selectedImg == 15) {
        selectedImg=0;
    }

    if (selectedImg < 0) {
        img_id = 15 - selectedImg * -1;
    }
    else {
        img_id = selectedImg;
    }
    img_id_left = img_id - 1;
    if (img_id_left < 0) {
        img_id_left = 14;
    }

    img_id_right = img_id + 1;
    if (img_id_right == 15) {
        img_id_right = 0;
    }

    img_id_left2 = img_id_left - 1;
    if (img_id_left2 == -1) {
        img_id_left2 = 14;
    }

    img_id_right2 = img_id_right + 1;
    if (img_id_right2 == 15) {
        img_id_right2 = 0;
    }

    img_id_left3 = img_id_left2 - 1;
    if (img_id_left3 == -1) {
        img_id_left3 = 14;
    }

    img_id_right3 = img_id_right2 + 1;
    if (img_id_right3 == 15) {
        img_id_right3 = 0;
    }


    $("#cell-" + img_id.toString()).removeClass("semi-active");
    $("#cell-" + img_id.toString()).addClass("active");

    $("#cell-" + img_id_right.toString()).removeClass("semi-inactive");
    $("#cell-" + img_id_right.toString()).addClass("semi-active");

    $("#cell-" + img_id_left.toString()).removeClass("active");
    $("#cell-" + img_id_left.toString()).addClass("semi-active");

    $("#cell-" + img_id_right2.toString()).removeClass("inactive");
    $("#cell-" + img_id_right2.toString()).addClass("semi-inactive");

    $("#cell-" + img_id_left2.toString()).removeClass("semi-active");
    $("#cell-" + img_id_left2.toString()).addClass("semi-inactive");

    $("#cell-" + img_id_right3.toString()).removeClass("semi-inactive");
    $("#cell-" + img_id_right3.toString()).addClass("inactive");

    $("#cell-" + img_id_left3.toString()).removeClass("semi-inactive");
    $("#cell-" + img_id_left3.toString()).addClass("inactive");


    rotateCarousel();
});



function changeCarousel() {
cellCount = 15;
theta = 360 / cellCount;
var cellSize = isHorizontal ? cellWidth : cellHeight;
radius = Math.round( ( cellSize / 2) / Math.tan( Math.PI / cellCount ) );
for ( var i=0; i < cells.length; i++ ) {
    var cell = cells[i];
    if ( i < cellCount ) {
    // visible cell
    // cell.style.opacity = 1;
    var cellAngle = theta * i;
    cell.style.transform = rotateFn + '(' + cellAngle + 'deg) translateZ(' + radius + 'px)';
    } else {
    // hidden cell
    // cell.style.opacity = 0;
    cell.style.transform = 'none';
    }
}

rotateCarousel();
};

// set initials
changeCarousel();