// import React, { useState, useEffect } from 'react';
// import Slider from 'react-slick';
// import 'slick-carousel/slick/slick.css';
// import 'slick-carousel/slick/slick-theme.css';
// import { IconButton } from '@material-ui/core';
// import { ArrowBack, ArrowForward } from '@material-ui/icons';
// import Image from './Image.jpg'; 

// function CarouselComp() {
//   const [index, setIndex] = useState(0);

//   // Function to move to the next slide
//   const nextSlide = () => {
//     setIndex((prevIndex) => (prevIndex + 1) % 3); // Assuming there are 3 slides
//   };

//   // Function to move to the previous slide
//   const prevSlide = () => {
//     setIndex((prevIndex) => (prevIndex - 1 + 3) % 3); // Assuming there are 3 slides
//   };

//   // Use useEffect to start the interval when the component mounts
//   useEffect(() => {  
//     const interval = setInterval(() => {
//       nextSlide();   
//     }, 3000); // Change slide every 3 seconds

//     // Clear the interval when the component unmounts
//     return () => clearInterval(interval);
//   }, []);

//   const settings = {
//     dots: true,
//     infinite: true,
//     speed: 500,
//     slidesToShow: 1,
//     slidesToScroll: 1,
//     autoplay: true,
//     autoplaySpeed: 3000,
//     afterChange: (current) => setIndex(current)
//   };

//   return (
//     <div className="carousel-wrapper" style={{ position: 'relative', overflow: 'hidden' }}>
//       <Slider {...settings} className="carousel">
//         <div style={{ height: '100%', width: '100%' }}>
//           <img src={Image} alt="First slide" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
//           <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', color: '#fff' }}>
//             <h3>First slide label</h3>
//             <p>Nulla vitae elit libero, a pharetra augue mollis interdum.</p>
//           </div>
//         </div>
//         <div style={{ height: '100%', width: '100%' }}>
//           <img src={Image} alt="Second slide" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
//           <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', color: '#fff' }}>
//             <h3>Second slide label</h3>
//             <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
//           </div>
//         </div>
//         <div style={{ height: '100%', width: '100%' }}>
//           <img src={Image} alt="Third slide" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
//           <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', color: '#fff' }}>
//             <h3>Third slide label</h3>
//             <p>Praesent commodo cursus magna, vel scelerisque nisl consectetur.</p>
//           </div>
//         </div>
//       </Slider>
//       <IconButton className="prev" style={{ position: 'absolute', top: '50%', left: 0, transform: 'translateY(-50%)', backgroundColor: 'rgba(255, 255, 255, 0.5)' }} onClick={prevSlide}>
//         <ArrowBack style={{ color: '#fff' }} />
//       </IconButton>
//       <IconButton className="next" style={{ position: 'absolute', top: '50%', right: 0, transform: 'translateY(-50%)', backgroundColor: 'rgba(255, 255, 255, 0.5)' }} onClick={nextSlide}>
//         <ArrowForward style={{ color: '#fff' }} />
//       </IconButton>
//     </div>
//   );
// }

// export default CarouselComp;

// import React, { useState, useEffect } from 'react';
// import Slider from 'react-slick';
// import 'slick-carousel/slick/slick.css';
// import 'slick-carousel/slick/slick-theme.css';
// import { IconButton } from '@material-ui/core';
// import { ArrowBack, ArrowForward } from '@material-ui/icons';
// import Image from './Image.jpg'; 

// function CarouselComp() {
//   const [index, setIndex] = useState(0);

//   // Function to move to the next slide
//   const nextSlide = () => {
//     setIndex((prevIndex) => (prevIndex + 1) % 3); // Assuming there are 3 slides
//   };

//   // Function to move to the previous slide
//   const prevSlide = () => {
//     setIndex((prevIndex) => (prevIndex - 1 + 3) % 3); // Assuming there are 3 slides
//   };

//   // Use useEffect to start the interval when the component mounts
//   useEffect(() => {  
//     const interval = setInterval(() => {
//       nextSlide();   
//     }, 2000); // Change slide every 2 seconds

//     // Clear the interval when the component unmounts
//     return () => clearInterval(interval);
//   }, []);

//   const settings = {
//     dots: false,
//     infinite: true,
//     speed: 500,
//     slidesToShow: 1,
//     slidesToScroll: 1,
//     autoplay: false,
//     autoplaySpeed: 2000,
//     afterChange: (current) => setIndex(current)
//   };

//   return (
//     <div className="carousel-wrapper" style={{ position: 'relative', overflow: 'hidden' }}>
//       <Slider {...settings} className="carousel">
//         {/* Slide 1 */}
//         <div style={{ height: '100%', width: '100%', position: 'relative' }}>
//           <img src={Image} alt="First slide" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
//           <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: '#fff', textAlign: 'center' }}>
//             <h3>First slide label</h3>
//             <p>Nulla vitae elit libero, a pharetra augue mollis interdum.</p>
//           </div>
//         </div>

