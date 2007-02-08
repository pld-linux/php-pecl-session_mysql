/*

CREATE DATABASE phpsession;

GRANT SELECT,UPDATE,INSERT,DELETE
    ON phpsession.* TO 'phpsession'@'localhost' IDENTIFIED BY 'phpsession';

USE PHPSESSION;
*/

CREATE TABLE phpsession (
	sess_key char(64) not null,
	sess_mtime int(10) unsigned not null,
	sess_host char(64) not null,
	sess_val mediumblob not null,

	index i_key(sess_key(6)),
	index i_mtime(sess_mtime),
	index i_host(sess_host)
);
