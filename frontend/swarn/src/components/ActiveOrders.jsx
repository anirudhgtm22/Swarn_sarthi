// import React, { useState, useEffect } from 'react';
// import { Link as RouterLink } from 'react-router-dom';
// import Table from '@mui/material/Table';
// import TableBody from '@mui/material/TableBody';
// import TableCell from '@mui/material/TableCell';
// import TableHead from '@mui/material/TableHead';
// import TableRow from '@mui/material/TableRow';
// import Typography from '@mui/material/Typography';
// import Button from '@mui/material/Button';
// import { makeStyles } from '@mui/styles';

// const useStyles = makeStyles({
//   root: {
//     margin: '20px auto', // Center the component and add space from top and bottom
//     maxWidth: 800, // Set maximum width for the component
//   },
//   table: {
//     minWidth: 650,
//   },
//   tableHeader: {
//     fontWeight: 'bold',
//     fontSize: '1.1rem',
//   },
//   tableRow: {
//     '&:nth-of-type(odd)': {
//       backgroundColor: '#f3f3f3',
//     },
//   },
//   title: {
//     textAlign: 'center', // Center the heading
//     marginBottom: 20, // Add space below the heading
//     fontFamily: 'Arial, sans-serif', // Change the font family
//     fontSize: '1.5rem', // Adjust the font size
//   },
// });

// const ActiveOrders = () => {
//   const classes = useStyles();
//   const [orders, setOrders] = useState([]);

//   useEffect(() => {
//     const fetchOrders = async () => {
//       try {
//         const response = await fetch('http://127.0.0.1:8000/api/active-orders/');
//         if (!response.ok) {
//           throw new Error('Failed to fetch data');
//         }
//         const data = await response.json();
//         setOrders(data);
//       } catch (error) {
//         console.error('Error fetching active orders:', error);
//       }
//     };

//     fetchOrders();
//   }, []);

//   return (
//     <div className={classes.root}>
//       <Typography variant="h5" className={classes.title}>
//         Active Orders
//       </Typography>
//       <Table className={classes.table}>
//         <TableHead>
//           <TableRow>
//             <TableCell className={classes.tableHeader}>Service</TableCell>
//             <TableCell className={classes.tableHeader}>Amount</TableCell>
//             <TableCell className={classes.tableHeader}>Elderly's Name</TableCell>
//             <TableCell className={classes.tableHeader}>Actions</TableCell>
//           </TableRow>
//         </TableHead>
//         <TableBody>
//           {orders.map(order => (
//             <TableRow key={order.id} className={classes.tableRow}>
//               <TableCell>{order.order.service.title}</TableCell>
//               <TableCell>{order.order.amount}</TableCell>
//               <TableCell>{order.elderly.user.first_name} {order.elderly.user.last_name}</TableCell>
//               <TableCell>
//                 <Button component={RouterLink} to={`/order/${order.id}`} variant="outlined">
//                   View Details
//                 </Button>
//               </TableCell>
//             </TableRow>
//           ))}
//         </TableBody>
//       </Table>
//     </div>
//   );
// }

// export default ActiveOrders;

// import React, { useState, useEffect } from 'react';
// import { Link as RouterLink } from 'react-router-dom';
// import Table from '@mui/material/Table';
// import TableBody from '@mui/material/TableBody';
// import TableCell from '@mui/material/TableCell';
// import TableHead from '@mui/material/TableHead';
// import TableRow from '@mui/material/TableRow';
// import Typography from '@mui/material/Typography';
// import Button from '@mui/material/Button';
// import Modal from '@mui/material/Modal';
// import Box from '@mui/material/Box';
// import { makeStyles } from '@mui/styles';

