-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 10, 2024 at 11:11 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO"; -- field will not be auto-incremented
START TRANSACTION;
SET time_zone = "+00:00";


-- ? Database: `car_showroom`

/*
Contains:
- Table Structures
- Table Data
- Indexes
- Constraints
*/

-- --------------------------------------------------------

-- ? Table structures

-- Table structure for table `appointment`
CREATE TABLE `appointment` (
  `app_ID` varchar(20) NOT NULL,
  `Date` date NOT NULL,
  `Time` varchar(5) NOT NULL,
  `handling_emp_id` int(11) NOT NULL,
  `booking_cust_id` varchar(40) NOT NULL,
  `Appointment_for_car_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table `appointment`
INSERT INTO `appointment` (`app_ID`, `Date`, `Time`, `handling_emp_id`, `booking_cust_id`, `Appointment_for_car_id`) VALUES
('hard_314', '2024-03-14', '07:33', 1003, 'hardik pawar_5660_8319', 3),
('ian _121', '2024-03-21', '19:33', 1003, 'ian s tauro_4879_5954', 1),
('ian _414', '2024-03-14', '02:40', 1003, 'ian s tauro_4879_5954', 4),
('kara_222', '2024-03-22', '08:24', 1003, 'karan_1384_1419', 2);

-- --------------------------------------------------------

-- Table structure for table `car_features`
CREATE TABLE `car_features` (
  `car_ID` int(11) NOT NULL,
  `car_name` varchar(20) NOT NULL,
  `image_link` varchar(100) NOT NULL,
  `price` int(10) NOT NULL,
  `type` varchar(20) NOT NULL,
  `make` varchar(10) NOT NULL,
  `model` varchar(10) NOT NULL,
  `first_registration` varchar(10) NOT NULL,
  `mileage` int(5) NOT NULL,
  `fuel` varchar(10) NOT NULL,
  `engine_size` int(5) NOT NULL,
  `power` int(4) NOT NULL,
  `gearbox` varchar(10) NOT NULL,
  `no_of_seats` int(1) NOT NULL,
  `doors` int(1) NOT NULL,
  `color` varchar(10) NOT NULL,
  `Description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table `car_features`
INSERT INTO `car_features` (`car_ID`, `car_name`, `image_link`, `price`, `type`, `make`, `model`, `first_registration`, `mileage`, `fuel`, `engine_size`, `power`, `gearbox`, `no_of_seats`, `doors`, `color`, `Description`) VALUES
(1, 'Tesla Cybertruck', 'https://i.ibb.co/9yxzQSk/cybertruck.jpg', 51, 'Electric', 'None', 'Base Model', 'Unregister', 550, 'Electric', 1496, 600, 'Auto', 6, 4, 'Slip Grey', 'Buckle up, because the future of trucks is here with the Tesla Cybertruck! This isn\'t your ordinary pickup. It\'s a head-turning, all-electric powerhouse built with cold-rolled stainless steel for superior durability and a bold, futuristic design.\r\n\r\nHere\'s a glimpse of what awaits you:\r\n\r\nUnmatched Performance: Experience exhilarating acceleration and instant torque, leaving gas-powered trucks in the dust. Choose from a range of battery options offering up to 545 km (340 miles) of estimated range, perfect for conquering any journey.\r\n\r\nBuilt to Last: The Cybertruck\'s exoskeleton is crafted from ultra-strong stainless steel, making it dent-resistant and virtually indestructible.\r\n\r\nCyber-age Interior: Slide behind the yoke steering wheel and enter a spacious, minimalist cabin with a focus on functionality. The centerpiece is a massive 18.5-inch touchscreen controlling most vehicle functions, while a rear touchscreen keeps backseat passengers entertained.\r\n\r\nUltimate Utility: With a towing capacity of over 6.3 tonnes and a lockable vault for secure storage, the Cybertruck is your ultimate companion for work and play.\r\n\r\nThe Tesla Cybertruck is more than just a truck; it\'s a statement. It\'s a symbol of innovation and a commitment to a sustainable future.'),
(2, 'Range Rover', 'https://i.ibb.co/5jXtp2z/rangerover.jpg', 235, 'Hybrid', '2024', 'SV', '01/2024', 14, 'Petrol', 2997, 394, 'Automatic', 7, 4, 'black', 'Dominate the road in refined luxury. The Range Rover SV offers two distinct styles: timeless elegance or a dynamic presence. Inside, the SV Signature Suite pampers with individual rear seats, a hidden Club Table, and exquisite details. Choose from powerful PHEV or other engines, and conquer any terrain in unparalleled comfort. Experience luxury redefined. Contact me today.'),
(3, 'Toyota Supra', 'https://i.ibb.co/mNjkzh1/supra.jpg', 85, 'B58', '2023', 'MK3', 'Unregister', 13, 'Petrol', 1998, 382, 'Manual', 2, 2, 'black', 'Unleash your inner legend with the Toyota GR Supra. This iconic sports car delivers exhilarating performance with a 382-hp engine and sharp handling. Choose an automatic or a thrilling 6-speed manual transmission. The driver-focused interior features a head-up display and an 8.8-inch touchscreen. Turn heads and conquer corners. Supra: Go beyond.'),
(4, 'MINI Cooper JCW', 'https://i.ibb.co/Sdg0T41/cooper.jpg', 48, 'Combustion', '2020', 'JCW', '7/2020', 17, 'Petrol', 1998, 306, 'Automatic', 4, 4, 'Red and Bl', 'Embrace the legend with the iconic Mini Cooper. This playful hatchback, bursting with personality, offers exhilarating performance with a peppy engine and go-kart-like handling. Choose from a vibrant color palette to express yourself, and enjoy a surprisingly spacious interior that blends style with practicality. Experience the joy of driving, redefined.');

-- --------------------------------------------------------

-- Table structure for table `car_ownership`
CREATE TABLE `car_ownership` (
  `owner_cust_id` varchar(40) NOT NULL,
  `owned_car_id` int(11) NOT NULL,
  `emp_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table `car_ownership`
INSERT INTO `car_ownership` (`owner_cust_id`, `owned_car_id`, `emp_ID`) VALUES
('hardik pawar_5660_8319', 1, 1004),
('ian s tauro_4879_5954', 1, 1004),
('ian s tauro_4879_5954', 2, 1002),
('ian s tauro_4879_5954', 3, 1001),
('karan_1384_1419', 1, 2001),
('karan_1384_1419', 3, 1002);

-- --------------------------------------------------------

-- Table structure for table `customer`
CREATE TABLE `customer` (
  `customer_ID` varchar(40) NOT NULL,
  `Name` varchar(25) NOT NULL,
  `Age` int(3) NOT NULL,
  `Phone` int(10) NOT NULL,
  `Email` varchar(40) NOT NULL,
  `Registration_Date` date NOT NULL,
  `Password` varchar(20) NOT NULL,
  `Encrypted_Password` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table `customer`
INSERT INTO `customer` (`customer_ID`, `Name`, `Age`, `Phone`, `Email`, `Registration_Date`, `Password`, `Encrypted_Password`) VALUES
('hardik pawar_5660_8319', 'Hardik Pawar', 19, 2147483647, 'hardikhp.cs21@rvce.edu.in', '2024-02-28', 'wakuwaku8989', 'NA'),
('harshit_1401_2313', 'Harshit', 20, 2147483647, 'harshit@gmail.com', '2024-03-10', 'qwerty111', 'NA'),
('ian s tauro_4879_5954', 'Ian S Tauro', 19, 2147483647, 'iantauro.cs21@nie.edu.in', '2024-02-28', 'qwerty101', 'NA'),
('karan_1384_1419', 'Karan', 19, 2147483647, 'karan.sathish980@gmail.com', '2024-02-28', 'Imbatman#', 'NA');

-- --------------------------------------------------------

-- Table structure for table `department`
CREATE TABLE `department` (
  `dept_ID` int(11) NOT NULL,
  `Name` varchar(25) NOT NULL,
  `manager_emp_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table `department`
INSERT INTO `department` (`dept_ID`, `Name`, `manager_emp_id`) VALUES
(1, 'Sales', 1001),
(2, 'Finance', 2001),
(3, 'Management', 3001);

-- --------------------------------------------------------

-- Table structure for table `employee`
CREATE TABLE `employee` (
  `emp_ID` int(11) NOT NULL,
  `Name` varchar(25) NOT NULL,
  `Age` int(3) NOT NULL,
  `Gender` varchar(11) NOT NULL,
  `Salary` int(15) NOT NULL,
  `works_for_dept_id` int(11) NOT NULL,
  `password` varchar(20) NOT NULL,
  `Encrypted_Password` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table `employee`
INSERT INTO `employee` (`emp_ID`, `Name`, `Age`, `Gender`, `Salary`, `works_for_dept_id`, `password`, `Encrypted_Password`) VALUES
(1001, 'Rohit Sharma', 37, 'Male', 100000, 1, 'rs37', 'NA'),
(1002, 'Robert Kiyosaki', 76, 'Male', 2000000, 1, 'rk76', 'NA'),
(1003, 'Warren Buffett', 67, 'Male', 3400000, 1, 'wb67', 'NA'),
(1004, 'Avanti Nagral', 27, 'Female', 1600000, 1, 'an27', 'NA'),
(2001, 'Virat Kohli', 36, 'Male', 1300000, 2, 'vk36', 'NA'),
(3001, 'Smriti Mandhana', 27, 'Female', 900000, 3, 'sm27', 'NA');

-- --------------------------------------------------------

-- Table structure for table `review`
CREATE TABLE `review` (
  `review_ID` varchar(20) NOT NULL,
  `Star_rating` int(1) NOT NULL,
  `User_review` text NOT NULL,
  `review_cust_id` varchar(40) NOT NULL,
  `assessed_car_id` int(11) NOT NULL,
  `for_emp_ID` int(11) NOT NULL,
  `sentiment` varchar(20),
  `sentiment_score` int(11),
  `summarized_review` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table `review`
INSERT INTO `review` (`review_ID`, `Star_rating`, `User_review`, `review_cust_id`, `assessed_car_id`, `for_emp_ID`) VALUES
('amaz_10_3_ng_1710080', 10, 'amazing', 'karan_1384_1419', 3, 1004),
('grea_9_3_at_17100813', 9, 'great', 'karan_1384_1419', 3, 1004),
('outs_10_3_te_1710094', 10, 'outstanding mate', 'harshit_1401_2313', 3, 1004);

-- --------------------------------------------------------

-- Table structure for table `sale`
CREATE TABLE `sale` (
  `sale_ID` varchar(20) NOT NULL,
  `sale_date` date NOT NULL,
  `final_price` int(15) NOT NULL,
  `payment_method` varchar(20) NOT NULL,
  `sale_to_cust_id` varchar(40) NOT NULL,
  `sale_by_emp_id` int(11) NOT NULL,
  `sale_involved_car_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table `sale`
INSERT INTO `sale` (`sale_ID`, `sale_date`, `final_price`, `payment_method`, `sale_to_cust_id`, `sale_by_emp_id`, `sale_involved_car_id`) VALUES
('hars_3_1004_2024-03-', '2024-03-10', 85, 'visa', 'harshit_1401_2313', 1004, 3),
('ian _1_1004_2024-03-', '2024-03-06', 51, 'visa', 'ian s tauro_4879_5954', 1004, 1),
('ian _2_1001_2024-03-', '2024-03-06', 235, 'visa', 'ian s tauro_4879_5954', 1001, 2),
('ian _3_1001_2024-03-', '2024-03-06', 85, 'visa', 'ian s tauro_4879_5954', 1001, 3),
('kara_1_1002_2024-03-', '2024-03-06', 51, 'visa', 'karan_1384_1419', 1002, 1),
('kara_1_1004_2024-03-', '2024-03-06', 51, 'visa', 'karan_1384_1419', 1004, 1),
('kara_2_2001_2024-03-', '2024-03-11', 235, 'crypto', 'karan_1384_1419', 2001, 2),
('kara_3_1004_2024-03-', '2024-03-06', 85, 'visa', 'karan_1384_1419', 1004, 3),
('kara_3_2001_2024-03-', '2024-03-11', 85, 'visa', 'karan_1384_1419', 2001, 3),
('kara_4_1004_2024-03-', '2024-03-11', 48, 'visa', 'karan_1384_1419', 1004, 4);

-- --------------------------------------------------------

-- Table structure for table `sale_finance_details`
CREATE TABLE `sale_finance_details` (
  `finance_detail` varchar(20) NOT NULL,
  `sale_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ------------------------------------------------------

-- ? Indexes for dumped tables

-- Indexes for table `appointment`
ALTER TABLE `appointment`
  ADD PRIMARY KEY (`app_ID`),
  ADD KEY `appointment_ibfk_1` (`handling_emp_id`),
  ADD KEY `appointment_ibfk_2` (`booking_cust_id`),
  ADD KEY `appointment_ibfk_3` (`Appointment_for_car_id`);

-- Indexes for table `car_features`
ALTER TABLE `car_features`
  ADD PRIMARY KEY (`car_ID`);

-- Indexes for table `car_ownership`
ALTER TABLE `car_ownership`
  ADD PRIMARY KEY (`owner_cust_id`,`owned_car_id`,`emp_ID`),
  ADD KEY `owned_car_id` (`owned_car_id`);

-- Indexes for table `customer`
ALTER TABLE `customer`
  ADD PRIMARY KEY (`customer_ID`);

-- Indexes for table `department`
ALTER TABLE `department`
  ADD PRIMARY KEY (`dept_ID`),
  ADD KEY `manager_emp_id` (`manager_emp_id`);

-- Indexes for table `employee`
ALTER TABLE `employee`
  ADD PRIMARY KEY (`emp_ID`),
  ADD UNIQUE KEY `emp_ID` (`emp_ID`),
  ADD KEY `works_for_dept_id` (`works_for_dept_id`);

-- Indexes for table `review`
ALTER TABLE `review`
  ADD PRIMARY KEY (`review_ID`),
  ADD KEY `review_cust_id` (`review_cust_id`),
  ADD KEY `assessed_car_id` (`assessed_car_id`);

-- Indexes for table `sale`
ALTER TABLE `sale`
  ADD PRIMARY KEY (`sale_ID`),
  ADD KEY `sale_to_cust_id` (`sale_to_cust_id`),
  ADD KEY `sale_by_emp_id` (`sale_by_emp_id`),
  ADD KEY `sale_involved_car_id` (`sale_involved_car_id`);

-- Indexes for table `sale_finance_details`
ALTER TABLE `sale_finance_details`
  ADD PRIMARY KEY (`finance_detail`,`sale_ID`);

-- --------------------------------------------------------

-- ? Constraints for dumped tables

-- Constraints for table `appointment`
ALTER TABLE `appointment`
  ADD CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`handling_emp_id`) REFERENCES `employee` (`emp_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `appointment_ibfk_3` FOREIGN KEY (`Appointment_for_car_id`) REFERENCES `car_features` (`car_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

-- Constraints for table `car_ownership`
ALTER TABLE `car_ownership`
  ADD CONSTRAINT `car_ownership_ibfk_1` FOREIGN KEY (`owned_car_id`) REFERENCES `car_features` (`car_ID`);

-- Constraints for table `employee`
ALTER TABLE `employee`
  ADD CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`works_for_dept_id`) REFERENCES `department` (`dept_ID`);

-- Constraints for table `review`
ALTER TABLE `review`
  ADD CONSTRAINT `review_ibfk_2` FOREIGN KEY (`assessed_car_id`) REFERENCES `car_features` (`car_ID`);

-- Constraints for table `sale`
ALTER TABLE `sale`
  ADD CONSTRAINT `sale_ibfk_2` FOREIGN KEY (`sale_by_emp_id`) REFERENCES `employee` (`emp_ID`),
  ADD CONSTRAINT `sale_ibfk_3` FOREIGN KEY (`sale_involved_car_id`) REFERENCES `car_features` (`car_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
