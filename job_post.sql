-- public.job_post definition

-- Drop table

-- DROP TABLE public.job_post;

CREATE TABLE public.job_post (
	id serial NOT NULL,
	title varchar(50) NOT NULL,
	company_id int4 NOT NULL,
	created_date timestamp NOT NULL,
	job_description varchar(1000) NULL,
	location_city varchar(50) NOT NULL,
	specialization varchar(70) NOT NULL,
	is_active bool NULL,
	CONSTRAINT job_post_pkey PRIMARY KEY (id)
);
CREATE INDEX ix_job_post_id ON public.job_post USING btree (id);


-- public.job_post foreign keys

ALTER TABLE public.job_post ADD CONSTRAINT job_post_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.company(id);

INSERT INTO public.job_post (id,title,company_id,created_date,job_description,location_city,specialization,is_active) VALUES
	 (2,'Translator Mandarin',2,'2021-04-20 21:56:17.152742','Membantu menerjemahkan Bahasa Mandarin - Indonesia atau sebaliknya','Jakarta Selatan','Admin/ Secretarial',true),
	 (3,'Marketing Head',3,'2021-04-22 22:23:57.125747','Maintenance Customer, looking for new customer, handle marketing team','Surabaya','Pemasaran/ Penjualan',true),
	 (4,'IT Developer',3,'2021-04-22 22:31:03.126709','Design and proposed application architecture, develop application according to agreed user requirement','Jakarta','Teknologi Informasi, IT Admin',true),
	 (5,'Bussiness Development Supervisor',4,'2021-04-22 22:32:56.365042','Develop a growth strategy focusing on both financial gain and customer satisfaction','Yogyakarta','Penjualan/ Pemasaran, Pengembangan Bisnis',true),
	 (6,'Teknisi Elektronik',4,'2021-04-22 22:34:41.790335','Membaca skematik rangkaian elektronik, melakukan uji diagnosis dan QC produk','Yogyakarta','Teknik, Elektronika',true),
	 (7,'Call Center Agent',5,'2021-04-22 22:38:47.363297','Provide Service to Customer via Telephone, email and Other existing Channel','Bandung','Pelayanan, Layanan Pelanggan',true),
	 (8,'Finance & Tax Staff',5,'2021-04-22 22:40:07.838901','Count all tax objects and make e-billing, e-filling, and e-bupot every month.','Bandung','Keuangan, Akuntansi, Pembiayaan',true),
	 (1,'Personal Assistant Pribadi',1,'2021-04-20 21:51:24.583155','Provide secretarial and administrative support, manage & coordinate meetings.','Bandung','Admin/ Secretarial',true),
	 (9,'Driver Delivery',6,'2021-04-23 10:18:58.500409','Mengantarkan barang yang akan dikirim ke customer.','Tangerang','Driver',true);