// const useStyles = makeStyles({
//   root: {
//     margin: '20px auto',
//     maxWidth: 800,
//   },
//   table: {
//     minWidth: 650,
//   },
//   tableHeader: {
//     fontWeight: 'bold',
//     fontSize: '1.1rem',
//   },
//   tableRow: {
//     '&:nth-of-type(odd)': {
//       backgroundColor: '#f3f3f3',
//     },
//   },
//   title: {
//     textAlign: 'center',
//     marginBottom: 20,
//     fontFamily: 'Arial, sans-serif',
//     fontSize: '1.5rem',
//   },
//   modalContent: {
//     position: 'absolute',
//     width: 400,
//     backgroundColor: 'white',
//     border: '2px solid #000',
//     boxShadow: 24,
//     p: 4,
//     top: '50%',
//     left: '50%',
//     transform: 'translate(-50%, -50%)',
//   },
// });

// const ActiveOrders = () => {
//   const classes = useStyles();
//   const [orders, setOrders] = useState([]);
//   const [selectedOrder, setSelectedOrder] = useState(null);

//   useEffect(() => {
//     const fetchOrders = async () => {
//       try {
//         const response = await fetch('http://127.0.0.1:8000/api/active-orders/');
//         if (!response.ok) {
//           throw new Error('Failed to fetch data');
//         }
//         const data = await response.json();
//         setOrders(data);
//       } catch (error) {
//         console.error('Error fetching active orders:', error);
//       }
//     };

//     fetchOrders();
//   }, []);

//   const handleViewDetails = (order) => {
//     setSelectedOrder(order);
//   };

//   const handleCloseModal = () => {
//     setSelectedOrder(null);
//   };

//   return (
//     <div className={classes.root}>
//       <Typography variant="h5" className={classes.title}>
//         Active Orders
//       </Typography>
//       <Table className={classes.table}>
//         <TableHead>
//           <TableRow>
//             <TableCell className={classes.tableHeader}>Service</TableCell>
//             <TableCell className={classes.tableHeader}>Amount</TableCell>
//             <TableCell className={classes.tableHeader}>Elderly's Name</TableCell>
//             <TableCell className={classes.tableHeader}>Actions</TableCell>
//           </TableRow>
//         </TableHead>
//         <TableBody>
//           {orders.map(order => (
//             <TableRow key={order.id} className={classes.tableRow}>
//               <TableCell>{order.order.service.title}</TableCell>
//               <TableCell>{order.order.amount}</TableCell>
//               <TableCell>{order.elderly.user.first_name} {order.elderly.user.last_name}</TableCell>
//               <TableCell>
//                 <Button onClick={() => handleViewDetails(order)} variant="outlined">
//                   View Details
//                 </Button>
//               </TableCell>
//             </TableRow>
//           ))}
//         </TableBody>
//       </Table>
//       <Modal open={Boolean(selectedOrder)} onClose={handleCloseModal}>
//         <Box className={classes.modalContent}>
//           {selectedOrder && (
//             <>
//               <Typography variant="h6">{`Order ID: ${selectedOrder.id}`}</Typography>
//               <Typography variant="body1">{`Service: ${selectedOrder.order.service.title}`}</Typography>
//               <Typography variant="body1">{`Amount: ${selectedOrder.order.amount}`}</Typography>
//               <Typography variant="body1">{`Elderly's Name: ${selectedOrder.elderly.user.first_name} ${selectedOrder.elderly.user.last_name}`}</Typography>
//               {/* Add other order details here */}
//             </>
//           )}
//         </Box>
//       </Modal>
//     </div>
//   );
// }

// export default ActiveOrders;
// uppar walla working 

// import React, { useState, useEffect } from 'react';
// import { Link as RouterLink } from 'react-router-dom';
// import Table from '@mui/material/Table';
// import TableBody from '@mui/material/TableBody';
// import TableCell from '@mui/material/TableCell';
// import TableHead from '@mui/material/TableHead';
// import TableRow from '@mui/material/TableRow';
// import Typography from '@mui/material/Typography';
// import Button from '@mui/material/Button';
// import Modal from '@mui/material/Modal';
// import Box from '@mui/material/Box';
// import Grid from '@mui/material/Grid';
// import Divider from '@mui/material/Divider';
// import IconButton from '@mui/material/IconButton';
// import CloseIcon from '@mui/icons-material/Close';

// const ActiveOrders = () => {
//   const [orders, setOrders] = useState([]);
//   const [selectedOrder, setSelectedOrder] = useState(null);

