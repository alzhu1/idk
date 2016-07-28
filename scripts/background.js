var images = ['balls.jpg', 'bridge.jpg', 'concert.jpg', 'jellyfish.jpg','museum.jpg', 'soccer.jpg', 'nightlife.jpg', 'stars.jpg'];

$('body').css({'background-image': 'url(images/' + images[Math.floor(Math.random() * images.length)] + ')'});
