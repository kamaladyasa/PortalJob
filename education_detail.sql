-- public.education_detail definition

-- Drop table

-- DROP TABLE public.education_detail;

CREATE TABLE public.education_detail (
	id serial NOT NULL,
	last_education varchar(30) NOT NULL,
	major varchar(50) NOT NULL,
	univ_name varchar(100) NOT NULL,
	start_date timestamp NOT NULL,
	complete_date timestamp NULL,
	gpa float8 NULL,
	user_id int4 NOT NULL,
	CONSTRAINT education_detail_pkey PRIMARY KEY (id)
);
CREATE INDEX ix_education_detail_id ON public.education_detail USING btree (id);


-- public.education_detail foreign keys

ALTER TABLE public.education_detail ADD CONSTRAINT education_detail_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);

INSERT INTO public.education_detail (last_education,major,univ_name,start_date,complete_date,gpa,user_id) VALUES
	 ('S1','Statistics','Islamic University','2017-04-19 00:00:00','2021-04-19 00:00:00',3.99,1),
	 ('S1','Informatics Engineering','Telkom University','2017-04-19 00:00:00','2021-04-19 00:00:00',3.0,2),
	 ('S1','Telecomunication','Telkom University','2017-04-19 00:00:00','2021-04-19 00:00:00',3.01,3),
	 ('SMA','Science','SMA Islam','20112-04-19 00:00:00','2015-04-19 00:00:00',9.88,1),
	 ('SMA','Science','SMAN 6 Bengkulu','2012-04-19 00:00:00','2015-04-19 00:00:00',9.08,2),
	 ('SMA','Social','SMKN 16 Bandung','2012-04-19 00:00:00','2015-04-19 00:00:00',8.08,3),
	 ('SMA','Social','SMAN 5 Bandung','2007-04-19 00:00:00','2010-04-19 00:00:00',9.18,4),
	 ('SMA','Science','SMAN 1 Madura','2010-03-02 00:00:00','2013-05-20 00:00:00',9.18,5),
	 ('SMA','Bahasa','SMAN 99 Jakarta','2012-02-02 00:00:00','2015-12-20 00:00:00',9.88,6),
	 ('SMA','Social','STM Muhammadiyah Banyumas','2012-08-12 00:00:00','2015-12-20 00:00:00',9.99,8);
INSERT INTO public.education_detail (last_education,major,univ_name,start_date,complete_date,gpa,user_id) VALUES
	 ('S1','Telecommunication','Telkom University','2016-08-12 00:00:00','2020-12-20 00:00:00',3.11,8),
	 ('S1','Linguistics','Al-Azhar University','2016-08-12 00:00:00','2020-12-20 00:00:00',3.41,6),
	 ('S1','Physics','Institute of Technology Surabaya','2013-05-12 00:00:00','2017-11-20 00:00:00',3.71,5),
	 ('S1','','Telkom University','2010-05-12 00:00:00','2014-11-20 00:00:00',3.55,4),
	 ('S1','','Binus University','2016-05-12 00:00:00','2020-11-20 00:00:00',2.55,9),
	 ('S1','Medical Science','University of Indonesia','2016-05-12 00:00:00','2020-11-20 00:00:00',2.15,10),
	 ('SMA','Science','SMAN 1 Pekalongan','2009-05-12 00:00:00','2012-11-20 00:00:00',8.88,10);