//   useEffect(() => {
//     const fetchOrders = async () => {
//       try {
//         const response = await fetch('http://127.0.0.1:8000/api/active-orders/');
//         if (!response.ok) {
//           throw new Error('Failed to fetch data');
//         }
//         const data = await response.json();
//         setOrders(data);
//       } catch (error) {
//         console.error('Error fetching active orders:', error);
//       }
//     };

//     fetchOrders();
//   }, []);

//   const handleViewDetails = (order) => {
//     setSelectedOrder(order);
//   };

//   const handleCloseModal = () => {
//     setSelectedOrder(null);
//   };

//   return (
//     <div style={{ margin: '20px auto', maxWidth: 800 }}>
//       <Typography variant="h5" style={{ textAlign: 'center', marginBottom: 20 }}>
//         Active Orders
//       </Typography>
//       <Table style={{ minWidth: 650 }}>
//         <TableHead>
//           <TableRow>
//             <TableCell style={{ fontWeight: 'bold' }}>Service</TableCell>
//             <TableCell style={{ fontWeight: 'bold' }}>Amount</TableCell>
//             <TableCell style={{ fontWeight: 'bold' }}>Address</TableCell>
//             <TableCell style={{ fontWeight: 'bold' }}>Actions</TableCell>
//           </TableRow>
//         </TableHead>
//         <TableBody>
//           {orders.map(order => (
//             <TableRow key={order.id}>
//               <TableCell>{order.order.service.title}</TableCell>
//               <TableCell>{order.order.amount}</TableCell>
//               <TableCell>{`${order.elderly.user.address}-${order.elderly.user.state}`}</TableCell>
//               <TableCell>
//                 <Button onClick={() => handleViewDetails(order)} variant="outlined">
//                   View Details
//                 </Button>
//               </TableCell>
//             </TableRow>
//           ))}
//         </TableBody>
//       </Table>
//       <Modal open={Boolean(selectedOrder)} onClose={handleCloseModal}>
//         <Box style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', backgroundColor: 'white', boxShadow: 'rgba(0, 0, 0, 0.24) 0px 3px 8px', padding: 24, borderRadius: 8, minWidth: 400, width: '70%', maxWidth: 800 }}>
//           {selectedOrder && (
//             <>
//               <Grid container alignItems="center" style={{ marginBottom: 16 }}>
//                 <Grid item>
//                   <Typography variant="h6">{`Order ID: ${selectedOrder.id}`}</Typography>
//                 </Grid>
//                 <Grid item>
//                   <IconButton onClick={handleCloseModal}>
//                     <CloseIcon />
//                   </IconButton>
//                 </Grid>
//               </Grid>
//               <Divider style={{ marginBottom: 16 }} />
//               <Typography variant="body1">{`Service: ${selectedOrder.order.service.title}`}</Typography>
//               <Typography variant="body1">{`Amount: ${selectedOrder.order.amount}`}</Typography>
//               <Typography variant="body1">{`Address: ${selectedOrder.elderly.user.address}-${selectedOrder.elderly.user.state}`}</Typography>
//               {/* Add other order details here */}
//               <Button onClick={handleCloseModal} color="primary" variant="contained" style={{ marginTop: 20 }} fullWidth>
//                 Accept Request
//               </Button>
//             </>
//           )}
//         </Box>
//       </Modal>
//     </div>
//   );
// }

// export default ActiveOrders;


// import React, { useState, useEffect } from 'react';
// import { Typography, Table, TableHead, TableBody, TableRow, TableCell, Button, Modal, Box, Grid, Divider, IconButton } from '@mui/material';
// import CloseIcon from '@mui/icons-material/Close';
// import Cookies from 'js-cookie';

