

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `A-PLAN`
--

-- --------------------------------------------------------

--
-- Table structure for table `Student`
--

CREATE TABLE `Student` (
  `NYU_Net_ID` varchar(20) NOT NULL,
  `First_Name` varchar(30) NOT NULL,
  `Last_Name` varchar(30) NOT NULL,
  `Major` varchar(40) NOT NULL,
  `N_ID` int(20) NOT NULL,
  `Password` char(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Student`
--

INSERT INTO `Student` (`NYU_Net_ID`, `First_Name`, `Last_Name`, `Major`, `N_ID`, `Password`) VALUES
('aaa123@nyu.edu', 'chair', 'bed', 'Computer Science', 22222222, '$5$rounds=535000$7dB6RSsxiBZtvcfc$2qv05.5pI9g0xJaeMCg9lH4whniExm2/qKadVfdt8rC'),
('bbtt147@nyu.edu', 'Bob', 'Table', 'Math', 1111, '$5$rounds=535000$amao/rpSKckakkxl$efi/kjS7SgreAqqilYBwcLI8AmrlkMJZOVUpJWGh5X.'),
('mat1223@nyu.edu', 'Math', 'Moremath', 'Computer Science', 88888888, '$5$rounds=535000$aRnTdq23K5AmYNae$gxzo1tqrJFmYx.whle3tUcgspXkgVuPxSBPEJtAVxn3'),
('mgg123@nyu.edu', 'Mark', 'Green', 'Computer Science', 77770000, '$5$rounds=535000$kU7igGCFGnVKTY9i$9KkserqpfIbExMVOcCjoJQg1mghJ0srhQokJIAuy9H4'),
('orgg178@nyu.edu', 'Orange', 'Green', 'Computer Science', 22227777, '$5$rounds=535000$mA89fq3CQTdKZ4gi$FPzK9mYqp62dKDBkylRKMilZ8bWgE/5qf41O.P4B8K6'),
('ssj152@nyu.edu', 'John', 'Sterling', 'Computer Science', 22222222, '$5$rounds=535000$aC8pAQFTr8mC0YGi$AU7Fcli03gy0fI.UkHt2tiP.d7B/Xc4yF7ovLWhm9qA'),
('ww123@nyu.edu', 'Hat', 'Pat', 'Engineering', 22222222, '$5$rounds=535000$HOJWxdTwszKD36PD$qhjgOVQbBIneta.mnhJ0/7rplHf2fiZKebCJ.Cklvk2'),
('yyc785@nyu.edu', 'Yewon', 'Cho', 'Computer Science', 77774444, '$5$rounds=535000$EMySOoJMN6yC7Nvm$yznhwsCudlceVuKRfyLGM09QmKIPfu7j.l7g5IoUGJ2'),
('yyy123@nyu.edu', 'Mike', 'Lee', 'Engineering', 0, '$5$rounds=535000$m9AxqpY.rqiJwxhU$4M8Uq7GBnfZh4U8UJrYFgNFsW5fQlLPcIBYhZOorvb/'),
('zzz1234@nyu.edu', 'Blue', 'Red', 'Engineering', 11111111, '$5$rounds=535000$00zWFH7QRr53O97X$CmIaej/G6vDYSLTTr.yWKfKkkK8x.UWM.puMt4qjybD'),
('zzz123@nyu.edu', 'Joe', 'Bob', 'Engineering', 1234567, '$5$rounds=535000$PFBEyXaqFlhZP3w.$OMKp.fqf9VvL6jO9iUCKbbY4zguEJn5FYhKjuXK9h23');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Student`
--
ALTER TABLE `Student`
  ADD UNIQUE KEY `NYU_Net_ID` (`NYU_Net_ID`,`N_ID`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
