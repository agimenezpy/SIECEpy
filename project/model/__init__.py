
PERIODS = ("EFM", "FMA", "MAM",
           "AMJ", "JJA", "JAS",
           "ASO", "SON", "OND", "NDE")

CLIMATE_MODELS = {
    "tiempo": dict(
        prec=[
            dict(title="Paraguay", content="WRF3.4/PY-10km-p.gif"),
            dict(title="Sudamérica", content="WRF3.4/SA-30km-p.gif")
        ],
        temp=[
            dict(title="Paraguay", content="WRF3.4/PY-10km-t.gif"),
            dict(title="Sudamérica", content="WRF3.4/SA-30km-t.gif")
        ]),
    "clima": dict(
        prec=[
            dict(title="Miembro 1", region="Paraguay", period=PERIODS,
                 content="CWRF3.4/PARAGUAY/M1/%(period)s_2017M1.jpg"),
            dict(title="Miembro 2", region="Paraguay", period=PERIODS,
                 content="CWRF3.4/PARAGUAY/M2/%(period)s_2017M2.jpg"),
            dict(title="Miembro 3", region="Paraguay", period=PERIODS,
                 content="CWRF3.4/PARAGUAY/M3/%(period)s_2017M3.jpg"),
            dict(title="Miembro 4", region="Paraguay", period=PERIODS,
                 content="CWRF3.4/PARAGUAY/M4/%(period)s_2017M4.jpg"),
            dict(title="Miembro 1", region="Sudamérica", period=PERIODS,
                 content="CWRF3.4/PARAGUAY/M1/%(period)s_2017M1.jpg"),
            dict(title="Miembro 2", region="Sudamérica", period=PERIODS,
                 content="CWRF3.4/PARAGUAY/M2/%(period)s_2017M2.jpg"),
            dict(title="Miembro 3", region="Sudamérica", period=PERIODS,
                 content="CWRF3.4/PARAGUAY/M3/%(period)s_2017M3.jpg"),
            dict(title="Miembro 4", region="Sudamérica", period=PERIODS,
                 content="CWRF3.4/PARAGUAY/M4/%(period)s_2017M4.jpg")
        ],
        temp=[
            dict(title="Miembro 1", region="Paraguay", period=PERIODS,
                 content="CWRF3.4/PARAGUAY/M1/%(period)s_t_2017M1.jpg"),
            dict(title="Miembro 2", region="Paraguay", period=PERIODS,
                 content="CWRF3.4/PARAGUAY/M2/%(period)s_t_2017M2.jpg"),
            dict(title="Miembro 3", region="Paraguay", period=PERIODS,
                 content="CWRF3.4/PARAGUAY/M3/%(period)s_t_2017M3.jpg"),
            dict(title="Miembro 4", region="Paraguay", period=PERIODS,
                 content="CWRF3.4/PARAGUAY/M4/%(period)s_t_2017M4.jpg"),
            dict(title="Miembro 1", region="Sudamérica", period=PERIODS,
                 content="CWRF3.4/PARAGUAY/M1/%(period)s_t_2017M1.jpg"),
            dict(title="Miembro 2", region="Sudamérica", period=PERIODS,
                 content="CWRF3.4/PARAGUAY/M2/%(period)s_t_2017M2.jpg"),
            dict(title="Miembro 3", region="Sudamérica", period=PERIODS,
                 content="CWRF3.4/PARAGUAY/M3/%(period)s_t_2017M3.jpg"),
            dict(title="Miembro 4", region="Sudamérica", period=PERIODS,
                 content="CWRF3.4/PARAGUAY/M4/%(period)s_t_2017M4.jpg")
        ]),
    "atmos": dict(
        prec=[
            dict(title="Miembro 1", period=PERIODS,
                 content="CAM/M1/%(period)s_2017.png"),
            dict(title="Miembro 2", period=PERIODS,
                 content="CAM/M2/%(period)s_2017.png"),
            dict(title="Miembro 3", period=PERIODS,
                 content="CAM/M3/%(period)s_2017.png"),
            dict(title="Miembro 4", period=PERIODS,
                 content="CAM/M4/%(period)s_2017.png")
        ],
        temp=[
            dict(title="Miembro 1", period=PERIODS,
                 content="CAM/M1/%(period)s_t_2017.png"),
            dict(title="Miembro 2", period=PERIODS,
                 content="CAM/M2/%(period)s_t_2017.png"),
            dict(title="Miembro 3", period=PERIODS,
                 content="CAM/M3/%(period)s_t_2017.png"),
            dict(title="Miembro 4", period=PERIODS,
                 content="CAM/M4/%(period)s_t_2017.png")
        ])
}