// const OrderDetailsModal = ({ selectedOrder, onClose, onAcceptRequest }) => {
//   return (
//     <Box style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', backgroundColor: 'white', boxShadow: 'rgba(0, 0, 0, 0.24) 0px 3px 8px', padding: 24, borderRadius: 8, minWidth: 400, width: '70%', maxWidth: 800 }}>
//       <Grid container alignItems="center" style={{ marginBottom: 16 }}>
//         <Grid item>
//           <Typography variant="h6">{`Order ID: ${selectedOrder.id}`}</Typography>
//         </Grid>
//         <Grid item>
//           <IconButton onClick={onClose}>
//             <CloseIcon />
//           </IconButton>
//         </Grid>
//       </Grid>
//       <Divider style={{ marginBottom: 16 }} />
//       <Typography variant="body1">{`Service: ${selectedOrder.order.service.title}`}</Typography>
//       <Typography variant="body1">{`Amount: ${selectedOrder.order.amount}`}</Typography>
//       <Typography variant="body1">{`Elderly's Name: ${selectedOrder.elderly.user.first_name} ${selectedOrder.elderly.user.last_name}`}</Typography>
//       <Typography variant="body1">{`Order Date: ${selectedOrder.order.order_date}`}</Typography>
//       <Typography variant="body1">{`Completed At: ${selectedOrder.order.completed_at || 'Not Completed'}`}</Typography>
//       {/* Add other order details here */}
//       <Button onClick={onAcceptRequest} color="primary" variant="contained" style={{ marginTop: 20 }} fullWidth>
//         Accept Request
//       </Button>
//     </Box>
//   );
// };

// function parseAndFormatDate(dateString) {
//     // Parse the date string with timezone information
//     const parsedDate = new Date(dateString);

//     // Format the date and time in a user-friendly way
//     const options = {
//       weekday: 'long',
//       year: 'numeric',
//       month: 'long',
//       day: 'numeric',
//       hour: 'numeric',
//       minute: '2-digit',
//       timeZone: 'UTC', // To display in UTC (adjust if needed)
//     };

//     return parsedDate.toLocaleDateString('en-US', options); // US English locale for formatting

//   } 

// const ActiveOrders = () => {
//   const [orders, setOrders] = useState([]);
//   const [selectedOrder, setSelectedOrder] = useState(null);

//   useEffect(() => {
//     const fetchOrders = async () => {
//       try {
//         const response = await fetch('http://127.0.0.1:8000/api/active-orders/');
//         if (!response.ok) {
//           throw new Error('Failed to fetch data');
//         }
//         const data = await response.json();
//         setOrders(data);
//       } catch (error) {
//         console.error('Error fetching active orders:', error);
//       }
//     };

//     fetchOrders();
//   }, []);

//   const handleViewDetails = (order) => {
//     setSelectedOrder(order);
//   };

//   const handleCloseModal = () => {
//     setSelectedOrder(null);
//     handleCloseModal();
//   };

//   const handleAcceptRequest = async () => {
//     try {
//       const token = Cookies.get('token'); // Replace 'your_cookie_name' with the actual cookie name
//       if (!token) {
//         throw new Error('Token not found in cookies');
//       }
  
//       const response = await fetch('http://127.0.0.1:8000/accept-orders/', {
//         method: 'PATCH',
//         headers: {
//           'Content-Type': 'application/json',
//           Authorization: `Bearer ${token}`,
//         },
//         body: JSON.stringify({
//           status: 'volunteer_assigned'
//         })
//       });
//       if (!response.ok) {
//         throw new Error('Failed to accept request');
//       }
//       handleCloseModal(); // Close modal after accepting request
//     } catch (error) {
//       console.error('Error accepting request:', error);
//     }
//   };

