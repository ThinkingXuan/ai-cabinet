-- 用户表：使用 account_id 作为唯一标识，不使用外键
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '系统主键',
    account_id VARCHAR(64) NOT NULL UNIQUE COMMENT '全局唯一账号ID（逻辑主键）',
    username VARCHAR(50) NOT NULL COMMENT '用户名',
    email VARCHAR(100) COMMENT '邮箱',
    password_hash VARCHAR(255) NOT NULL COMMENT '加密后的密码',
    gender ENUM('male', 'female', 'other') COMMENT '性别',
    birthdate DATE COMMENT '出生日期',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) COMMENT='用户信息表';

-- 衣物表：使用 account_id 关联用户，无外键
CREATE TABLE clothes (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '衣物ID',
    account_id VARCHAR(64) NOT NULL COMMENT '所属账号ID',
    name VARCHAR(100) COMMENT '衣物名称',
    category VARCHAR(50) COMMENT '分类，如上衣、裤子',
    color VARCHAR(30) COMMENT '主色调',
    season SET('spring', 'summer', 'autumn', 'winter') COMMENT '适合季节',
    style VARCHAR(50) COMMENT '风格',
    status ENUM('available', 'dirty', 'laundry', 'lost', 'discarded') DEFAULT 'available' COMMENT '状态',
    image_url VARCHAR(255) COMMENT '衣物图片URL',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX (account_id)
) COMMENT='衣物信息表';

-- 标签表：用于给衣物打标签
CREATE TABLE tags (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '标签ID',
    account_id VARCHAR(64) NOT NULL COMMENT '所属账号',
    name VARCHAR(50) NOT NULL COMMENT '标签名称',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (account_id, name),
    INDEX (account_id)
) COMMENT='衣物标签表';

-- 衣物-标签中间表：多对多关系，不使用外键
CREATE TABLE clothes_tags (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '记录ID',
    account_id VARCHAR(64) NOT NULL COMMENT '所属账号',
    clothes_id BIGINT NOT NULL COMMENT '衣物ID',
    tag_id BIGINT NOT NULL COMMENT '标签ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (account_id, clothes_id, tag_id),
    INDEX (account_id)
) COMMENT='衣物与标签的关联表';



-- 穿搭记录：一个搭配包含多件衣物
CREATE TABLE outfits (
	id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '搭配ID', 
	account_id VARCHAR(64) NOT NULL COMMENT '所属账号', 
	name VARCHAR(100) COMMENT '搭配名称', 
	description TEXT COMMENT '搭配描述', 
	style VARCHAR(50) COMMENT '风格', 
	season VARCHAR(50) COMMENT '适合季节', 
	occasion VARCHAR(50) COMMENT '适合场合', 
	clothes_items TEXT COMMENT '包含的衣物ID列表（JSON数组）', 
	image_url VARCHAR(255) COMMENT '搭配展示图', 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX (account_id)
) COMMENT='穿搭记录表';

-- 推荐记录
CREATE TABLE recommendations (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '推荐记录ID',
    account_id VARCHAR(64) NOT NULL COMMENT '所属账号',
    date DATE NOT NULL COMMENT '推荐日期',
    outfit_id BIGINT COMMENT '推荐的搭配ID',
    feedback ENUM('like', 'dislike', 'neutral') DEFAULT 'neutral' COMMENT '用户反馈',
    generated_by_ai BOOLEAN DEFAULT TRUE COMMENT '是否由AI生成',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX (account_id)
) COMMENT='AI推荐记录表';

-- 天气记录
CREATE TABLE weather_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '天气记录ID',
    account_id VARCHAR(64) NOT NULL COMMENT '所属账号',
    date DATE NOT NULL COMMENT '日期',
    location VARCHAR(100) COMMENT '位置（如城市名）',
    temperature DECIMAL(4,1) COMMENT '温度 °C',
    condition VARCHAR(50) COMMENT '天气状况',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX (account_id)
) COMMENT='天气记录表';

-- AI识别数据表：记录每次识别的结果
CREATE TABLE clothes_ai_info (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '识别记录ID',
    account_id VARCHAR(64) NOT NULL COMMENT '所属账号',
    clothes_id BIGINT NOT NULL COMMENT '衣物ID',
    detected_category VARCHAR(50) COMMENT 'AI识别分类',
    detected_color VARCHAR(30) COMMENT 'AI识别颜色',
    detected_texture VARCHAR(50) COMMENT '纹理/图案',
    ai_confidence DECIMAL(5,2) COMMENT '识别置信度',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX (account_id)
) COMMENT='衣物AI识别信息';

-- 衣柜共享（家庭/好友共享）
CREATE TABLE shared_wardrobes (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '共享记录ID',
    account_id VARCHAR(64) NOT NULL COMMENT '拥有者账号',
    shared_with_account_id VARCHAR(64) NOT NULL COMMENT '被共享账号',
    role ENUM('read', 'write') DEFAULT 'read' COMMENT '共享权限',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (account_id, shared_with_account_id),
    INDEX (account_id),
    INDEX (shared_with_account_id)
) COMMENT='衣柜共享关系表';

-- 用户身材表：与用户表通过account_id关联
CREATE TABLE user_body_info (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '身材信息ID',
    account_id VARCHAR(64) NOT NULL UNIQUE COMMENT '关联的账号ID',
    avatar_url VARCHAR(255) COMMENT '用户头像URL',
    height DECIMAL(5,2) COMMENT '身高(cm)',
    weight DECIMAL(5,2) COMMENT '体重(kg)',
    upper_body_length DECIMAL(5,2) COMMENT '上身长度(cm)',
    lower_body_length DECIMAL(5,2) COMMENT '下身长度(cm)',
    body_shape VARCHAR(50) COMMENT '身材类型，如梨形、苹果型等',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX (account_id)
) COMMENT='用户身材信息表';