//         {/* Slide 2 */}
//         <div style={{ height: '100%', width: '100%', position: 'relative' }}>
//           <img src={Image} alt="Second slide" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
//           <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: '#fff', textAlign: 'center' }}>
//             <h3>Second slide label</h3>
//             <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
//           </div>
//         </div>

//         {/* Slide 3 */}
//         <div style={{ height: '100%', width: '100%', position: 'relative' }}>
//           <img src={Image} alt="Third slide" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
//           <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: '#fff', textAlign: 'center' }}>
//             <h3>Third slide label</h3>
//             <p>Praesent commodo cursus magna, vel scelerisque nisl consectetur.</p>
//           </div>
//         </div>
//       </Slider>

//       {/* Previous Slide Button */}
//       <IconButton className="prev" style={{ position: 'absolute', top: '50%', left: 0, transform: 'translateY(-50%)', zIndex: 1 }} onClick={prevSlide}>
//         <ArrowBack style={{ color: '#fff' }} />
//       </IconButton>

//       {/* Next Slide Button */}
//       <IconButton className="next" style={{ position: 'absolute', top: '50%', right: 0, transform: 'translateY(-50%)', zIndex: 1 }} onClick={nextSlide}>
//         <ArrowForward style={{ color: '#fff' }} />
//       </IconButton>
//     </div>
//   );
// }

// export default CarouselComp;

// import React, { useState, useEffect } from 'react';
// import Slider from 'react-slick';
// import 'slick-carousel/slick/slick.css';
// import 'slick-carousel/slick/slick-theme.css';
// import { IconButton } from '@material-ui/core';
// import { ArrowBack, ArrowForward } from '@material-ui/icons';
// import Image from './Image.jpg'; 

// function CarouselComp() {
//   const [index, setIndex] = useState(0);

//   // Function to move to the next slide
//   const nextSlide = () => {
//     setIndex((prevIndex) => (prevIndex + 1) % 3); // Assuming there are 3 slides
//   };

//   // Function to move to the previous slide
//   const prevSlide = () => {
//     setIndex((prevIndex) => (prevIndex - 1 + 3) % 3); // Assuming there are 3 slides
//   };

//   useEffect(() => {
//     const interval = setInterval(() => {
//       nextSlide();   
//     }, 2000); // Change slide every 2 seconds

//     return () => clearInterval(interval);
//   }, []);

//   const settings = {
//     dots: false,
//     infinite: true,
//     speed: 500,
//     slidesToShow: 1,
//     slidesToScroll: 1,
//     autoplay: true,
//     autoplaySpeed: 2000,
//     afterChange: (current) => setIndex(current)
//   };

//   return (
//     <div className="carousel-wrapper" style={{ position: 'relative', overflow: 'hidden' }}>
//       <Slider {...settings} className="carousel" beforeChange={(oldIndex, newIndex) => setIndex(newIndex)}>
//         <div>
//           <img src={Image} alt="First slide" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
//         </div>
//         <div>
//           <img src={Image} alt="Second slide" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
//         </div>
//         <div>
//           <img src={Image} alt="Third slide" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
//         </div>
//       </Slider>
//       <IconButton className="prev" style={{ position: 'absolute', top: '50%', left: 0, transform: 'translateY(-50%)', zIndex: 1 }} onClick={prevSlide}>
//         <ArrowBack style={{ color: '#fff' }} />
//       </IconButton>
//       <IconButton className="next" style={{ position: 'absolute', top: '50%', right: 0, transform: 'translateY(-50%)', zIndex: 1 }} onClick={nextSlide}>
//         <ArrowForward style={{ color: '#fff' }} />
//       </IconButton>
//     </div>
//   );
// }

// export default CarouselComp;
import React, { useState, useEffect } from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import Image from './Image.jpg'; 

function CarouselComp() {
  const [index, setIndex] = useState(0);

  // Use useEffect to start the interval when the component mounts
  useEffect(() => {  
    const interval = setInterval(() => {
      setIndex((prevIndex) => (prevIndex + 1) % 3); // Assuming there are 3 slides
    }, 2000); // Change slide every 2 seconds

    // Clear the interval when the component unmounts
    return () => clearInterval(interval);
  }, []);

  const settings = {
    dots: false,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 2000,
    afterChange: (current) => setIndex(current)
  };

  const carouselStyle = {
    height: '75vh', // 3/4 of the viewport height
    overflow: 'hidden',
    position: 'relative'
  };

  const imageContainerStyle = {
    width: '100%',
    height: '100%',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'flex-end' // Align the image to the bottom
  };

  const imageStyle = {
    width: '100%',
    objectFit: 'contain' // Fit the image inside
  };

  return (
    <div className="carousel-wrapper" style={carouselStyle}>
      <Slider {...settings} className="carousel">
        <div style={imageContainerStyle}>
          <img src={Image} alt="First slide" style={imageStyle} />
        </div>
        <div style={imageContainerStyle}>
          <img src={Image} alt="Second slide" style={imageStyle} />
        </div>
        <div style={imageContainerStyle}>
          <img src={Image} alt="Third slide" style={imageStyle} />
        </div>
      </Slider>
    </div>
  );
}

export default CarouselComp;