//   return (
//     <div style={{ margin: '20px auto', maxWidth: 900 }}>
//       <Typography variant="h5" style={{ textAlign: 'center', marginBottom: 20 }}>
//         Active Orders
//       </Typography>
//       <Table style={{ minWidth: 650 }}>
//         <TableHead>
//           <TableRow>
//             <TableCell style={{ fontWeight: 'bold' }}>Service</TableCell>
//             <TableCell style={{ fontWeight: 'bold' }}>Amount</TableCell>
//             <TableCell style={{ fontWeight: 'bold' }}>Address</TableCell>
//             <TableCell style={{ fontWeight: 'bold' }}>Order-Date</TableCell>
//             <TableCell style={{ fontWeight: 'bold' }}>Actions</TableCell>
//           </TableRow>
//         </TableHead>
//         <TableBody>
//           {orders.map(order => (
//             <TableRow key={order.id}>
//               <TableCell>{order.order.service.title}</TableCell>
//               <TableCell>{order.order.amount}</TableCell>
//               <TableCell>{`${order.elderly.user.address}-${order.elderly.user.state}`}</TableCell>
//               <TableCell>
//                 {parseAndFormatDate(order.order.orderDate)}
//               </TableCell>
//               <TableCell>
//                 <Button onClick={() => handleViewDetails(order)} variant="outlined">
//                   View Details
//                 </Button>
//               </TableCell>
//             </TableRow>
//           ))}
//         </TableBody>
//       </Table>
//       <Modal open={Boolean(selectedOrder)} onClose={handleCloseModal}>
//         <OrderDetailsModal selectedOrder={selectedOrder} onClose={handleCloseModal} onAcceptRequest={handleAcceptRequest} />
//       </Modal>
//     </div>
//   );
// }

// export default ActiveOrders;


// import React, { useState, useEffect } from 'react';
// import { Typography, Table, TableHead, TableBody, TableRow, TableCell, Button, Modal, Box, Grid, Divider, IconButton } from '@mui/material';
// import CloseIcon from '@mui/icons-material/Close';
// import Cookies from 'js-cookie';

// const OrderDetailsModal = ({ selectedOrder, onClose, onAcceptRequest }) => {
//   return (
//     <Box style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', backgroundColor: 'white', boxShadow: 'rgba(0, 0, 0, 0.24) 0px 3px 8px', padding: 24, borderRadius: 8, minWidth: 400, width: '70%', maxWidth: 800 }}>
//       <Grid container alignItems="center" style={{ marginBottom: 16 }}>
//         <Grid item>
//           <Typography variant="h6">{`Order ID: ${selectedOrder.id}`}</Typography>
//         </Grid>
//         <Grid item>
//           <IconButton onClick={onClose}>
//             <CloseIcon />
//           </IconButton>
//         </Grid>
//       </Grid>
//       <Divider style={{ marginBottom: 16 }} />
//       <Typography variant="body1">{`Service: ${selectedOrder.order.service.title}`}</Typography>
//       <Typography variant="body1">{`Amount: ${selectedOrder.order.amount}`}</Typography>
//       <Typography variant="body1">{`Elderly's Name: ${selectedOrder.elderly.user.first_name} ${selectedOrder.elderly.user.last_name}`}</Typography>
//       <Typography variant="body1">{`Order Date: ${selectedOrder.order.order_date}`}</Typography>
//       <Typography variant="body1">{`Completed At: ${selectedOrder.order.completed_at || 'Not Completed'}`}</Typography>
//       {/* Add other order details here */}
//       <Button onClick={() => onAcceptRequest(selectedOrder.id)} color="primary" variant="contained" style={{ marginTop: 20 }} fullWidth>
//         Accept Request
//       </Button>
//     </Box>
//   );
// };

// function parseAndFormatDate(dateString) {
//     // Parse the date string with timezone information
//     const parsedDate = new Date(dateString);

//     // Format the date and time in a user-friendly way
//     const options = {
//       weekday: 'long',
//       year: 'numeric',
//       month: 'long',
//       day: 'numeric',
//       hour: 'numeric',
//       minute: '2-digit',
//       timeZone: 'UTC', // To display in UTC (adjust if needed)
//     };

//     return parsedDate.toLocaleDateString('en-US', options); // US English locale for formatting

//   } 

// const ActiveOrders = () => {
//   const [orders, setOrders] = useState([]);
//   const [selectedOrder, setSelectedOrder] = useState(null);

//   useEffect(() => {
//     const fetchOrders = async () => {
//       try {
//         const response = await fetch('http://127.0.0.1:8000/api/active-orders/');
//         if (!response.ok) {
//           throw new Error('Failed to fetch data');
//         }
//         const data = await response.json();
//         setOrders(data);
//       } catch (error) {
//         console.error('Error fetching active orders:', error);
//       }
//     };

