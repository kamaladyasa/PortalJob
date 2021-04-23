-- public.company definition

-- Drop table

-- DROP TABLE public.company;

CREATE TABLE public.company (
	id serial NOT NULL,
	email varchar(100) NOT NULL,
	"password" varchar NOT NULL,
	company_name varchar(70) NOT NULL,
	website varchar(40) NULL,
	contact_number varchar(20) NOT NULL,
	profile_description varchar(1000) NULL,
	address varchar(100) NOT NULL,
	city varchar(40) NOT NULL,
	registration_date timestamp NOT NULL,
	CONSTRAINT company_email_key UNIQUE (email),
	CONSTRAINT company_pkey PRIMARY KEY (id)
);
CREATE INDEX ix_company_id ON public.company USING btree (id);

INSERT INTO public.company (email,"password",company_name,website,contact_number,profile_description,address,city,registration_date) VALUES
	 ('inovastek@test.com','$2b$12$k.hP9rGglDh52IeF5pkboeg3fMsH.2D13CDvGE45Ojuv/w5qDVcG6','PT Inovastek Glomatra Indonesia','inovastek.com','0852*******','PT. Inovastek Glomatra Indonesia produce a detailed local forecast,fromweather, ocean, hydro-meteorological disaster, severe weather warnings, to decision support system for agricultural and industrial management','Jl. Sukahaji Permai, Sukasari','Bandung','2021-04-20 21:47:00.480637'),
	 ('cahaya@test.com','$2b$12$GkdK2QuYVudEdnjiehAtZeFaSVtvIodLYSJpvHEgcgwNFHkZcNcT2','PT Cahaya Dunia Ekspedisi','cahaya.com','0852*******','J&T Express merupakan perusahaan yang bergerak di bidang pengiriman ekspress yang berbasis perkembangan teknologi sebagai dasar dari sistemnya.','Jl. Warung Buncit Raya No. 2 Kalibata, Pancoran','Jakarta Selatan','2021-04-20 21:54:37.024486'),
	 ('temas@test.com','$2b$12$wtUXhhpxhnkl48.UmDFFNeHU1/175sBoCwdMVyv03rdEY5mhvyX7.','PT TEMAS TBK','temas.com','0852*******','The Company conducts its main line of business in shipping, offering full-containerized shipping services covering both domestic and international markets.','JL. Yos Sudarso Kav. 33','Surabaya','2021-04-22 15:48:28.312956'),
	 ('nsi@test.com','$2b$12$7USjCmxzF5WKGyz6GB/GXudCkfSqyRqrPlOiA00v6NEiORltGqkoy','PT Nanosense Instrument Indonesia','nanosense.com','0852*******','PT Nanosense Instrument Indonesia merupakan perusahaan startup yang berfokus pada manufaktur dan produksi sistem sensor yang terintegrasi dengan artificial intelligence (AI) dan nanotechnology.','JL. Gito-gati No.12','Yogyakarta','2021-04-22 17:13:50.528485'),
	 ('cemerlang@test.com','$2b$12$Jf23EBWgkYj0ICK7fdjEzOmz5P03P8yD1/D05wlyn7LzIdeDjCkRu','PT Cemerlang Multimedia','cemerlang.com','0852*******','PT. Cemerlang Multimedia melahirkn produk broadband internet dengan menggunakan teknologi FTTH (Fiber To The Home).','JL. Batununggal No.128','Kota Bandung','2021-04-22 17:22:54.833439'),
	 ('hema@test.com','$2b$12$1px.zWi/bjAMR4wsXGsp9ekbChII9FjMjvP.HVAKtikH1C6qdl0DS','PT Hema Medhajaya','hema.com','0852*******','PT Hema Medhajaya has the vision and creativity to manage a better future indeed.','JL. Otto Iskandar No.28A','Tangerang','2021-04-23 10:17:32.708334');