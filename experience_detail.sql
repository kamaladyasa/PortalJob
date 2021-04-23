-- public.experience_detail definition

-- Drop table

-- DROP TABLE public.experience_detail;

CREATE TABLE public.experience_detail (
	id serial NOT NULL,
	job_title varchar(50) NULL,
	company_name varchar(100) NULL,
	job_location_city varchar(50) NULL,
	description_job varchar(2000) NULL,
	start_date timestamp NULL,
	end_date timestamp NULL,
	user_id int4 NOT NULL,
	CONSTRAINT experience_detail_pkey PRIMARY KEY (id)
);
CREATE INDEX ix_experience_detail_id ON public.experience_detail USING btree (id);


-- public.experience_detail foreign keys

ALTER TABLE public.experience_detail ADD CONSTRAINT experience_detail_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);

INSERT INTO public.experience_detail (id,job_title,company_name,job_location_city,description_job,start_date,end_date,user_id) VALUES
	 (1,'Admin','PT. Rumah Perkasa','Kota Bandung','Mengadmini','2017-04-19 00:00:00','2019-04-19 00:00:00',1),
	 (2,'HR','PT. Jaya Abadi','Bandung','Human resources','2017-04-19 00:00:00','2019-04-19 00:00:00',2),
	 (3,'Manager Sales','PT. Rumah Kita Sendiri','Cimahi','Memimpin jalannya pertandingan','2017-04-19 00:00:00','2019-04-19 00:00:00',3),
	 (4,'Customer Service','PT. KAI','Cibadak','Melayani Customer','2016-04-19 00:00:00','2017-04-19 00:00:00',3),
	 (5,'Admin','CV Payoni','Pekalongan','Mengadministrasi pekerjaan','2018-01-19 00:00:00','2019-06-21 00:00:00',1),
	 (6,'CEO','Toko Besi Berkah Jaya','Bandung','Mendirikan Toko Bangunan','2018-01-30 00:00:00','2021-04-22 00:00:00',4),
	 (7,'Digital Marketing','Toko Bunga Matahari','Bekasi','Memasarkan produk bunga','2016-05-10 00:00:00','2021-04-22 00:00:00',5),
	 (8,'Translator Arab-Indonesia','PT Buana Rahasia','Jakarta','Penghubung komunikasi klien','2020-05-10 00:00:00','2021-04-22 00:00:00',6),
	 (10,'Supervisor','PT Merapi Steel','Purwokerto','Memimpin jalannya proyek','2020-05-10 00:00:00','2021-04-22 00:00:00',8);