//     fetchOrders();
//   }, []);

//   const handleViewDetails = (order) => {
//     setSelectedOrder(order);
//   };

//   const handleCloseModal = () => {
//     setSelectedOrder(null);
//   };

//   const handleAcceptRequest = async (orderId) => {
//     try {
//       const token = Cookies.get('token');
//       if (!token) {
//         throw new Error('Token not found in cookies');
//       }
  
//       const response = await fetch(`http://127.0.0.1:8000/accept-orders/${orderId}/`, {
//         method: 'PATCH',
//         headers: {
//           'Content-Type': 'application/json',
//           Authorization: `Bearer ${token}`,
//         },
//         body: JSON.stringify({
//           status: 'volunteer_assigned'
//         })
//       });
  
//       if (!response.ok) {
//         throw new Error('Failed to accept request');
//       }
  
//       window.alert('Request accepted successfully');
//       handleCloseModal();
//     } catch (error) {
//       console.error('Error accepting request:', error);
//       window.alert('Failed to accept request');
//     }
//   };
  

//   return (
//     <div style={{ margin: '20px auto', maxWidth: 900 }}>
//       <Typography variant="h5" style={{ textAlign: 'center', marginBottom: 20 }}>
//         Active Orders
//       </Typography>
//       <Table style={{ minWidth: 650 }}>
//         <TableHead>
//           <TableRow>
//             <TableCell style={{ fontWeight: 'bold' }}>Service</TableCell>
//             <TableCell style={{ fontWeight: 'bold' }}>Amount</TableCell>
//             <TableCell style={{ fontWeight: 'bold' }}>Address</TableCell>
//             <TableCell style={{ fontWeight: 'bold' }}>Order-Date</TableCell>
//             <TableCell style={{ fontWeight: 'bold' }}>Actions</TableCell>
//           </TableRow>
//         </TableHead>
//         <TableBody>
//           {orders.map(order => (
//             <TableRow key={order.id}>
//               <TableCell>{order.order.service.title}</TableCell>
//               <TableCell>{order.order.amount}</TableCell>
//               <TableCell>{`${order.elderly.user.address}-${order.elderly.user.state}`}</TableCell>
//               <TableCell>
//                 {parseAndFormatDate(order.order.orderDate)}
//               </TableCell>
//               <TableCell>
//                 <Button onClick={() => handleViewDetails(order)} variant="outlined">
//                   View Details
//                 </Button>
//               </TableCell>
//             </TableRow>
//           ))}
//         </TableBody>
//       </Table>
//       <Modal open={Boolean(selectedOrder)} onClose={handleCloseModal}>
//         <OrderDetailsModal selectedOrder={selectedOrder} onClose={handleCloseModal} onAcceptRequest={handleAcceptRequest} />
//       </Modal>
//     </div>
//   );
// }

// export default ActiveOrders;


import React, { useState, useEffect } from 'react';
import { Typography, Table, TableHead, TableBody, TableRow, TableCell, Button, Modal, Box, Grid, Divider, IconButton ,TextField} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import Cookies from 'js-cookie';

const OrderDetailsModal = ({ selectedOrder, handleClose, onAcceptRequest }) => {
  return (
    <Modal open={true} onClose={handleClose}>
      <Box style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', backgroundColor: 'white', boxShadow: 'rgba(0, 0, 0, 0.24) 0px 3px 8px', padding: 24, borderRadius: 8, minWidth: 400, width: '70%', maxWidth: 800 }}>
        <IconButton style={{ position: 'absolute', top: 10, right: 10 }} onClick={handleClose}>
          <CloseIcon />
        </IconButton>
        <Grid container alignItems="center" style={{ marginBottom: 16 }}>
          <Grid item>
            <Typography variant="h6">{`Order ID: ${selectedOrder.id}`}</Typography>
          </Grid>
        </Grid>
        <Divider style={{ marginBottom: 16 }} />
        <TextField label="Service" value={selectedOrder.service.title} fullWidth disabled sx={{ marginBottom: 2 }} />
        <TextField label="Amount" value={selectedOrder.amount} fullWidth disabled sx={{ marginBottom: 2 }} />
        <TextField label="Elderly's Name" value={`${selectedOrder.elderly.user.first_name} ${selectedOrder.elderly.user.last_name}`} fullWidth disabled sx={{ marginBottom: 2 }} />
        <TextField label="Order Date" value={parseAndFormatDate(selectedOrder.order_date)} fullWidth disabled sx={{ marginBottom: 2 }} />
        <TextField label="Completed At" value={selectedOrder.completed_at || 'Not Completed'} fullWidth disabled sx={{ marginBottom: 2 }} />

        {/* Add other order details here */}
        <Button onClick={() => onAcceptRequest(selectedOrder.id)} color="primary" variant="contained" style={{ marginTop: 20 }} fullWidth>
          Accept Request
        </Button>
      </Box>
    </Modal>
  );
};

