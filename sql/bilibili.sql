SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for bilibili_member
-- ----------------------------
DROP TABLE IF EXISTS `bilibili_member`;
CREATE TABLE `bilibili_member`  (
  `mid` int(11) UNSIGNED NOT NULL COMMENT 'b站用户唯一id',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '用户昵称',
  `sign` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '个人签名',
  `rank` int(11) UNSIGNED NULL DEFAULT NULL COMMENT '排名?暂时不知道',
  `level` tinyint(3) UNSIGNED NULL DEFAULT NULL COMMENT '等级',
  `jointime` int(10) UNSIGNED NULL DEFAULT NULL COMMENT '加入时间(都是0...)',
  `moral` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '道德值',
  `silence` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '0正常 1被封禁',
  `birthday` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '生日(月-日)',
  `coins` int(11) UNSIGNED NULL DEFAULT NULL COMMENT '所持金币(都是0...)',
  `fans_badge` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '粉丝徽章',
  `vip_type` tinyint(3) UNSIGNED NULL DEFAULT NULL COMMENT '0非vip 1好像和0一样 2年度大会员',
  `vip_status` tinyint(3) UNSIGNED NULL DEFAULT NULL COMMENT '0未激活 1激活',
  `create_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录插入时间',
  `update_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录更新时间',
  PRIMARY KEY (`mid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for failure_record
-- ----------------------------
DROP TABLE IF EXISTS `failure_record`;
CREATE TABLE `failure_record`  (
  `mid` bigint(20) UNSIGNED NOT NULL COMMENT 'b站用户id',
  `remark` varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '备注',
  `state` tinyint(4) UNSIGNED NOT NULL COMMENT '状态 0未修复 1已修复 2暂时忽略',
  `create_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`mid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
