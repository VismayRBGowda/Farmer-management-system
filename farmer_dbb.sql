
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


CREATE TABLE IF NOT EXISTS `addagroproducts` (
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `pid` int(11) NOT NULL,
  `productname` varchar(100) NOT NULL,
  `productdesc` text NOT NULL,
  `price` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `trig` (
  `id` int(11) NOT NULL,
  `farmer_id` varchar(50) NOT NULL,
  `action` varchar(50) NOT NULL,
  `timestamp` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE IF NOT EXISTS `farmers` (
    farmer_id INT AUTO_INCREMENT PRIMARY KEY,
    fname VARCHAR(255) NOT NULL,
    lname VARCHAR(255) NOT NULL,
    dob DATE NOT NULL,
    farming_experience INT NOT NULL,
    phone_no VARCHAR(10) NOT NULL,
    state VARCHAR(255) NOT NULL,
    district VARCHAR(255) NOT NULL,
    town_village VARCHAR(255) NOT NULL,
    pincode VARCHAR(6) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DELIMITER $$
CREATE TRIGGER `deletion` BEFORE DELETE ON `farmers` FOR EACH ROW INSERT INTO trig VALUES(null,OLD.farmer_id,'FARMER DELETED',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `insertion` AFTER INSERT ON `farmers` FOR EACH ROW INSERT INTO trig VALUES(null,NEW.farmer_id,'Farmer Inserted',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `updation` AFTER UPDATE ON `farmers` FOR EACH ROW INSERT INTO trig VALUES(null,NEW.farmer_id,'FARMER UPDATED',NOW())
$$
DELIMITER ;


CREATE TABLE IF NOT EXISTS `land_details`(
    land_id  INT AUTO_INCREMENT PRIMARY KEY,
    size FLOAT NOT NULL,
    location VARCHAR(255) NOT NULL,
    soil_type VARCHAR(255) NOT NULL,
    irrigation_system VARCHAR(255) NOT NULL,
    farmer_id INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE IF NOT EXISTS `crops` (
    crop_id INT AUTO_INCREMENT PRIMARY KEY,
    crop_type VARCHAR(255) NOT NULL,
    planting_date DATE NOT NULL,
    harvest_date DATE NOT NULL,
    expected_yield INT NOT NULL,
    actual_yield INT NOT NULL,
    fertilizers_used VARCHAR(255) NOT NULL,
    farmer_id INT
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE IF NOT EXISTS `farm_equipment` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(255) NOT NULL,
    model VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    purchase_date DATE NOT NULL,
    farmer_id INT
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;;




CREATE TABLE IF NOT EXISTS `farm_animals` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    breed VARCHAR(255) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    age INT NOT NULL,
    health_status VARCHAR(255) NOT NULL,
    farmer_id INT
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;;



CREATE TABLE IF NOT EXISTS `labour` (
    labour_id INT AUTO_INCREMENT PRIMARY KEY,
    fname VARCHAR(255) NOT NULL,
    lname VARCHAR(255) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    phone_no VARCHAR(15) NOT NULL,
    state VARCHAR(255) NOT NULL,
    district VARCHAR(255) NOT NULL,
    town_village VARCHAR(255) NOT NULL,
    pincode  VARCHAR(6) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;;




CREATE TABLE IF NOT EXISTS `labour_hired` (
    hiring_id INT AUTO_INCREMENT PRIMARY KEY,
    labour_id INT,
    hiring_date DATE NOT NULL,
    no_of_days_worked INT NOT NULL,
    labour_cost DECIMAL(10,2) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE `test` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



DELIMITER $$

CREATE PROCEDURE `SelectFarmersByState` (IN state_param VARCHAR(255))
BEGIN
    SELECT * FROM farmers WHERE state = state_param;
END $$

DELIMITER ;


ALTER TABLE `addagroproducts`
  ADD PRIMARY KEY (`pid`);


ALTER TABLE `test`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `trig`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);


ALTER TABLE land_details
ADD CONSTRAINT fk_land_details_farmer
FOREIGN KEY (farmer_id) REFERENCES farmers(farmer_id);

ALTER TABLE `crops`
ADD COLUMN `land_id` INT,
ADD FOREIGN KEY (`land_id`) REFERENCES `land_details` (`land_id`);

ALTER TABLE `farm_equipment`
ADD FOREIGN KEY (`farmer_id`) REFERENCES `farmers` (`farmer_id`);

ALTER TABLE `farm_animals`
ADD FOREIGN KEY (`farmer_id`) REFERENCES `farmers` (`farmer_id`);

ALTER TABLE `labour_hired`
ADD COLUMN `farmer_id` INT,
ADD FOREIGN KEY (`farmer_id`) REFERENCES `farmers` (`farmer_id`);

ALTER TABLE `user` ADD COLUMN `role` VARCHAR(20) NOT NULL DEFAULT 'user';


ALTER TABLE `addagroproducts`
  MODIFY `pid` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `test`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `trig`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

COMMIT;