function parseAndFormatDate(dateString) {
    // Parse the date string with timezone information
    const parsedDate = new Date(dateString);

    // Format the date and time in a user-friendly way
    const options = {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      timeZone: 'UTC', // To display in UTC (adjust if needed)
    };

    return parsedDate.toLocaleDateString('en-US', options); // US English locale for formatting
  } 

const ActiveOrders = () => {
  const [orders, setOrders] = useState([]);
  const [selectedOrder, setSelectedOrder] = useState(null);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/active-orders/');
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        const data = await response.json();
        setOrders(data);
      } catch (error) {
        console.error('Error fetching active orders:', error);
      }
    };

    fetchOrders();
  }, []);

  const handleViewDetails = (order) => {
    setSelectedOrder(order);
  };

  const handleCloseModal = () => {
    setSelectedOrder(null);
  };

  const handleAcceptRequest = async (orderId) => {
    try {
      const token = Cookies.get('token');
      if (!token) {
        throw new Error('Token not found in cookies');
      }
  
      const response = await fetch(`http://127.0.0.1:8000/accept-orders/${orderId}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          status: 'volunteer_assigned'
        })
      });
      if (response.status === 450) {
        window.alert('Please complete your profile first');
        return;
      }
      if (!response.ok) {
        throw new Error('Failed to accept request');
      }
  
      window.alert('Request accepted successfully');
      handleCloseModal();
      // Reload the page
      window.location.reload();
    } catch (error) {
      console.error('Error accepting request:', error);
      window.alert('Failed to accept request');
    }
  };

  return (
    <div style={{ margin: '20px auto', maxWidth: 900 }}>
      <Typography variant="h5" style={{ textAlign: 'center', marginBottom: 20 }}>
        Active Orders
      </Typography>
      {orders.length === 0 ? (
        <Typography variant="body1" style={{ textAlign: 'center' }}>
          No active orders
        </Typography>
      ) : (
        <Table style={{ minWidth: 650 }}>
          <TableHead>
            <TableRow>
              <TableCell style={{ fontWeight: 'bold' }}>Service</TableCell>
              <TableCell style={{ fontWeight: 'bold' }}>Amount</TableCell>
              <TableCell style={{ fontWeight: 'bold' }}>Address</TableCell>
              <TableCell style={{ fontWeight: 'bold' }}>Order-Date</TableCell>
              <TableCell style={{ fontWeight: 'bold' }}>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {orders.map(order => (
              <TableRow key={order.id}>
                <TableCell>{order.service.title}</TableCell>
                <TableCell>{order.amount}</TableCell>
                <TableCell>{`${order.elderly.user.address}-${order.elderly.user.state}`}</TableCell>
                <TableCell>
                  {parseAndFormatDate(order.order_date)}
                </TableCell>
                <TableCell>
                  <Button onClick={() => handleViewDetails(order)} variant="outlined">
                    View Details
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
     <Modal open={Boolean(selectedOrder)} onClose={handleCloseModal}>
        <OrderDetailsModal selectedOrder={selectedOrder} handleClose={handleCloseModal} onAcceptRequest={handleAcceptRequest} />
      </Modal>

    </div>
  );
}

export default ActiveOrders;
