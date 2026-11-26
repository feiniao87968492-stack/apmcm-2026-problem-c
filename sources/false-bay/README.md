# False Bay ERA5 snapshots

Retrieved 2026-11-26. These files preserve the Open-Meteo API responses. The underlying ERA5 reanalysis is from the Copernicus Climate Change Service. Wind is 10 m wind speed in m/s at the returned cell (-34.25, 18.50). Wave height is total significant wave height in metres at the returned offshore cell (-34.50, 18.50). The offshore value is a regional sea-state proxy.

- [Wind request](https://archive-api.open-meteo.com/v1/archive?latitude=-34.25&longitude=18.50&start_date=2022-06-06&end_date=2022-06-28&hourly=wind_speed_10m&timezone=Africa%2FJohannesburg&models=era5&cell_selection=nearest&wind_speed_unit=ms)
- [Wave request](https://marine-api.open-meteo.com/v1/marine?latitude=-34.20&longitude=18.62&start_date=2022-06-06&end_date=2022-06-28&hourly=wave_height&timezone=Africa%2FJohannesburg&models=era5_ocean&cell_selection=sea)
- [ERA5 single levels](https://doi.org/10.24381/cds.adbb2d47)
- [Playback study](https://doi.org/10.12688/openreseurope.24618.1)

SHA-256 wind.json: 98024e1efae9edf22f782d0dce322527815a51154c9837e9582e909b125ca299

SHA-256 wave.json: afd7b356d893b61f0a7bae70ff3f0d7e4cf5624b958af2c7508cef9b49d890ca

Both APIs returned Africa/Johannesburg timestamps at UTC+02:00. The analysis selects the six hourly timestamps 08:00 through 13:00 on each of the 12 Data02 dates. Runtime reads only these archived files.

The user-supplied WAVERYS snapshot is archived as [waverys.json](waverys.json). It contains VHM0 (total significant wave height in metres) at four cells, with 36 timestamped values per cell. The analysis uses the cells at (-34.2, 18.6) and (-34.4, 18.6) and interpolates the local 08:00, 11:00 and 14:00 values to the six hours from 08:00 to 13:00 each date. The remaining cells are retained in the snapshot. The catalogue and exact Zarr asset are recorded in the JSON. SHA-256 is 3018d8c11ceb9696f8c83e58e9402705c3e617cd9718797880feaf209ab93ff5. [Copernicus Marine catalogue](https://stac.marine.copernicus.eu/metadata/GLOBAL_MULTIYEAR_WAV_001_032/cmems_mod_glo_wav_my_0.2deg_PT3H-i_202411/dataset.stac.json)
