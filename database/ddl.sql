CREATE TABLE question_meta (
	qst_id	int(11) NOT NULL	auto_increment,
	dfn_id	int(11) NOT NULL,
	prpt_his_id	int(11) NOT NULL,
	fgpt_id	int(11) NULL,
	gen_eng_cd	varchar(50)	NULL,
	sbj_cd	varchar(5)	NULL,
	grd_cd	varchar(20)	NULL,
	trm_cd	varchar(20)	NULL,
	ctg1_cd	varchar(100)	NULL,
	ctg2_cd	varchar(100)	NULL,
	ctg3_cd	varchar(100)	NULL,
	ctg4_cd	varchar(100)	NULL,
	qst	text	NULL,
	lgnds	text	NULL,
	answ	text	NULL,
	crt_at	timestamp	NULL,
	mod_at	timestamp	NULL,
	PRIMARY KEY(qst_id) 
);

CREATE TABLE fingerprint_meta (
	fgpt_id	int(11) NOT NULL	auto_increment,
	dfn_id	int(11) NOT NULL,
	prpt_his_id	int(11) NOT NULL,
	gen_eng_cd	varchar(50)	NOT NULL,
	sbj_cd	varchar(5)	NOT NULL,
	grd_cd	varchar(20)	NOT NULL,
	trm_cd	varchar(20)	NOT NULL,
	ctg1_cd	varchar(100)	NOT NULL,
	ctg2_cd	varchar(100)	NULL,
	ctg3_cd	varchar(100)	NULL,
	ctg4_cd	varchar(100)	NULL,
	fgpt	text	NULL,
	crt_at	timestamp	NULL,
	mod_at	timestamp	NULL,
	PRIMARY KEY(fgpt_id)
);

CREATE TABLE define_meta (
	dfn_id	int(11) NOT NULL	auto_increment,
	prpt_his_id	int(11) NOT NULL,
	gen_eng_cd	varchar(50)	NOT NULL,
	sbj_cd	varchar(5)	NOT NULL,
	grd_cd	varchar(20)	NOT NULL,
	trm_cd	varchar(20)	NOT NULL,
	ctg1_cd	varchar(100)	NOT NULL,
	ctg2_cd	varchar(100)	NULL,
	ctg3_cd	varchar(100)	NULL,
	ctg4_cd	varchar(100)	NULL,
	title	varchar(100)	NOT NULL,
	desc1	text	NOT NULL,
	cont1	text	NULL,
	desc2	text	NULL,
	cont2	text	NULL,
	desc3	text	NULL,
	cont3	text	NULL,
	desc4	text	NULL,
	cont4	text	NULL,
	smmr	text	NULL,
	crt_at	timestamp	NULL,
	mod_at	timestamp	NULL,
	PRIMARY KEY(dfn_id)
);

CREATE TABLE code_meta (
	cd_id	int(11) NOT NULL	auto_increment,
	cd_val	varchar(10)	NOT NULL,
	cd_nm	varchar(100)	NOT NULL,
	crt_at	timestamp	NULL,
	mod_at	timestamp	NULL,
	PRIMARY KEY(cd_id)
);

drop table prompt_history;
CREATE TABLE prompt_history (
	prpt_his_id	int(11) NOT NULL,
	gen_eng_cd varchar(50) NOT NULL,
	prpt	text	NOT NULL,
	result	text	NOT NULL,
	crt_at	timestamp	NOT NULL,
	PRIMARY KEY(prpt_his_id)
);

drop table question_answer_history;
CREATE TABLE question_answer_history (
	qst_his_id	int(11) NOT NULL,
	usr_Id	varchar(50)	NOT NULL,
	std_cnt	int(11) NOT NULL	DEFAULT 1,
	qst_id	int(11) NOT NULL,
	answer	varchar(1000)	NULL,
	crrct_yn varchar(1) not null default '0',
	crt_at	timestamp	NOT NULL,
	PRIMARY KEY(qst_his_id)
);

