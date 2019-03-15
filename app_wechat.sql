-- MySQL dump 10.17  Distrib 10.3.13-MariaDB, for osx10.14 (x86_64)
--
-- Host: localhost    Database: app_wechat
-- ------------------------------------------------------
-- Server version	10.3.13-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `adminlogs`
--

DROP TABLE IF EXISTS `adminlogs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adminlogs` (
  `alid` int(11) NOT NULL AUTO_INCREMENT,
  `aid` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`alid`),
  KEY `aid` (`aid`),
  KEY `ix_adminlogs_add_time` (`add_time`),
  CONSTRAINT `adminlogs_ibfk_1` FOREIGN KEY (`aid`) REFERENCES `admins` (`aid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adminlogs`
--

LOCK TABLES `adminlogs` WRITE;
/*!40000 ALTER TABLE `adminlogs` DISABLE KEYS */;
/*!40000 ALTER TABLE `adminlogs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admins` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `account` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `is_super` smallint(6) DEFAULT NULL,
  `rid` int(11) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`aid`),
  UNIQUE KEY `account` (`account`),
  KEY `rid` (`rid`),
  KEY `ix_admins_add_time` (`add_time`),
  CONSTRAINT `admins_ibfk_1` FOREIGN KEY (`rid`) REFERENCES `roles` (`rid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (1,'admin','pbkdf2:sha256:50000$E9CGuhgO$d0936d3bb41a83613424fa2bc3207cee18440d0c81bdadaea4b30678343809c4',0,1,'2019-03-10 03:08:23'),(2,'newtorn','pbkdf2:sha256:50000$pBCTmkJj$35409487b2618849448c841c31420b0c159edb121e6f51b37b7a952cfe30b2a5',1,2,'2019-03-10 03:08:23');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('79129d6fa01d');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auths`
--

DROP TABLE IF EXISTS `auths`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auths` (
  `auid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `url` varchar(255) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`auid`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `url` (`url`),
  KEY `ix_auths_add_time` (`add_time`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auths`
--

LOCK TABLES `auths` WRITE;
/*!40000 ALTER TABLE `auths` DISABLE KEYS */;
INSERT INTO `auths` VALUES (1,'首页','index','2019-03-10 01:58:32'),(2,'查看反馈','LookFeedBack','2019-03-10 01:58:32'),(3,'添加回复','AddReply','2019-03-10 01:58:32'),(4,'删除回复','DelReply','2019-03-10 01:58:32'),(5,'查看回复','ViewReply','2019-03-10 01:58:32'),(6,'数据统计','DataCount','2019-03-10 01:58:32');
/*!40000 ALTER TABLE `auths` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedbacks`
--

DROP TABLE IF EXISTS `feedbacks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feedbacks` (
  `fid` int(11) NOT NULL AUTO_INCREMENT,
  `openid` varchar(50) NOT NULL,
  `phone` varchar(12) NOT NULL,
  `content` text NOT NULL,
  `navtype` varchar(20) NOT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`fid`),
  KEY `ix_feedbacks_time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedbacks`
--

LOCK TABLES `feedbacks` WRITE;
/*!40000 ALTER TABLE `feedbacks` DISABLE KEYS */;
/*!40000 ALTER TABLE `feedbacks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `imagematerials`
--

DROP TABLE IF EXISTS `imagematerials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `imagematerials` (
  `imid` int(11) NOT NULL AUTO_INCREMENT,
  `add_time` datetime DEFAULT NULL,
  `keyword` varchar(50) NOT NULL,
  `media_id` varchar(50) NOT NULL,
  PRIMARY KEY (`imid`),
  UNIQUE KEY `keyword` (`keyword`),
  KEY `ix_imagematerials_add_time` (`add_time`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imagematerials`
--

LOCK TABLES `imagematerials` WRITE;
/*!40000 ALTER TABLE `imagematerials` DISABLE KEYS */;
INSERT INTO `imagematerials` VALUES (1,'2019-03-09 19:19:12','河大图片','thisisamedia');
/*!40000 ALTER TABLE `imagematerials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `musicmaterials`
--

DROP TABLE IF EXISTS `musicmaterials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `musicmaterials` (
  `mmid` int(11) NOT NULL AUTO_INCREMENT,
  `add_time` datetime DEFAULT NULL,
  `keyword` varchar(50) NOT NULL,
  `title` varchar(60) NOT NULL,
  `description` varchar(100) NOT NULL,
  `music_url` varchar(2000) NOT NULL,
  `hqmusic_url` varchar(2000) NOT NULL,
  PRIMARY KEY (`mmid`),
  UNIQUE KEY `keyword` (`keyword`),
  KEY `ix_musicmaterials_add_time` (`add_time`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `musicmaterials`
--

LOCK TABLES `musicmaterials` WRITE;
/*!40000 ALTER TABLE `musicmaterials` DISABLE KEYS */;
INSERT INTO `musicmaterials` VALUES (1,'2019-03-09 19:19:18','听听歌曲','动物世界-薛之谦','动物世界都太假','https://m10.music.126.net/20190309191150/4c30c8a0f1d8fb8a567b27ac1ec169ea/ymusic/d444/4451/6e2c/665169e0e959fc602f8ed1315de4c13e.mp3','https://m10.music.126.net/20190309191150/4c30c8a0f1d8fb8a567b27ac1ec169ea/ymusic/d444/4451/6e2c/665169e0e959fc602f8ed1315de4c13e.mp3');
/*!40000 ALTER TABLE `musicmaterials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `newsmaterials`
--

DROP TABLE IF EXISTS `newsmaterials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `newsmaterials` (
  `nmid` int(11) NOT NULL AUTO_INCREMENT,
  `add_time` datetime DEFAULT NULL,
  `keyword` varchar(50) NOT NULL,
  `title` varchar(60) NOT NULL,
  `description` varchar(100) NOT NULL,
  `pic_url` varchar(2000) NOT NULL,
  `url` varchar(2000) NOT NULL,
  PRIMARY KEY (`nmid`),
  UNIQUE KEY `keyword` (`keyword`),
  KEY `ix_newsmaterials_add_time` (`add_time`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `newsmaterials`
--

LOCK TABLES `newsmaterials` WRITE;
/*!40000 ALTER TABLE `newsmaterials` DISABLE KEYS */;
INSERT INTO `newsmaterials` VALUES (1,'2019-03-09 19:16:43','河北大学','河大欢迎你','亲爱的新生，你们好，欢迎关注和大青年','http://www.hbu.edu.cn/u/cms/hbu/201711/07100234zsb9.jpg','http://www.hbu.edu.cn/');
/*!40000 ALTER TABLE `newsmaterials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operatelogs`
--

DROP TABLE IF EXISTS `operatelogs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `operatelogs` (
  `oid` int(11) NOT NULL AUTO_INCREMENT,
  `aid` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `reason` varchar(600) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`oid`),
  KEY `aid` (`aid`),
  KEY `ix_operatelogs_add_time` (`add_time`),
  CONSTRAINT `operatelogs_ibfk_1` FOREIGN KEY (`aid`) REFERENCES `admins` (`aid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operatelogs`
--

LOCK TABLES `operatelogs` WRITE;
/*!40000 ALTER TABLE `operatelogs` DISABLE KEYS */;
/*!40000 ALTER TABLE `operatelogs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phones`
--

DROP TABLE IF EXISTS `phones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phones` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `address` varchar(40) NOT NULL,
  `phone` varchar(16) NOT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=137 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phones`
--

LOCK TABLES `phones` WRITE;
/*!40000 ALTER TABLE `phones` DISABLE KEYS */;
INSERT INTO `phones` VALUES (1,'研究生院办公室','5971132'),(2,'文学院办公室','5079302'),(3,'文学院团委','5079303'),(4,'历史学院办公室','5077310'),(5,'历史学院团委','5077302'),(6,'新闻传播学院办公室','5079310'),(7,'新闻传播学院团委','5079309'),(8,'新闻学院团委','5079309'),(9,'经济学院办公室','5079320'),(10,'经济学院团委','5079327'),(11,'管理学院办公室','5977048'),(12,'管理学院团委','5079595'),(13,'外国语学院办公室','5073256'),(14,'外国语学院团委','5073257'),(15,'教育学院办公室','5079334'),(16,'教育学院团委','5079743'),(17,'政法学院办公室','5079340'),(18,'政法学院团委','5079339'),(19,'艺术学院办公室','5073050'),(20,'艺术学院团委','5073061'),(21,'计算机科学与技术学院办公室','5079351'),(22,'计算机科学与技术学院团委','5073087'),(23,'数学与信息科学学院办公室','5079351'),(24,'数学与信息科学学院团委','5079729'),(25,'物理科学与技术学院办公室','5079354'),(26,'物理科学与技术学院团委','5077315'),(27,'化学与环境科学学院办公室','5079359'),(28,'化学与环境科学学院团委','5079592'),(29,'药学院办公室','5971107'),(30,'药学院团委','5971107'),(31,'生命科学学院办公室','5079364'),(32,'生命科学学院团委','5079363'),(33,'电子信息工程学院办公室','5079368'),(34,'电子信息工程学院团委','5079367'),(35,'建筑工程学院办公室','5079375'),(36,'建筑工程学院团委','5079342'),(37,'质量技术监督学院办公室','5092717'),(38,'质量技术监督学院办公室','5079329'),(39,'临床医学院办公室','5981697'),(40,'护理学院办公室','5075665'),(41,'护理学院团委','5075626'),(42,'公共卫生学院办公室','5075639'),(43,'公共卫生学院团委','5078509'),(44,'基础医学院办公室','5079008'),(45,'基础医学院团委','5097490'),(46,'中医学院办公室','5075644'),(47,'中医学院团委','5078514'),(48,'继续教育学院办公室','5079378'),(49,'人民武装学院办公室','0311-85200867'),(50,'党委办公室','5079433'),(51,'纪委办公室','5079650'),(52,'党委组织部','5079438'),(53,'党委宣传部','5079440'),(54,'党委统战部','5079740'),(55,'工会','5079466'),(56,'校团委','5079462'),(57,'校长办公室','5079709'),(58,'人事处','5079468'),(59,'老干部处','5079343'),(60,'教务处','5079473'),(61,'教师教学发展中心','5079371'),(62,'学生处','5079444'),(63,'心理健康','5977074'),(64,'生活园区','5079410'),(65,'就业办','5079445'),(66,'国防教育','5971127'),(67,'红色战线','5079693'),(68,'国防生办','5077308'),(69,'武装部','5079444'),(70,'国有资产管理处办公室','5079507'),(71,'保卫处','5079506'),(72,'校园管理处','5079634'),(73,'国际合作处','5079766'),(74,'发展规划办公室','5079783'),(75,'实验室管理办公室副主任室','5073999'),(76,'学位委员会办公室副主任室','5977058'),(77,'教育教学质量评估办公室副主任室','5977077'),(78,'新校区管理与建设办公室','5073298'),(79,'新闻中心','5079787'),(80,'机关党委','5079576'),(81,'网络中心','5079705'),(82,'图书馆','5079425'),(83,'档案馆','5071118'),(84,'博物馆','5077063'),(85,'期刊社','5079697'),(86,'校友会','5079774'),(87,'医学学科建设领导小组办公室','5079040'),(88,'大学科技园管理办公室','5077331'),(89,'河大社区','5079648'),(90,'学术委员会','5079607'),(91,'附属医院院办公室','5981680'),(92,'校医院门诊','5079659'),(93,'校医院南院医务','5079780'),(94,'校医院新区医务','5929855'),(95,'产业办公室','5079513'),(96,'人工环境公司','5079567'),(97,'出版社','5073003'),(98,'赫达实业办公室','5079539'),(99,'易百超市','5922099'),(100,'赫达实业文印中心','5079546'),(101,'赫达实业物业公司','5938587'),(102,'赫达实业驾校','7532111'),(103,'华萃园','5079694'),(104,'主楼咖啡','5079564'),(105,'新区咖啡','5073300'),(106,'后勤综合部','7532000'),(107,'后勤本部收发','5079714'),(108,'后勤新区收发','5073088'),(109,'后勤本部公寓','5079534'),(110,'后勤新区公寓','5929920'),(111,'餐饮公司办公室','5079559'),(112,'医学部后勤服务公司办公室','5097499'),(113,'高教学会办公室','5079759'),(114,'关心下一代工作委员会办公室','5079436'),(115,'关心老一辈工作委员会办公室','5079464'),(116,'老教授协会办公室','5069575'),(117,'马克思学院','5079448'),(118,'外语教研部','5079405'),(119,'数学教研部','5079658'),(120,'体育教研部','5079409'),(121,'计算中心办公室','5079390'),(122,'文科综合实验教学中心办公室','5073888'),(123,'医学实验中心办公室','5075522'),(124,'宋史中心','5079415'),(125,'医学部党支部','5079020'),(126,'医学部行政办公室','5079021'),(127,'医学部保卫科','5079034'),(128,'工商学院团委','5073135'),(129,'工商学院人文学部','6773055'),(130,'工商学院经济管理学部','5073116'),(131,'工商学院经济学部','5073116'),(132,'工商学院信息科学与工程学部','6773077'),(133,'工商学院信息学部','6773077'),(134,'工商学院国际文化交流学部','6773066'),(135,'附属医院','5981680'),(136,'校医院','5079554');
/*!40000 ALTER TABLE `phones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `rid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `auths` varchar(600) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`rid`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_roles_add_time` (`add_time`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'超级管理员','1,2,3,4,5,6','2019-03-10 03:08:20'),(2,'普通管理员','1,2,3,5,6','2019-03-10 03:08:20');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `textmaterials`
--

DROP TABLE IF EXISTS `textmaterials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `textmaterials` (
  `tmid` int(11) NOT NULL AUTO_INCREMENT,
  `add_time` datetime DEFAULT NULL,
  `keyword` varchar(50) NOT NULL,
  `content` text NOT NULL,
  PRIMARY KEY (`tmid`),
  UNIQUE KEY `keyword` (`keyword`),
  KEY `ix_textmaterials_add_time` (`add_time`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `textmaterials`
--

LOCK TABLES `textmaterials` WRITE;
/*!40000 ALTER TABLE `textmaterials` DISABLE KEYS */;
INSERT INTO `textmaterials` VALUES (1,'2019-03-09 19:16:39','hello','欢迎关注河大青年~~~'),(2,'2019-03-10 13:08:51','系统错误','系统错误，请联系管理员修复~~'),(3,'2019-03-10 13:08:51','关注','啦啦啦，啦啦啦，我们是河大的小管家！\n“河小博”“河小知”“河掌柜”三个萌娃带你走遍河大！\n\n学习上有问题就找“河小博”\n生活有疑惑就找“河小知”\n还有什么想问的就找“河掌柜”哈~~\n\n回复【菜单】即可找到三个萌娃噻~~'),(4,'2019-03-10 13:08:51','留言','您的留言小编已经收到了\n回复【菜单】查看全部功能哦'),(5,'2019-03-10 13:08:51','河小博','好好学习，天天向上\nHELLO~我是河小博~\n回复括号内的信息进行下一步查询\n 【成绩查询】\n 【图书信息】\n 【空闲自习室】\n 【网上评教】\n 【办公电话】'),(6,'2019-03-10 13:08:51','河小知','嗨亲~我是河小知~\n活动超丰富，小知都知道哟~\n回复括号内的信息进行下一步查询\n 【国际交流】\n 【社团活动】'),(7,'2019-03-10 13:08:51','河掌柜','来喽~我是河掌柜~\n有事您说话~\n回复括号内的信息进行下一步查询\n 【天气预报】\n 【公交查询】\n 【后勤报修】'),(8,'2019-03-10 13:08:51','菜单','回复以下括号内的关键词就可以收到相应的内容哦\n河小博：\n 【成绩查询】\n 【课表查询】\n 【图书信息】\n 【空闲自习室】\n 【网上评教】\n河小知：\n 【天气预报】\n 【公交查询】\n 【快递查询】\n 【办公电话】\n 【国际交流】\n 【创业就业】\n河掌柜：\n 【学生公寓】\n 【后勤报修】\n 【河大全景】\n 【培训信息】\n 【河大驾校】\n 【图书订购】\n 【易百超市】\n 【意见反馈】\n新生同学看过来:\n 【新生】'),(9,'2019-03-10 13:08:51','绑定学号','亲，要先绑定学号哦！\n绑定学号的操作方法为: \n发送“绑定+空格+学号+空格+教务系统密码” \n如：绑定 20181234123 20181234123 \n教务系统的初始密码是学号，学号绑定的密码一定要与教务系统密码一致呦!\n如果教务系统密码发生了修改，务必要修改河大青年的密码为教务系统密码!\n可发送“修改密码”获取提示，根据提示修改密码。'),(10,'2019-03-10 13:08:51','绑定格式','绑定学号的操作方法为: \n发送“绑定+空格+学号+空格+教务系统密码”'),(11,'2019-03-10 13:08:51','绑定成功','绑定成功！\n发送【我的学籍】查看已绑信息\n发送【修改密码】查看如何修改密码\n发送【解除绑定】解除绑定的学号\n发送【我的成绩】即可查询本学期成绩'),(12,'2019-03-10 13:08:51','绑定失败','绑定失败!请仔细检查:\n账号为学号，密码为教务系统密码哦~\n可能系统网络延迟，也可以重新尝试哦~'),(13,'2019-03-10 13:08:51','已经绑定','亲，你已经绑定咯~\n发送【修改密码】查看如何修改密码'),(14,'2019-03-10 13:08:51','解除绑定','回复【确认解绑】解除绑定\n解除绑定后，不能使用成绩查询等功能哦~~'),(15,'2019-03-10 13:08:51','解绑成功','解除绑定成功\n你仍可以使用部分功能哦~~\n回复【菜单】即可查看全部功能哦'),(16,'2019-03-10 13:08:51','修改密码','亲，修改密码格式如下哦\n请回复：改密+空格+教务系统密码\n如：改密 20181234123'),(17,'2019-03-10 13:08:51','改密格式','修改密码的操作方法为: \n发送“改密+空格+教务系统密码”'),(18,'2019-03-10 13:08:51','改密成功','修改成功!\n发送【我的学籍】查看已绑信息\n发送【修改密码】查看如何修改密码\n发送【解除绑定】解除绑定的学号\n发送【我的成绩】即可查询本学期成绩'),(19,'2019-03-10 13:08:51','改密失败','修改失败!请仔细检查:\n密码为教务系统密码哦~\n可能系统网络延迟，也可以重新尝试哦~'),(20,'2019-03-10 13:08:51','成绩查询','发送【我的学籍】查看学籍信息\n发送【我的成绩】查看本学期成绩\n发送【所有成绩】即可查询所有成绩'),(21,'2019-03-10 13:08:51','天气预报','来喽~我是河掌柜~有事您说话~\n请回复：天气+空格+城市\n如：天气 保定'),(22,'2019-03-10 13:08:51','学生公寓','回复：\n【调宿服务】\n【退宿服务】\n【公寓电话】\n即可查看详细说明'),(23,'2019-03-10 13:08:51','图书信息','好好学习，天天向上\nHELLO~我是河小博~\n请回复：图书+空格+图书名称\n如：图书 新闻学概论'),(25,'2019-03-10 13:08:51','公交查询','目前只提供保定市公交线路查询哦~~~\n1.发送\"附近公交+空格+当前位置\"如：\"河北大学\"即可查询附近的所有站点\n2.发送\"公交+空格+公交线路\"如：\"公交 27\"即可查询该线路所有站点\n3.发送\"公交+空格+起点+空格+终点\"即可查询可乘坐的公交线路，如\"公交 河北大学 火车站\"'),(26,'2019-03-10 13:08:51','快递查询','快递查询方式为：\n发送\"快递+空格+快递单号\"即可查询快递信息，\n如：快递 123456789'),(27,'2019-03-10 13:08:51','办公电话','好好学习,天天向上\nHELLO~我是河小博~\n1.请回复：\"办公机构\" 即可查询所有办公机构\n2.请回复：\"电话+空格+办公机构\"\n如\"电话 物理学院\"即可查询办公电话'),(28,'2019-03-10 13:08:51','国际交流','<a href=\"http://oice.hbu.edu.cn/\">河小博带你走进国际交流处，点击即可查看（建议在wifi环境下使用）</a>'),(29,'2019-03-10 13:08:51','创业就业','嗨亲~我是河小知 发送:\n【我来创业】\n【就业信息】\n即可进行查询哦'),(30,'2019-03-10 13:08:51','我来创业','嗨亲~我是河小知 \n发送括号内的关键词\n【创业基地简介】\n【入驻条件】\n【入驻程序】\n【创业优惠政策】\n即可进行创业信息查询哦'),(31,'2019-03-10 13:08:51','创业基地简介','大学生创业孵化基地简介\n大学生创业孵化基地(以下简称创业基地)是在高新区管委会和河北大学的领导下，由河大科技园有限公司负责指导与管理。大学生创业孵化基地是河大科技园有限公司下属综合性指导机构，基地实行企业化管理，为入驻大学生创业、就业提供物质帮助与技术支持。\n创业基地的主要任务：提供创业孵化场地和孵化企业基本办公条件，搭建科技信息网络平台，提供科技和产业信息，帮助创业孵化企业进入市场或营造局部市场环境以及为入孵企业提供法律、财务、管理等创业所需的重要信息及咨询服务。\n地址：河北省保定市北二环路5699号大学科技园7号楼A座 \n电话：0312-3376005   0312-5077331 \nEmail: hbdxkjy@126.com\n传真：0312-3376006 \n邮编：071051'),(32,'2019-03-10 13:08:51','入驻条件','创业基地入驻条件\n1、符合国家产业、技术政策，技术含量较高，创新性较强，有较强的市场竞争力，有利于节能降耗和环境保护，经济效益和社会效益显著，孵化项目原则上应立足于创业团队的自身专业领域，以提高专业技能和创新实践能力为主要目的；\n2、孵化企业具有完整创业计划，启动资金和创业团队，具有明确的市场应有的目标和市场经营计划，并通过创业基地审核的，准备开业的企业；\n3、处于研发阶段的项目（需有明确的市场应用目标和经营构想），可以项目组的形式入驻创业基地；\n4、必须是在保定国家高新区工商行政管理部门注册登记的法人实体，或已注册登记的，必须将公司注册地迁到保定国家高新区\n5、公司负责人（或孵化企业法人）为全日制在校大学生，或毕业两年内的大学生，具有较高的素养和品格，懂政策，重信誉，有一定的经营能力，接受河大科技园有限公司的管理，遵守一切规章制度。'),(33,'2019-03-10 13:08:51','入驻程序','创业基地入驻程序\n1、提交申请入驻材料。\n入驻企业提供的材料有：入驻基地申请；商业计划书；公司相关管理制度、企业章程；法定代表人简历及身份证明复印件；营业执照证书复印件；企业委托代办相关手续的，需提供注册登记所需的有关证明材料。\n2、企业填写企业基本情况表。\n3、基地进行初步审查，报河大科技园有限公司创业导师团审批。\n4、评审通过后，签定入驻创业基地协议。\n5、基地协助孵化企业搬迁入驻，办理相关证、照。\n具体程序请与我处联系\n地址：河北省保定市国家高新技术开发区朝阳路科技园 \n电话：0312-5077329 \nEmail: kjy@hbu.edu.cn\n传真：5077331 \n邮编：071002'),(34,'2019-03-10 13:08:51','创业优惠政策','入驻企业性质与优惠政策\n大学生创业公司分为设计类、服务类和商贸类等类型的公司。基地鼓励工业设计、软件设计类企业优先入驻，智力服务类、商贸类公司其次，对于其他类型公司进行严格审批。\n创业公司营运资金实行“学生自筹+创业基金资助”的模式；\n学校为入驻公司提供以下支持与优惠：\n1、免费为入驻企业提供1年场地租赁费；一年免租期到期后，在孵企业可继续留在孵化基地，第二年享受市场租赁费减半的优惠，第三年以市场价缴纳租赁费，孵化满三年后，在孵企业必须退出创业基地，并优先推荐其进入科技园园或产业园进一步孵化；\n2、免费为入驻公司提供网络端口、电源接口、办公桌椅、资料柜等办公设备（孵化器项目经费中出）\n3、对公司办理工商、税务登记和变更、年检及公司代码、银行开户手续提供指导；\n4、为入驻企业提供有偿财务会计服务（专设一人）\n5、联系有协作关系的咨询公司，为公司提供技术与管理的咨询服务；\n6、提供文讯、打字复印等有偿服务；\n7、帮助企业解决其他有关事宜。'),(35,'2019-03-10 13:08:51','就业信息','嗨亲~我是河小知~近期招聘信息汇总如下哦:\n<a href=\'http://job.hbu.cn：8080/news/ShowArticle.asp?ArticleID=2337\'>麦当劳校园招聘</a>\n<a href=\'http://job.hbu.cn：8080/news/ShowArticle.asp?ArticleID=2340\'>5月19日河北大学小型招聘会参会企业名单</a>\n<a href=\'http://job.hbu.cn：8080/news/ShowArticle.asp?ArticleID=2295\'>北京爱其科技有限公司校园招聘</a>\n<a href=\'http://job.hbu.cn：8080/news/ShowArticle.asp?ArticleID=2293\'>5月12日河北大学小型招聘会参会企业名单</a>\n<a href=\'http://job.hbu.cn：8080/news/ShowArticle.asp?ArticleID=2290\'>永旺集团招聘</a>\n\n具体信息以校就业指导网公布信息为准'),(36,'2019-03-10 13:08:51','调宿服务','【1】因特殊原因学生个人申请调宿的，凭个人书面申请，经学生所在学院同意、园区办公室审核，到公寓中心综合部办理调宿手续。\n【2】学生公寓办理学生调宿手续：楼层服务员检查原宿舍公共设施情况，收回宿舍钥匙，退还学生住宿卡片；学生凭住宿卡片到调整后公寓值班室，工作人员核对、更改住宿卡片，发放宿舍钥匙，学生将个人物品搬入调整后宿舍。'),(37,'2019-03-10 13:08:51','退宿服务','【1】退宿条件：A身体有疾病，确需在外休养，B家在保定市居住，C在校勤工俭学需夜间值班。\n【2】学生凭离校通知单或《河北大学学生公寓退宿申请表》到公寓办理退宿手续。\n【3】楼层服务员检验宿舍公共设施。\n【4】学生交回宿舍钥匙，公寓楼长在离校通知单或退宿审批表加盖公寓检验章。\n【5】中心在离校通知单或退宿审批表加盖公寓中心章，涉及退住宿费的到公司财务部办理退费手续。\n【6】学生搬出宿舍，退宿办理完毕。'),(38,'2019-03-10 13:08:51','公寓电话','【校本部公寓】\n茗园公寓 5079449\n慧园公寓 5079323\n沁园公寓 5079451\n菊园公寓 5079452\n桂园公寓 5079453\n芳园公寓 5079454\n荷园公寓 5079665\n熙园公寓 5079667\n竹园公寓 5079689\n馨园公寓 5079670\n梅园公寓 5079311\n恬园公寓 5079639\n【新校区公寓】\n厚望公寓 南5929923/北7532021\n厚泽公寓 南5929925/北5929924\n厚朴公寓 南5929927/北7532026\n信佳公寓 5929996\n信香公寓 南5929928/北5929929\n信然公寓 南5929932/中5929933/北5929934\n信士公寓 南5929930 /北5929931\n馨宁公寓 南5929946/ 北5929948\n馨雅公寓 南5929944/北5929945\n馨清公寓 5929950\n馨逸公寓 5929952\n馨源公寓 南5929916/北5929918\n【医学部公寓】\n学生公寓1号楼：5075681\n学生公寓2号楼：5075682\n学生公寓3号楼：5075683\n学生公寓4号楼：7910658\n学生公寓5号楼：7910659'),(39,'2019-03-10 13:08:51','后勤报修','【本部、新校区】\n综合保障服务热线“7532000”、“7532555”24小时为您提供维修、咨询和服务投诉等服务。\n\n【医学部】\n后勤服务公司24小时维修电话。\n水暖维修：5097495；\n电力维修：5097498；\n负责人电话：13833033717'),(40,'2019-03-10 13:08:51','河大全景','<a href=\"https://jiejing.qq.com/#pano=11061118130817105158100&heading=5&pitch=1&zoom=1&isappinstalled=-1&poi=0\">河小知带你走遍河大，点击即可查看（建议在wifi环境下使用）</a>'),(41,'2019-03-10 13:08:51','培训信息','后勤集团培训学校送福利啦！有意参加教师资格证、会计证、人力资源师、秘书、心理咨询师、育婴师、公共营养师等培训项目的同学注意喽！\n【一】凡关注“河北大学青年”微信公众服务平台的河北大学在册学生到我校报名培训项目学费优惠5%。\n【二】 凡报名参加我校培训项目的学员均可成为我校会员。会员享受以下增值服务：\n 【1】所有会员免费在我校教室上自习。\n 【2】自带笔记本电脑的会员享受免费无线上网服务。\n 【3】全天免费供应饮用水。\n 【4】不定期向会员免费提供励志电影服务。\n【本部校区地址】河大本部南院浴池三楼           \n咨询电话：0312-5958960\n【新区校区地址】河大新区坤舆园区餐厅北侧四楼\n咨询电话：0312-5929995'),(42,'2019-03-10 13:08:51','河大驾校','河北大学驾驶员培训学校于2002年成立，驾校占地面积60亩，拥有教练车40辆，C1/C2两个培训车型，配有45台电脑智能化答题教室，电动式教车一台，电子操纵仿真模拟器4部，机械模拟器15台，解剖车一部，并配有专门的模拟教学室，具有二级资质的大型国营驾校。\n\n十余年来，驾校多次获得了省市交通运管部门颁发的“省级先进驾校”、“AAA驾校”等多项荣誉。\n\n咨询服务热线：0312-7532111（新区）0312-5079017（本部）'),(43,'2019-03-10 13:08:51','图书订购','亲爱的同学们，河北大学青年联合后勤集团推出当当网图书代购活动了！同学们绑定学号后，将获得当当网图书零利润、免运费代购服务哦！喜欢读书的同学过来看一看啦！同学们再也不用担心自己没有时间去去“当当”了。\n【服务项目】如下：\n 【1】后勤集团代购服务集中采购，为同学们节约运费；\n 【2】后勤集中收货，同学们可选择自主时间取货；\n 【3】同学们可选择货到付款，后勤集团可以为同学们提前支付，降低购买风险；\n 【4】如果同学们在当当网上没有找到需要的书，后勤集团可以为大家联系出版社直接订购。\n【订购方法】：\n 【1】同学们先到当当网上选择需要购买的图书；\n 【2】之后将图书信息交至本部南院八教学楼一层西侧赫达文化传播公司业务办公室，留下联系方式并交纳小额订金，业务办公室联系电话：13603240321\n 【3】收货后以短信或电话的方式通知同学们取货；\n 【4】同学们选择空闲时间取货并支付书款。'),(44,'2019-03-10 13:08:51','易百超市','易百超市共有五个超市，其中：\n【毓秀园店】\n河大本部南院，服务电话：5079563；\n【怡然亭店】\n河大北院，服务电话：5971145； \n【坤舆湖店】\n河大新区坤舆湖的南面，服务电话：7532004；\n【坤舆泉店】\n坤舆园区综合楼的北侧，服务电话：7532007；\n【易百新店】\n馨源楼的西面，服务电话：5922099；\n\n各点服务时间为：早7:30分—晚10:30分，'),(45,'2019-03-10 13:08:51','新生','<a href=\"http://h.eqxiu.com/s/bCG5asAT\">hello！欢迎新童鞋！点击即可查询新生板块。河大青年在手中，学习生活很轻松！（建议在wifi环境下打开）</a>\n'),(46,'2019-03-11 01:20:24','国交中心服务','<a href=\"http://www.iesc.cn/\" class=\"ui-link\">河小博带你走进国际交流服务中心，点击即可查看（建议在wifi环境下使用）</a>'),(47,'2019-03-11 02:50:34','洗衣服务','【赫达干洗卡，自主洗衣机卡充值赠送活动】\n凡在活动期间一次性充值200元以上（含200元）的顾客，均可获赠价值20-100元不等的精美礼品一份或手机充值卡一张。\n【活动时间】\n2014年03月31日--2014年04月30日\n【校本部代收点】\n河北大学后勤集团洗涤部（南院食堂北侧）\n咨询电话：5079654\n【新校区代收点】\n厚朴楼122室，咨询电话：7532009'),(48,'2019-03-11 12:48:19','公益河大','【西部计划】又是一年似火的初夏，青春洋溢、壮志凌云的毕业生们即将告别丰富多彩的大学生活，怀揣梦想与斗志步入社会，开启人生新的征程，开拓新的人生事业，成为祖国建设事业各条战线上的骨干。对于每个应届大学毕业生而言，选择去西部、去基层是一次新的机遇、新的挑战。在那里，将获得施展才华、实现人生价值的广阔舞台。在那里，会经受生活的磨炼，直面失败与挫折，甚至体味失败与挫折的辛酸，但是，也一定会感受到成功的喜悦，收获宝贵的精神财富。在此，我们真诚地欢迎你们报名参加西部计划，感受新西部、体验新生活、实现新成长！\n\n咨询方式：\n\n1、到河北大学团委宣传部进行相关咨询\n\n2、致电西部计划河北大学项目办公室，咨询电话为：0312-5079462、18330219679\n\n3、 关注河北大学弘毅网站，及时了解相关动态'),(49,'2019-03-11 23:39:42','校园漫步','来喽~我是河掌柜~\n大家回复：\n【河大全景】\n【洗衣服务】\n【培训信息】\n【河大驾校】\n【图书订购】\n【易百超市】\n即可查询。'),(50,'2019-03-11 23:40:44','选课信息','各位亲，又到了选课的时候了，大家千万不要错过时间哦！\n'),(51,'2019-03-11 23:43:27','我的学业','好好学习，天天向上\nHELLO~我是河小博~发送：\n【成绩查询】\n【选课信息】\n【我的课表】\n【我的学籍】\n【修改密码】\n【绑定学号】\n【解除绑定】\n即可查询');
/*!40000 ALTER TABLE `textmaterials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `openid` varchar(50) NOT NULL,
  `studentID` varchar(11) NOT NULL,
  `studentPWD` varchar(50) NOT NULL,
  `bindingTime` date NOT NULL,
  `leftTime` date NOT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `openid` (`openid`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (7,'oOBVv1cFS_mZnLps3GBhrMwQqac0','20171004113','199892.lw','2019-03-15','2019-03-15');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `videomaterials`
--

DROP TABLE IF EXISTS `videomaterials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `videomaterials` (
  `vimid` int(11) NOT NULL AUTO_INCREMENT,
  `add_time` datetime DEFAULT NULL,
  `keyword` varchar(50) NOT NULL,
  `media_id` varchar(50) NOT NULL,
  `title` varchar(60) NOT NULL,
  `description` varchar(100) NOT NULL,
  PRIMARY KEY (`vimid`),
  UNIQUE KEY `keyword` (`keyword`),
  KEY `ix_videomaterials_add_time` (`add_time`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `videomaterials`
--

LOCK TABLES `videomaterials` WRITE;
/*!40000 ALTER TABLE `videomaterials` DISABLE KEYS */;
INSERT INTO `videomaterials` VALUES (1,'2019-03-09 19:18:44','看看河大','thisisamediaid','看看河大','河大好风光～～河大真的大～～');
/*!40000 ALTER TABLE `videomaterials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `voicematerials`
--

DROP TABLE IF EXISTS `voicematerials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `voicematerials` (
  `vomid` int(11) NOT NULL AUTO_INCREMENT,
  `add_time` datetime DEFAULT NULL,
  `keyword` varchar(50) NOT NULL,
  `media_id` varchar(50) NOT NULL,
  PRIMARY KEY (`vomid`),
  UNIQUE KEY `keyword` (`keyword`),
  KEY `ix_voicematerials_add_time` (`add_time`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `voicematerials`
--

LOCK TABLES `voicematerials` WRITE;
/*!40000 ALTER TABLE `voicematerials` DISABLE KEYS */;
INSERT INTO `voicematerials` VALUES (1,'2019-03-09 19:16:53','聆听河大','thisisamediaid');
/*!40000 ALTER TABLE `voicematerials` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-03-15  8:40:51
