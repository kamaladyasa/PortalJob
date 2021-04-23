-- public.users definition

-- Drop table

-- DROP TABLE public.users;

CREATE TABLE public.users (
	id serial NOT NULL,
	email varchar(100) NOT NULL,
	"password" varchar NOT NULL,
	first_name varchar(40) NOT NULL,
	last_name varchar(40) NULL,
	date_of_birth timestamp NOT NULL,
	gender varchar(10) NOT NULL,
	contact_number varchar(20) NOT NULL,
	registration_date timestamp NOT NULL,
	CONSTRAINT users_email_key UNIQUE (email),
	CONSTRAINT users_pkey PRIMARY KEY (id)
);
CREATE INDEX ix_users_id ON public.users USING btree (id);

INSERT INTO public.users (id,email,"password",first_name,last_name,date_of_birth,gender,contact_number,registration_date) VALUES
	 (2,'diyan@test.com','$2b$12$OmT6nn5XL4L5j5ONtHcli.NKxM3xjvKqTAULRmwVy0bb/qcLHZDuG','Diyan','Maulana','1998-05-30 00:00:00','Male','0812*******','2021-04-20 21:43:47.155667'),
	 (3,'fadil@test.com','$2b$12$AahsGx9TYzfn10vf60DOwuvsVXzaWxRxA.ssqFB7bn27LM9fhUUCG','Fadil','Sudirman','1995-08-17 00:00:00','Male','0812*******','2021-04-20 21:44:32.627521'),
	 (4,'willy@test.com','$2b$12$3dyb5gpYyeG94azdLHJqi.F33VXlyGKGTql7xLqNMROSqYBl6vUPy','Willy','Kusumaatmaja','1993-01-11 00:00:00','Male','0812*******','2021-04-22 14:18:25.966233'),
	 (5,'yanti@test.com','$2b$12$uDmwo90M.Fulzwl/WwLV..r5EbL3lGpnM0AciMFMViaa0tum21Xz6','Yanti','Wahyuningsih','1992-11-02 00:00:00','Female','0812*******','2021-04-22 14:21:21.004939'),
	 (6,'fira@test.com','$2b$12$BppPnbdqdq5b.OnW.JvAZu.CExps96oBQ2T0fcqMGgpfbvNxaOX4W','Fira','Safitri','1995-02-12 00:00:00','Female','0812*******','2021-04-22 14:35:58.993499'),
	 (8,'fauzan@test.com','$2b$12$X02wM6Th3l2QaT6p5bJpJuJ81j1AmNLLsrHXs46MZL3iNGF5XHE0q','Fauzan','Irfani','1995-03-10 00:00:00','Male','0812*******','2021-04-22 14:42:38.522005'),
	 (9,'sulaiman@test.com','$2b$12$NSQ59eJQFUyQ8FYvkd7cK.OtgrVm0l.pB1VNR9z7NsXO.59N5FdkO','Sulaiman','Ali','1990-12-31 00:00:00','Male','0812*******','2021-04-22 14:45:54.886651'),
	 (10,'ibrahim@test.com','$2b$12$CL0Fcwx4S0xfdurWoQpegOWs/18TEqaTbVTDF7epvrBo./9s2ScNa','Ibrahim','Alkatiri','1994-07-21 00:00:00','Male','0812*******','2021-04-22 15:04:51.006866'),
	 (1,'kamaladyasa@test.com','$2b$12$udYMSmFOXeAX8clJYMH6i.4ZWDyMMG6fPeQ944gTU7E13Yc0TQG9C','Kamal','Adyasa','2000-04-19 00:00:00','Male','081212122222','2021-04-20 21:42:52.483682');