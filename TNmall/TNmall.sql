-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: localhost    Database: wad
-- ------------------------------------------------------
-- Server version	8.0.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `product_id` int NOT NULL,
  `product_amount` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cart_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` VALUES (10,4,10,1),(11,5,15,3);
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category_id` (`id`),
  UNIQUE KEY `category_name` (`category_name`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (2,'Appliance'),(7,'Book'),(1,'Clothing'),(4,'Cosmetic'),(3,'Electronic'),(8,'Other');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(100) NOT NULL,
  `customer_phone` varchar(100) NOT NULL,
  `customer_email` varchar(100) NOT NULL,
  `customer_address` varchar(255) NOT NULL,
  `customer_password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `customer_id` (`id`),
  UNIQUE KEY `customer_email` (`customer_email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (4,'kkkkkkkkknnnnnnn','13666200982','kkkkkknnnnnn@qq.com','chengdu','$2b$12$2VuZxjmLLsoW6CbGGoCWouXQQZZzJuaKmVXA1rXmRNpnCzebdDPXa'),(5,'fomokn','19983573669','978345838@qq.com','chengdu','$2b$12$OUXp0VdWrxqCBajA0MVYDejok4H0hhaN2IC6Yu9cAieHGzQ4lEWpW');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `product_id` int NOT NULL,
  `feedback_time` datetime NOT NULL,
  `feedback_content` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `feedback_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (11,4,10,'2023-05-21 16:13:57','6666666666'),(12,4,15,'2023-05-21 16:14:53','1966666666666666'),(13,5,10,'2023-05-21 16:16:25','kkkkkkkkkkkkkkkkkkkkkkkknnnnnnnnnnnn'),(14,5,11,'2023-05-21 16:16:47','5555555555555555555555555');
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `vendor_id` int NOT NULL,
  `customer_id` int NOT NULL,
  `product_amount` int NOT NULL,
  `order_create_time` datetime NOT NULL,
  `order_total` int DEFAULT NULL,
  `order_status` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_info_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (7,10,6,4,3,'2023-05-21 16:14:15',23097,0),(8,15,7,4,1,'2023-05-21 16:14:42',240,0),(9,10,6,5,2,'2023-05-21 16:16:02',15398,1);
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category_id` int NOT NULL,
  `vendor_id` int NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `product_desc` varchar(100) NOT NULL,
  `product_price` decimal(8,1) NOT NULL,
  `product_img` varchar(100) NOT NULL,
  `product_discount_status` tinyint NOT NULL DEFAULT '0',
  `product_discount_price` decimal(8,1) DEFAULT NULL,
  `product_discount_deadline` datetime DEFAULT NULL,
  `product_dislike` int DEFAULT NULL,
  `product_like` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (10,3,6,'LEGION Y7000','This is a laptop',7899.0,'static/product_images\\LEGION.jpg',1,7699.0,'2023-06-24 16:02:00',2,4),(11,3,6,'LEGION Y9000','900090000',9899.0,'static/product_images\\fb1fd3eee080480a85bf4041111db734.png',0,9899.0,NULL,0,1),(12,3,6,'Yoga','yogagagaga',5655.0,'static/product_images\\R_1.jpg',1,5400.0,'2023-07-01 16:04:00',0,0),(14,3,6,'Xiaoxin Pro16','xxxxxxxxxxxxxxx',6355.0,'static/product_images\\XIAOXIN.jpg',0,6355.0,NULL,0,0),(15,4,7,'196','lipstick',256.0,'static/product_images\\OIP-C.jpg',1,240.0,'2023-06-10 16:08:00',2,5),(16,1,8,'Sport coat','nikeeeeeeeee',350.0,'static/product_images\\R.jpg',1,300.0,'2023-06-22 16:10:00',0,0),(17,2,9,'XQG100','hhjfjhvhj',3666.0,'static/product_images\\R-C.png',1,2999.0,'2023-06-24 16:13:00',0,0);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendor`
--

DROP TABLE IF EXISTS `vendor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `vendor_name` varchar(100) NOT NULL,
  `vendor_phone` varchar(100) NOT NULL,
  `vendor_email` varchar(100) NOT NULL,
  `vendor_address` varchar(255) NOT NULL,
  `vendor_password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vendor_id` (`id`),
  UNIQUE KEY `vendor_email` (`vendor_email`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendor`
--

LOCK TABLES `vendor` WRITE;
/*!40000 ALTER TABLE `vendor` DISABLE KEYS */;
INSERT INTO `vendor` VALUES (6,'Lenovo','11111111','11111111@Lenovo.com','chengdu','$2b$12$lq1Qv8pRmDPI/TE78iklI.8MXxNDDC2fhF4h9Be3CfPxK9PIjgmVa'),(7,'Lancome','2222222','22222222@Lancome.com','beijing','$2b$12$BU2YdvdA1ukX83P8CpaBw.Dx61WZ1TMfiAPeCJCda.OCrROXq.uYq'),(8,'Nike','33333333','33333333@Nike.com','shanghai','$2b$12$aTkeHC8/wPoexlMmQa.smu8GyLz6uEUZb6wrPwQ51FsW/kIbZFvqq'),(9,'Panasonic','44444444','44444444@Panasonic','shanghai','$2b$12$NWHj2agNGyAzA31SMcnZuehacS4PYmJ6pTndaQ3.zyJPS1w0Rxfvm');
/*!40000 ALTER TABLE `vendor` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-21 22:03:57
