-- --------------------------------------------------------
-- 主机:                           localhost
-- 服务器版本:                        5.5.54 - MySQL Community Server (GPL)
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  9.3.0.4984
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- 导出  表 db_quick_app.fix_county 结构
CREATE TABLE IF NOT EXISTS `fix_county` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '地市级主键ID',
  `county_id` char(12) DEFAULT NULL COMMENT '地市级代码',
  `county_name` varchar(50) DEFAULT NULL COMMENT '地市级名',
  `father_province` char(2) DEFAULT NULL COMMENT '父级省自治区主键ID',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='省级固定存储表';

-- 数据导出被取消选择。


-- 导出  表 db_quick_app.fix_district 结构
CREATE TABLE IF NOT EXISTS `fix_district` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '区县级主键ID',
  `district_id` char(12) DEFAULT NULL COMMENT '区县级代号',
  `district_name` varchar(60) DEFAULT NULL COMMENT '区县级名',
  `father_county` char(12) DEFAULT NULL COMMENT '父级地市主键ID',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_quick_app.fix_province 结构
CREATE TABLE IF NOT EXISTS `fix_province` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '省自治区级主键ID',
  `province_name` varchar(50) DEFAULT NULL COMMENT '省自治区级代码',
  `province_id` char(2) DEFAULT NULL COMMENT '省自治区级名',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- 数据导出被取消选择。


-- 导出  表 db_quick_app.fix_town 结构
CREATE TABLE IF NOT EXISTS `fix_town` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '镇街道级主键ID',
  `town_id` char(12) DEFAULT NULL COMMENT '镇街道级代码',
  `town_name` varchar(50) DEFAULT NULL COMMENT '镇街道级名',
  `father_distinct` char(12) DEFAULT NULL COMMENT '父级区县主键ID',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- 数据导出被取消选择。


-- 导出  表 db_quick_app.fix_village 结构
CREATE TABLE IF NOT EXISTS `fix_village` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '村社级主键ID',
  `village_cd` char(12) DEFAULT NULL COMMENT '村社级代码',
  `village_type_cd` char(3) DEFAULT NULL COMMENT '村社级类型',
  `village_name` varchar(50) DEFAULT NULL COMMENT '村社级名',
  `father_town` char(12) DEFAULT NULL COMMENT '父级镇街道级主键ID',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- 数据导出被取消选择。
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
