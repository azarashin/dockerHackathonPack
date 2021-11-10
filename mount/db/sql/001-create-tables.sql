
DROP DATABASE IF EXISTS `db_steam_product`;

CREATE DATABASE `db_steam_product`;
USE `db_steam_product`;

CREATE TABLE IF not exists `product`(
	id int, 
	status_flag char(16), 
	title char(255), 
	publisher char(255), 
	developer char(255), 
	release_date datetime, 
	price float, 
	price_country char(32),
	review_type char(32), 
	review_count int, 
	rating_value int, 
	max_rating int, 
	min_rating int
);


CREATE TABLE IF not exists `user_language`(
	id int, 
	lang_title char(64), 
	interface boolean, 
	full_audio boolean, 
	subtitles boolean
);

CREATE TABLE IF not exists `tag`(
	id int, 
	tag char(64)
);

CREATE TABLE IF not exists `genre`(
	id int, 
	genre char(32)
);

CREATE TABLE IF not exists `price`(
	id int, 
	price float
);

CREATE TABLE IF not exists `discount_price`(
	id int, 
	original_price float, 
	discouted_price float
);
