-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 21, 2024 at 12:24 PM
-- Server version: 10.6.15-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hallbookingsystem_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'hallmanagementadmin', '0001_initial', '2024-10-05 08:27:01.427185'),
(2, 'contenttypes', '0001_initial', '2024-10-05 08:27:29.027610'),
(3, 'auth', '0001_initial', '2024-10-05 08:27:29.257997'),
(4, 'admin', '0001_initial', '2024-10-05 08:27:29.331111'),
(5, 'admin', '0002_logentry_remove_auto_add', '2024-10-05 08:27:29.339279'),
(6, 'admin', '0003_logentry_add_action_flag_choices', '2024-10-05 08:27:29.350873'),
(7, 'contenttypes', '0002_remove_content_type_name', '2024-10-05 08:27:29.410500'),
(8, 'auth', '0002_alter_permission_name_max_length', '2024-10-05 08:27:29.436378'),
(9, 'auth', '0003_alter_user_email_max_length', '2024-10-05 08:27:29.460203'),
(10, 'auth', '0004_alter_user_username_opts', '2024-10-05 08:27:29.470422'),
(11, 'auth', '0005_alter_user_last_login_null', '2024-10-05 08:27:29.499059'),
(12, 'auth', '0006_require_contenttypes_0002', '2024-10-05 08:27:29.500294'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2024-10-05 08:27:29.509068'),
(14, 'auth', '0008_alter_user_username_max_length', '2024-10-05 08:27:29.532808'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2024-10-05 08:27:29.555790'),
(16, 'auth', '0010_alter_group_name_max_length', '2024-10-05 08:27:29.581249'),
(17, 'auth', '0011_update_proxy_permissions', '2024-10-05 08:27:29.606992'),
(18, 'auth', '0012_alter_user_first_name_max_length', '2024-10-05 08:27:29.629263'),
(19, 'sessions', '0001_initial', '2024-10-05 08:27:29.654239');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('cihuxbayjnh2zy91xizrfqd15432t7ft', 'eyJ1aWQiOjExfQ:1t1AP9:aB62CLWbL4_jxtL0W6s0YtKDqdOihI39bTYdfgbDIJA', '2024-10-30 20:13:59.786808'),
('fonarzk5yzgsiggzmg8m09byybsu583b', '.eJxVjUEOQDAQRe_y141EkNCVm8hgyCRa0ioLcXfDzuov3nv5F5KMsLlB8uQYFjQ68e3sSJZsWB2URA4KvjFY9w22LIuqbgz41ZRFmk7yFFNPEn6x6t3BQSZh_dlD4vsBiXIm1g:1syPOj:mqmw6YcUuSxg4WeBQtSifPhf-9m2ncc_zpmUyltN8GQ', '2024-10-23 05:38:09.108256'),
('ip0fm5vx6ibxwllfh8u0yi8npy9vhsuz', 'eyJvdHAiOjEyOTkxOSwiZW1haWwiOiJzYWRAZ21haWwuY29tIiwib3RwX3ZlcmlmaWVkIjp0cnVlfQ:1sy2vf:I87nJ7VLe6KOJZ1x2u5sHmCVzxe1J_UXt7wop9MY8Yk', '2024-10-22 05:38:39.369249'),
('mg2n1c8pwic2wn2p3851wlo2gt35n5pg', 'e30:1sy2wO:pTzIGL3U5KoZopMtldzm4TG3GlPbSMfTZUv-e4_p_qI', '2024-10-22 05:39:24.493634'),
('orgwhk2r5jyrb8y1ham2za27arng4fvd', 'eyJ1aWQiOjExLCJvdHAiOjQ4NjMyOSwiZW1haWwiOiJzYWZ3YW5hc3ViYWlyQGdtYWlsLmNvbSIsIm90cF92ZXJpZmllZCI6dHJ1ZX0:1t1fzS:ZLPrLPOejXYV29NhC4gJBgrM0t5nhk-LmDaGBgHtppA', '2024-11-01 05:57:34.552895'),
('ovtsg17w6x8kqctp6cx1soy8z1izlpko', 'eyJ1aWQiOjExfQ:1t1h4r:CcqkEQjzBtSQgD2rwK2hbo7J34jBXXJSpMxuS91hO2U', '2024-11-01 07:07:13.592372'),
('w5kny2xqx41l1scrzyzcj9hu5gn6eps6', 'e30:1sy2x4:apnzwuc1zLbJluZKkqPgTyCTvmVIBNuS7cLV9jDhTIY', '2024-10-22 05:40:06.285562'),
('ym85z2ilxaualg2cmnnsmhsa537ab6d9', 'eyJ1aWQiOjM4LCJvdHBfdmVyaWZpZWQiOnRydWV9:1t1k4D:jyO-0L9oTQGLG6R3l0cMV3wf7lpURQ0ocGSEXvsdJLw', '2024-11-01 10:18:45.925433'),
('yvyoogj59ljafrwylb5gj8cnxgifu1xr', 'eyJ1aWQiOjM4LCJvdHBfdmVyaWZpZWQiOnRydWV9:1t2ooT:9JTsvT2rjKjKUDGigBSCUO9ppq9xZwi7WA8tIPmMHqg', '2024-11-04 09:34:57.752778');

-- --------------------------------------------------------

--
-- Table structure for table `hallmanagementadmin_adminrecord`
--

CREATE TABLE `hallmanagementadmin_adminrecord` (
  `id` bigint(20) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `addedon` date NOT NULL,
  `superadmin` int(11) NOT NULL,
  `isdelete` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hallmanagementadmin_adminrecord`
--

INSERT INTO `hallmanagementadmin_adminrecord` (`id`, `username`, `email`, `password`, `addedon`, `superadmin`, `isdelete`) VALUES
(38, 'Lala', 'lala@gmail.com', 'Lala@123', '2024-10-18', 1, 0),
(39, 'Manjima', 'manji@gmail.com', 'Manj@123', '2024-10-18', 0, 0),
(40, 'Tony Jose', 'tony@gmail.com', 'Tony@123', '2024-10-18', 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `hallmanagementadmin_availability`
--

CREATE TABLE `hallmanagementadmin_availability` (
  `id` bigint(20) NOT NULL,
  `sunday` int(11) NOT NULL,
  `monday` int(11) NOT NULL,
  `tuesday` int(11) NOT NULL,
  `wednesday` int(11) NOT NULL,
  `thursday` int(11) NOT NULL,
  `friday` int(11) NOT NULL,
  `saturday` int(11) NOT NULL,
  `addedon` date NOT NULL,
  `isdelete` int(11) NOT NULL,
  `addedby` int(11) NOT NULL,
  `hall_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hallmanagementadmin_availability`
--

INSERT INTO `hallmanagementadmin_availability` (`id`, `sunday`, `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`, `addedon`, `isdelete`, `addedby`, `hall_id`) VALUES
(96, 1, 1, 1, 0, 0, 0, 0, '2024-10-18', 0, 0, 175),
(97, 0, 0, 1, 1, 0, 0, 0, '2024-10-18', 0, 0, 176),
(98, 0, 0, 0, 0, 0, 1, 0, '2024-10-18', 0, 0, 177);

-- --------------------------------------------------------

--
-- Table structure for table `hallmanagementadmin_booking`
--

CREATE TABLE `hallmanagementadmin_booking` (
  `id` bigint(20) NOT NULL,
  `date` date NOT NULL,
  `timeslot` varchar(100) NOT NULL,
  `ac` varchar(100) NOT NULL,
  `description` varchar(100) NOT NULL,
  `event_name` varchar(100) NOT NULL,
  `addedon` date NOT NULL,
  `approval_status` tinyint(1) NOT NULL,
  `evening_before` varchar(3) DEFAULT NULL,
  `features` longtext NOT NULL,
  `hall_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hallmanagementadmin_booking`
--

INSERT INTO `hallmanagementadmin_booking` (`id`, `date`, `timeslot`, `ac`, `description`, `event_name`, `addedon`, `approval_status`, `evening_before`, `features`, `hall_id`, `user_id`) VALUES
(31, '2024-09-29', 'Full Day', 'A/C', 'wewqe', 'marriage', '2024-10-18', 0, NULL, '20', 175, 22),
(32, '2024-09-28', 'Evening', 'A/C', 'wewqe', 'marriage', '2024-10-18', 1, 'no', '20', 175, 22),
(33, '2024-10-18', 'Full Day', 'A/C', 'dfsfsfsfs', 'marriage', '2024-10-19', 1, NULL, '19', 177, 23),
(35, '2024-10-28', 'Full Day', 'A/C', 'For marriage.', 'marriage', '2024-10-19', 1, 'no', '18, 20', 175, 24),
(36, '2024-10-27', 'Evening', 'A/C', 'For marriage.', 'marriage', '2024-10-19', 1, 'no', '18, 20', 175, 24),
(37, '2024-10-15', 'Full Day', 'A/C', 'xxzx', 'marriage', '2024-10-19', 1, 'no', '18', 175, 25),
(38, '2024-10-14', 'Evening', 'A/C', 'xxzx', 'marriage', '2024-10-19', 0, 'no', '18', 175, 25),
(39, '2024-10-22', 'Evening', 'A/C', 'cscsad', 'marriage', '2024-10-19', 0, NULL, '', 175, 26);

-- --------------------------------------------------------

--
-- Table structure for table `hallmanagementadmin_discountrate`
--

CREATE TABLE `hallmanagementadmin_discountrate` (
  `id` int(11) NOT NULL,
  `rate` varchar(100) NOT NULL,
  `isdelete` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hallmanagementadmin_discountrate`
--

INSERT INTO `hallmanagementadmin_discountrate` (`id`, `rate`, `isdelete`) VALUES
(1, '25', 1),
(2, '25', 0),
(3, '23', 0),
(4, '60', 0),
(5, '25', 0),
(6, '20', 0),
(7, '68', 0);

-- --------------------------------------------------------

--
-- Table structure for table `hallmanagementadmin_feature`
--

CREATE TABLE `hallmanagementadmin_feature` (
  `id` bigint(20) NOT NULL,
  `featurename` varchar(100) NOT NULL,
  `addedby` int(11) NOT NULL,
  `addedon` date NOT NULL,
  `isdelete` int(11) NOT NULL,
  `amount` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hallmanagementadmin_feature`
--

INSERT INTO `hallmanagementadmin_feature` (`id`, `featurename`, `addedby`, `addedon`, `isdelete`, `amount`) VALUES
(22, 'Wifi', 0, '2024-10-21', 1, ''),
(23, 'Pool', 0, '2024-10-21', 1, ''),
(24, 'Parking', 0, '2024-10-21', 1, ''),
(25, 'Kitchen', 0, '2024-10-21', 1, ''),
(26, 'Wifi', 0, '2024-10-21', 0, '25000');

-- --------------------------------------------------------

--
-- Table structure for table `hallmanagementadmin_hall`
--

CREATE TABLE `hallmanagementadmin_hall` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `place` varchar(100) NOT NULL,
  `landmark` varchar(100) NOT NULL,
  `capacity` varchar(100) NOT NULL,
  `pincode` varchar(100) NOT NULL,
  `district` varchar(100) NOT NULL,
  `ac_nonac_both` varchar(100) NOT NULL,
  `ac_rent` varchar(100) NOT NULL,
  `non_ac_rent` varchar(100) NOT NULL,
  `owner_name` varchar(100) NOT NULL,
  `contact` varchar(100) NOT NULL,
  `images` varchar(100) NOT NULL,
  `addedon` date NOT NULL,
  `isdelete` int(11) NOT NULL,
  `addedby` int(11) NOT NULL,
  `description` varchar(1000) NOT NULL,
  `terms` varchar(2000) NOT NULL,
  `location` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hallmanagementadmin_hall`
--

INSERT INTO `hallmanagementadmin_hall` (`id`, `name`, `place`, `landmark`, `capacity`, `pincode`, `district`, `ac_nonac_both`, `ac_rent`, `non_ac_rent`, `owner_name`, `contact`, `images`, `addedon`, `isdelete`, `addedby`, `description`, `terms`, `location`) VALUES
(175, 'Cosmo', 'Eriyad', 'Near Eriyad Kvhss school.', '1500', '680661', 'Thrissur', 'A/C', '12000', '', 'Nandhana', '7789343743', '', '2024-10-18', 0, 0, 'Cosmopolitan Convention Center in Eriyad,Thrissur.', '•  Booking Confirmation: A reservation is confirmed only upon receipt of a signed contract and a deposit.\r\n•  Payment: Full payment must be made at least [number] days before the event. Accepted payment methods include [list payment methods].\r\n•  Cancellation Policy:\r\n•	Cancellations made [number] days prior to the event will receive a full refund.\r\n•	Cancellations made less than [number] days prior will incur a [percentage]% cancellation fee.\r\n•  Capacity Limits: The maximum capacity of the hall is [number] attendees. Exceeding this limit may result in additional charges or cancellation of the booking.\r\n•  Use of Facilities:\r\n•	The hall must be used for the purpose specified in the booking.\r\n•	No alterations to the hall\'s structure or decor are allowed without prior permission.\r\n•  Damage and Liability:\r\n•	The booking party is responsible for any damage incurred during the event.\r\n•	The venue is not liable for any injuries or losses that occur during the event.\r\n\r\n', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3926.462036731539!2d76.16557557408042!3d10.224269669137517!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3b081951c01ddd39%3A0xf5de2005911cfc9d!2sCosmopolitan%20Convention%20Center!5e0!3m2!1sen!2sin!4v1729227553861!5m2!1sen!2sin'),
(176, 'Seema', 'Perumbavoor', 'Near  Calelin Market .', '2000', '680655', 'Ernakulam', 'Non A/C', '', '15000', 'Tony Jose', '9633080149', '', '2024-10-18', 0, 0, 'Seema Auditorium is located Calelin Market in Perumbavoor.', '•  Booking Confirmation: A reservation is confirmed only upon receipt of a signed contract and a deposit.\r\n•  Payment: Full payment must be made at least [number] days before the event. Accepted payment methods include [list payment methods].\r\n•  Cancellation Policy:\r\n•	Cancellations made [number] days prior to the event will receive a full refund.\r\n•	Cancellations made less than [number] days prior will incur a [percentage]% cancellation fee.\r\n•  Capacity Limits: The maximum capacity of the hall is [number] attendees. Exceeding this limit may result in additional charges or cancellation of the booking.\r\n•  Use of Facilities:\r\n•	The hall must be used for the purpose specified in the booking.\r\n•	No alterations to the hall\'s structure or decor are allowed without prior permission.\r\n•  Damage and Liability:\r\n•	The booking party is responsible for any damage incurred during the event.\r\n•	The venue is not liable for any injuries or losses that occur during the event.\r\n\r\n', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3927.872004524086!2d76.47422647407903!3d10.109561671141844!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3b07e260fdd68ff7%3A0xbd3cac3a4dc687f6!2sSEEMA%20Auditorium!5e0!3m2!1sen!2sin!4v1729227932656!5m2!1sen!2sin'),
(177, 'Bahadhur', 'Kara', 'Near Kara Center.', '1000', '680671', 'Thrissur', 'Both A/C and Non A/C', '12000', '10000', 'Helga', '7789343743', '', '2024-10-18', 0, 0, 'Convention center in Kara, Kerala\r\n', '•  Booking Confirmation: A reservation is confirmed only upon receipt of a signed contract and a deposit.\r\n•  Payment: Full payment must be made at least [number] days before the event. Accepted payment methods include [list payment methods].\r\n•  Cancellation Policy:\r\n•	Cancellations made [number] days prior to the event will receive a full refund.\r\n•	Cancellations made less than [number] days prior will incur a [percentage]% cancellation fee.\r\n•  Capacity Limits: The maximum capacity of the hall is [number] attendees. Exceeding this limit may result in additional charges or cancellation of the booking.\r\n•  Use of Facilities:\r\n•	The hall must be used for the purpose specified in the booking.\r\n•	No alterations to the hall\'s structure or decor are allowed without prior permission.\r\n•  Damage and Liability:\r\n•	The booking party is responsible for any damage incurred during the event.\r\n•	The venue is not liable for any injuries or losses that occur during the event.\r\n\r\n', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3926.3128535378337!2d76.15042837408059!3d10.236332068925494!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3b081ec9843bcde3%3A0xf3bff779dff72ad6!2sBahadur%20Convention%20Center!5e0!3m2!1sen!2sin!4v1729228138246!5m2!1sen!2sin');

-- --------------------------------------------------------

--
-- Table structure for table `hallmanagementadmin_hallfeature`
--

CREATE TABLE `hallmanagementadmin_hallfeature` (
  `id` bigint(20) NOT NULL,
  `feature` varchar(100) NOT NULL,
  `addedby` int(11) NOT NULL,
  `addedon` date NOT NULL,
  `isdelete` int(11) NOT NULL,
  `hall_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hallmanagementadmin_hallfeature`
--

INSERT INTO `hallmanagementadmin_hallfeature` (`id`, `feature`, `addedby`, `addedon`, `isdelete`, `hall_id`) VALUES
(140, '20', 0, '2024-10-18', 0, 176),
(141, '21', 0, '2024-10-18', 0, 176),
(142, '18', 0, '2024-10-18', 0, 177),
(143, '19', 0, '2024-10-18', 0, 177),
(153, '18', 0, '2024-10-19', 0, 175),
(154, '20', 0, '2024-10-19', 0, 175);

-- --------------------------------------------------------

--
-- Table structure for table `hallmanagementadmin_imagegallery`
--

CREATE TABLE `hallmanagementadmin_imagegallery` (
  `id` bigint(20) NOT NULL,
  `image` varchar(100) NOT NULL,
  `addedby` int(11) NOT NULL,
  `addedon` date NOT NULL,
  `isdelete` int(11) NOT NULL,
  `hall_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hallmanagementadmin_imagegallery`
--

INSERT INTO `hallmanagementadmin_imagegallery` (`id`, `image`, `addedby`, `addedon`, `isdelete`, `hall_id`) VALUES
(111, 'hall_images/images_3_wUjhwzD.jfif', 0, '2024-10-18', 0, 175),
(112, 'hall_images/images_4_62Q5wRY.jfif', 0, '2024-10-18', 0, 175),
(113, 'hall_images/images_5_rml6hDM.jfif', 0, '2024-10-18', 0, 176),
(114, 'hall_images/images_6_dBi0eTM.jfif', 0, '2024-10-18', 0, 176),
(115, 'hall_images/images_7_jRwbHlb.jfif', 0, '2024-10-18', 0, 176),
(116, 'hall_images/images_6_I50Aylb.jfif', 0, '2024-10-18', 0, 177),
(117, 'hall_images/images_9_LQ141Jh.jfif', 0, '2024-10-18', 0, 177),
(118, 'hall_images/images_10_GpITeRW.jfif', 0, '2024-10-18', 0, 177),
(119, 'hall_images/images_13.jfif', 0, '2024-10-19', 0, 175);

-- --------------------------------------------------------

--
-- Table structure for table `hallmanagementadmin_inoperability`
--

CREATE TABLE `hallmanagementadmin_inoperability` (
  `id` bigint(20) NOT NULL,
  `start_date` varchar(100) NOT NULL,
  `end_date` varchar(100) NOT NULL,
  `reason` varchar(100) NOT NULL,
  `addedby` int(11) NOT NULL,
  `addedon` date NOT NULL,
  `isdelete` int(11) NOT NULL,
  `hall_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hallmanagementadmin_inoperability`
--

INSERT INTO `hallmanagementadmin_inoperability` (`id`, `start_date`, `end_date`, `reason`, `addedby`, `addedon`, `isdelete`, `hall_id`) VALUES
(18, '2024-10-02', '2024-10-09', 'rtwet', 0, '2024-10-19', 0, 175),
(19, '2024-10-16', '2024-10-25', 't43t', 0, '2024-10-19', 1, 176),
(20, '2024-10-08', '2024-10-16', 'edwdwd', 0, '2024-10-19', 0, 177);

-- --------------------------------------------------------

--
-- Table structure for table `hallmanagementadmin_member`
--

CREATE TABLE `hallmanagementadmin_member` (
  `id` bigint(20) NOT NULL,
  `role` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `addedby` int(11) NOT NULL,
  `addedon` date NOT NULL,
  `isdelete` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `hallmanagementadmin_payment`
--

CREATE TABLE `hallmanagementadmin_payment` (
  `id` bigint(20) NOT NULL,
  `payment_mode` varchar(100) NOT NULL DEFAULT 'Cash',
  `transaction_id` varchar(100) NOT NULL,
  `total_amount` varchar(100) NOT NULL,
  `cashreceived` varchar(100) NOT NULL,
  `remaining_amount` varchar(100) NOT NULL,
  `booking_id` int(11) NOT NULL,
  `addedby` int(11) NOT NULL,
  `addedon` date NOT NULL,
  `isdelete` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hallmanagementadmin_payment`
--

INSERT INTO `hallmanagementadmin_payment` (`id`, `payment_mode`, `transaction_id`, `total_amount`, `cashreceived`, `remaining_amount`, `booking_id`, `addedby`, `addedon`, `isdelete`) VALUES
(12, 'digital', 'sASA', '13000.00', '1000', '12000.00', 32, 0, '2024-10-18', 0);

-- --------------------------------------------------------

--
-- Table structure for table `hallmanagementadmin_user`
--

CREATE TABLE `hallmanagementadmin_user` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `number` bigint(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `address` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hallmanagementadmin_user`
--

INSERT INTO `hallmanagementadmin_user` (`id`, `name`, `number`, `email`, `address`) VALUES
(1, 'safwana', 1234567890, 'saf@gmail.com', 'ewrwerwer'),
(2, 'Manjima', 1234567890, 'manj@gmail.com', 'fefsere'),
(3, 'Tony Jose', 1234567890, 'tony@gmail.com', 'dADd'),
(19, 'Devika', 9544424963, 'safwanasubair@gmail.com', 'XSADADA'),
(20, 'Fayas', 9544424963, 'fayas@gmail.com', 'dsada'),
(21, 'Saina', 9544424963, 'safwanasubair@gmail.com', 'sdad'),
(22, 'shifa kk', 9544424963, 'sad@gmail.com', 'xsdad'),
(23, 'Alan', 9544424963, 'fayas@gmail.com', 'sfdsfs'),
(24, 'Zera', 9544424963, 'safwanasubair@gmail.com', 'Karappam veetill(h)'),
(25, 'shifa kk', 9544424963, 'safwanasubair@gmail.com', 'Kavvc'),
(26, 'Fayas', 9544424963, 'fayas@gmail.com', 'sdsad');

-- --------------------------------------------------------

--
-- Table structure for table `hallmanagementadmin_user_otp`
--

CREATE TABLE `hallmanagementadmin_user_otp` (
  `id` bigint(20) NOT NULL,
  `otp` int(11) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `addedon` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hallmanagementadmin_user_otp`
--

INSERT INTO `hallmanagementadmin_user_otp` (`id`, `otp`, `is_verified`, `user_id`, `addedon`) VALUES
(16, 830327, 0, NULL, '2024-10-18'),
(17, 52390, 0, NULL, '2024-10-18'),
(18, 876537, 1, NULL, '2024-10-18'),
(19, 156841, 1, 19, '2024-10-18'),
(20, 420402, 1, 20, '2024-10-18'),
(21, 288063, 1, 21, '2024-10-18'),
(22, 786361, 1, 22, '2024-10-18'),
(23, 28572, 0, NULL, '2024-10-19'),
(24, 878872, 1, 23, '2024-10-19'),
(25, 759132, 1, 24, '2024-10-19'),
(26, 112888, 1, 25, '2024-10-19'),
(27, 852429, 1, 26, '2024-10-19');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `hallmanagementadmin_adminrecord`
--
ALTER TABLE `hallmanagementadmin_adminrecord`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `hallmanagementadmin_availability`
--
ALTER TABLE `hallmanagementadmin_availability`
  ADD PRIMARY KEY (`id`),
  ADD KEY `hallmanagementadmin__hall_id_f1a481fc_fk_hallmanag` (`hall_id`);

--
-- Indexes for table `hallmanagementadmin_booking`
--
ALTER TABLE `hallmanagementadmin_booking`
  ADD PRIMARY KEY (`id`),
  ADD KEY `hallmanagementadmin__hall_id_5852e6c6_fk_hallmanag` (`hall_id`),
  ADD KEY `hallmanagementadmin__user_id_ce45ff0f_fk_hallmanag` (`user_id`);

--
-- Indexes for table `hallmanagementadmin_discountrate`
--
ALTER TABLE `hallmanagementadmin_discountrate`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `hallmanagementadmin_feature`
--
ALTER TABLE `hallmanagementadmin_feature`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `hallmanagementadmin_hall`
--
ALTER TABLE `hallmanagementadmin_hall`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `hallmanagementadmin_hallfeature`
--
ALTER TABLE `hallmanagementadmin_hallfeature`
  ADD PRIMARY KEY (`id`),
  ADD KEY `hallmanagementadmin__hall_id_376bd2c3_fk_hallmanag` (`hall_id`);

--
-- Indexes for table `hallmanagementadmin_imagegallery`
--
ALTER TABLE `hallmanagementadmin_imagegallery`
  ADD PRIMARY KEY (`id`),
  ADD KEY `hallmanagementadmin__hall_id_98e9f8ef_fk_hallmanag` (`hall_id`);

--
-- Indexes for table `hallmanagementadmin_inoperability`
--
ALTER TABLE `hallmanagementadmin_inoperability`
  ADD PRIMARY KEY (`id`),
  ADD KEY `hallmanagementadmin__hall_id_1f7ef2c9_fk_hallmanag` (`hall_id`);

--
-- Indexes for table `hallmanagementadmin_member`
--
ALTER TABLE `hallmanagementadmin_member`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `hallmanagementadmin_payment`
--
ALTER TABLE `hallmanagementadmin_payment`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `hallmanagementadmin_user`
--
ALTER TABLE `hallmanagementadmin_user`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `hallmanagementadmin_user_otp`
--
ALTER TABLE `hallmanagementadmin_user_otp`
  ADD PRIMARY KEY (`id`),
  ADD KEY `hallmanagementadmin__user_id_922a7195_fk_hallmanag` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `hallmanagementadmin_adminrecord`
--
ALTER TABLE `hallmanagementadmin_adminrecord`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `hallmanagementadmin_availability`
--
ALTER TABLE `hallmanagementadmin_availability`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=99;

--
-- AUTO_INCREMENT for table `hallmanagementadmin_booking`
--
ALTER TABLE `hallmanagementadmin_booking`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `hallmanagementadmin_discountrate`
--
ALTER TABLE `hallmanagementadmin_discountrate`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `hallmanagementadmin_feature`
--
ALTER TABLE `hallmanagementadmin_feature`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `hallmanagementadmin_hall`
--
ALTER TABLE `hallmanagementadmin_hall`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=178;

--
-- AUTO_INCREMENT for table `hallmanagementadmin_hallfeature`
--
ALTER TABLE `hallmanagementadmin_hallfeature`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=155;

--
-- AUTO_INCREMENT for table `hallmanagementadmin_imagegallery`
--
ALTER TABLE `hallmanagementadmin_imagegallery`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=120;

--
-- AUTO_INCREMENT for table `hallmanagementadmin_inoperability`
--
ALTER TABLE `hallmanagementadmin_inoperability`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `hallmanagementadmin_member`
--
ALTER TABLE `hallmanagementadmin_member`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `hallmanagementadmin_payment`
--
ALTER TABLE `hallmanagementadmin_payment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `hallmanagementadmin_user`
--
ALTER TABLE `hallmanagementadmin_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `hallmanagementadmin_user_otp`
--
ALTER TABLE `hallmanagementadmin_user_otp`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `hallmanagementadmin_availability`
--
ALTER TABLE `hallmanagementadmin_availability`
  ADD CONSTRAINT `hallmanagementadmin__hall_id_f1a481fc_fk_hallmanag` FOREIGN KEY (`hall_id`) REFERENCES `hallmanagementadmin_hall` (`id`);

--
-- Constraints for table `hallmanagementadmin_booking`
--
ALTER TABLE `hallmanagementadmin_booking`
  ADD CONSTRAINT `hallmanagementadmin__hall_id_5852e6c6_fk_hallmanag` FOREIGN KEY (`hall_id`) REFERENCES `hallmanagementadmin_hall` (`id`),
  ADD CONSTRAINT `hallmanagementadmin__user_id_ce45ff0f_fk_hallmanag` FOREIGN KEY (`user_id`) REFERENCES `hallmanagementadmin_user` (`id`);

--
-- Constraints for table `hallmanagementadmin_hallfeature`
--
ALTER TABLE `hallmanagementadmin_hallfeature`
  ADD CONSTRAINT `hallmanagementadmin__hall_id_376bd2c3_fk_hallmanag` FOREIGN KEY (`hall_id`) REFERENCES `hallmanagementadmin_hall` (`id`);

--
-- Constraints for table `hallmanagementadmin_imagegallery`
--
ALTER TABLE `hallmanagementadmin_imagegallery`
  ADD CONSTRAINT `hallmanagementadmin__hall_id_98e9f8ef_fk_hallmanag` FOREIGN KEY (`hall_id`) REFERENCES `hallmanagementadmin_hall` (`id`);

--
-- Constraints for table `hallmanagementadmin_inoperability`
--
ALTER TABLE `hallmanagementadmin_inoperability`
  ADD CONSTRAINT `hallmanagementadmin__hall_id_1f7ef2c9_fk_hallmanag` FOREIGN KEY (`hall_id`) REFERENCES `hallmanagementadmin_hall` (`id`);

--
-- Constraints for table `hallmanagementadmin_user_otp`
--
ALTER TABLE `hallmanagementadmin_user_otp`
  ADD CONSTRAINT `hallmanagementadmin__user_id_922a7195_fk_hallmanag` FOREIGN KEY (`user_id`) REFERENCES `hallmanagementadmin_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
