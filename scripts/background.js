var images = ['balls.jpg', 'bridge.jpg', 'concert.jpg', 'jellyfish.jpg','museum.jpg', 'soccer.jpg', 'nightlife.jpg', 'stars.jpg'];

$('body').css({'background-image': 'url(images/' + images[Math.floor(Math.random() * images.length)] + ')'});


var table = document.getElementById("eventbriteTable");

// 1. get to right container
// 2. calculate how many events you have
// 3. use that to find dimnesions of table
// 4. go through that list and put them in the table
